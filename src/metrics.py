from __future__ import annotations

import pandas as pd


CLOSED_STAGES = ["Closed Won", "Closed Lost"]
OPEN_STAGES = ["Prospecting", "Qualified", "Proposal", "Negotiation"]
STAGE_ORDER = ["Prospecting", "Qualified", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]


def open_deals(deals: pd.DataFrame) -> pd.DataFrame:
    return deals[~deals["stage"].isin(CLOSED_STAGES)].copy()


def closed_won(deals: pd.DataFrame) -> pd.DataFrame:
    return deals[deals["stage"] == "Closed Won"].copy()


def closed_deals(deals: pd.DataFrame) -> pd.DataFrame:
    return deals[deals["stage"].isin(CLOSED_STAGES)].copy()


def sales_cycle_days(deals: pd.DataFrame) -> pd.Series:
    created = pd.to_datetime(deals["created_date"], errors="coerce")
    closed = pd.to_datetime(deals["actual_close_date"], errors="coerce")
    return (closed - created).dt.days


def win_rate(deals: pd.DataFrame, group_by: str | None = None) -> pd.DataFrame | float:
    closed = closed_deals(deals)
    if closed.empty:
        return 0.0 if group_by is None else pd.DataFrame(columns=[group_by, "win_rate"])
    if group_by is None:
        return (closed["stage"].eq("Closed Won").mean() * 100).round(1)
    result = closed.groupby(group_by)["stage"].apply(lambda values: values.eq("Closed Won").mean() * 100)
    return result.round(1).reset_index(name="win_rate")


def quota_attainment(deals: pd.DataFrame, quotas: pd.DataFrame, quarter: str) -> pd.DataFrame:
    won = closed_won(deals)
    won_revenue = won.groupby("rep_name", as_index=False)["deal_amount"].sum().rename(columns={"deal_amount": "closed_won_revenue"})
    quota = quotas[quotas["quarter"] == quarter].copy()
    result = quota.merge(won_revenue, on="rep_name", how="left")
    result["closed_won_revenue"] = result["closed_won_revenue"].fillna(0)
    result["attainment_pct"] = (result["closed_won_revenue"] / result["quota"] * 100).round(1)
    result["quota_gap"] = (result["quota"] - result["closed_won_revenue"]).clip(lower=0)
    return result.sort_values("attainment_pct", ascending=False)


def pipeline_coverage(deals: pd.DataFrame, attainment: pd.DataFrame) -> dict[str, float]:
    open_pipeline = open_deals(deals)["deal_amount"].sum()
    weighted_pipeline = open_deals(deals)["weighted_pipeline"].sum()
    remaining_gap = attainment["quota_gap"].sum()
    if remaining_gap <= 0:
        raw_coverage = 0.0
        weighted_coverage = 0.0
    else:
        raw_coverage = open_pipeline / remaining_gap
        weighted_coverage = weighted_pipeline / remaining_gap
    return {
        "open_pipeline": float(open_pipeline),
        "weighted_pipeline": float(weighted_pipeline),
        "remaining_quota_gap": float(remaining_gap),
        "pipeline_coverage": round(raw_coverage, 2),
        "weighted_coverage": round(weighted_coverage, 2),
    }


def forecast_accuracy(deals: pd.DataFrame) -> pd.DataFrame:
    commit = deals[deals["forecast_category"] == "Commit"].copy()
    if commit.empty:
        return pd.DataFrame(columns=["rep_name", "committed_pipeline", "actual_closed_won", "accuracy_pct"])
    committed = commit.groupby("rep_name", as_index=False)["deal_amount"].sum().rename(columns={"deal_amount": "committed_pipeline"})
    won_commit = commit[commit["stage"] == "Closed Won"].groupby("rep_name", as_index=False)["deal_amount"].sum()
    won_commit = won_commit.rename(columns={"deal_amount": "actual_closed_won"})
    result = committed.merge(won_commit, on="rep_name", how="left")
    result["actual_closed_won"] = result["actual_closed_won"].fillna(0)
    result["accuracy_pct"] = (result["actual_closed_won"] / result["committed_pipeline"] * 100).round(1)
    result["forecast_gap"] = result["committed_pipeline"] - result["actual_closed_won"]
    return result.sort_values("accuracy_pct", ascending=False)


def stage_conversion(deals: pd.DataFrame) -> pd.DataFrame:
    counts = deals["stage"].value_counts().reindex(STAGE_ORDER, fill_value=0).reset_index()
    counts.columns = ["stage", "deal_count"]
    counts["next_stage_count"] = counts["deal_count"].shift(-1)
    counts["conversion_to_next_pct"] = (counts["next_stage_count"] / counts["deal_count"] * 100).round(1)
    counts.loc[counts["stage"].isin(["Closed Won", "Closed Lost"]), "conversion_to_next_pct"] = None
    return counts


def stale_deals(deals: pd.DataFrame, min_days: int = 45) -> pd.DataFrame:
    open_pipeline = open_deals(deals)
    return open_pipeline[open_pipeline["days_in_current_stage"] >= min_days].sort_values(
        ["days_in_current_stage", "deal_amount"], ascending=[False, False]
    )


def filter_deals(deals: pd.DataFrame, quarter: str, segments: list[str], reps: list[str], categories: list[str]) -> pd.DataFrame:
    filtered = deals[deals["close_quarter"] == quarter].copy()
    if segments:
        filtered = filtered[filtered["segment"].isin(segments)]
    if reps:
        filtered = filtered[filtered["rep_name"].isin(reps)]
    if categories:
        filtered = filtered[filtered["forecast_category"].isin(categories)]
    return filtered
