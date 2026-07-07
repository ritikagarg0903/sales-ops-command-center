from __future__ import annotations

from datetime import date

import pandas as pd


HIGH_RISK_TERMS = {
    "budget": "budget uncertainty",
    "frozen": "budget freeze",
    "competitor": "competitive evaluation",
    "procurement": "procurement delay",
    "legal": "legal review delay",
    "no economic buyer": "missing economic buyer",
    "no recent activity": "no recent activity",
    "blocked": "blocked review",
    "uncertain": "unclear timing",
}

POSITIVE_TERMS = {
    "champion": "champion identified",
    "executive sponsor": "executive sponsor engaged",
    "business case": "business case approved",
    "verbal approval": "verbal approval",
    "purchase order": "purchase order requested",
    "legal review complete": "legal review complete",
}


def _days_since(value: str) -> int:
    if not value:
        return 999
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return 999
    return (pd.Timestamp(date.today()) - parsed).days


def score_deal(row: pd.Series) -> dict[str, str]:
    notes = str(row.get("notes", "")).lower()
    stage = row.get("stage", "")
    forecast = row.get("forecast_category", "")
    days_in_stage = int(row.get("days_in_current_stage", 0))
    days_since_activity = _days_since(row.get("last_activity_date", ""))
    expected_close = pd.to_datetime(row.get("expected_close_date", ""), errors="coerce")

    score = 0
    reasons = []

    for term, reason in HIGH_RISK_TERMS.items():
        if term in notes:
            score += 2
            reasons.append(reason)

    positive_hits = [reason for term, reason in POSITIVE_TERMS.items() if term in notes]
    score -= min(len(positive_hits), 2)

    if stage in {"Proposal", "Negotiation"} and days_in_stage >= 45:
        score += 2
        reasons.append(f"{days_in_stage} days in {stage}")
    elif days_in_stage >= 70:
        score += 1
        reasons.append("long stage aging")

    if days_since_activity >= 21:
        score += 2
        reasons.append(f"no activity in {days_since_activity} days")

    if pd.notna(expected_close) and expected_close.date() < date.today() and stage not in {"Closed Won", "Closed Lost"}:
        score += 2
        reasons.append("past expected close date")

    if forecast == "Commit" and score >= 3:
        score += 1
        reasons.append("risky Commit forecast")

    if score >= 5:
        level = "High"
    elif score >= 3:
        level = "Medium"
    else:
        level = "Low"

    if not reasons and positive_hits:
        reasons = positive_hits[:2]
    if not reasons:
        reasons = ["normal deal progression"]

    return {
        "ai_risk_level": level,
        "ai_risk_reason": _reason_sentence(level, reasons),
        "recommended_action": _recommended_action(level, stage, forecast, reasons),
    }


def _reason_sentence(level: str, reasons: list[str]) -> str:
    joined = ", ".join(dict.fromkeys(reasons[:3]))
    return f"{level} risk: {joined}."


def _recommended_action(level: str, stage: str, forecast: str, reasons: list[str]) -> str:
    reason_text = " ".join(reasons).lower()

    if level == "High" and forecast == "Commit":
        return "Review before the forecast call and confirm whether this belongs in Commit."
    if "economic buyer" in reason_text or "champion" in reason_text:
        return "Confirm decision maker, champion strength, and next mutual action."
    if "procurement" in reason_text or "legal" in reason_text:
        return "Ask rep for procurement/legal owner, blocker, and target signature date."
    if "activity" in reason_text:
        return "Require a next step update or move the deal out of active forecast."
    if stage == "Negotiation":
        return "Validate close plan, paper process, and remaining approval steps."
    if level == "Medium":
        return "Monitor in pipeline review and ask for a dated next step."
    return "Keep current, with no immediate manager escalation."


def add_risk_scores(deals: pd.DataFrame) -> pd.DataFrame:
    scored = deals.copy()
    open_mask = ~scored["stage"].isin(["Closed Won", "Closed Lost"])
    risk_rows = scored.loc[open_mask].apply(score_deal, axis=1, result_type="expand")
    scored[["ai_risk_level", "ai_risk_reason", "recommended_action"]] = ""
    scored.loc[open_mask, ["ai_risk_level", "ai_risk_reason", "recommended_action"]] = risk_rows
    scored.loc[~open_mask, "ai_risk_level"] = "Closed"
    scored.loc[~open_mask, "ai_risk_reason"] = "Closed deal excluded from open-pipeline risk scoring."
    scored.loc[~open_mask, "recommended_action"] = "No open-pipeline action."
    return scored
