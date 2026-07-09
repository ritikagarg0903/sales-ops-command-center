# AI-Assisted Sales Pipeline Command Center

An interactive sales operations portfolio project that analyzes synthetic CRM data for pipeline health, quota attainment, forecast accuracy, rep performance, funnel conversion, and AI-assisted deal risk.

The dashboard is framed around a practical business problem: helping revenue leaders understand whether the team has enough quality pipeline, which deals create forecast risk, and where manager attention should be focused before pipeline and forecast reviews.

## Why This Project Exists

Sales operations teams help leadership answer practical revenue questions:

- Do we have enough pipeline to hit quota?
- Which reps are on track or at risk?
- Are committed forecast deals actually closing?
- Where are deals stalling in the funnel?
- Which open deals need manager attention before the forecast call?

This dashboard turns synthetic CRM-style data into those business answers.

## Key Features

- Executive overview with open pipeline, weighted pipeline, quota gap, and coverage ratio
- Pipeline health by stage and segment
- Rep performance by quota attainment, win rate, deal size, and sales cycle
- Forecast accuracy comparing Commit deals against actual closed-won revenue
- Funnel conversion analysis by sales stage
- AI-assisted deal risk scoring using transparent rules
- Recommended action for risky deals
- Synthetic CRM data generator for safe public portfolio use

## AI Approach

The "AI-assisted" layer uses explainable rules over:

- Deal notes
- Sales stage
- Days in current stage
- Last activity date
- Expected close date
- Forecast category

It produces:

- Risk level: Low, Medium, or High
- One-line reason
- Recommended action

This shows how unstructured sales notes can be converted into decision-useful insights that are easier to review, audit, and act on.

## Tech Stack

- Python
- Streamlit
- pandas
- Plotly

## Project Structure

```text
sales-ops-command-center/
  app.py
  requirements.txt
  README.md
  .gitignore
  data/
    synthetic_deals.csv
    rep_quotas.csv
  src/
    generate_data.py
    metrics.py
    risk_scoring.py
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

The first run creates synthetic data files in the `data/` folder if they do not already exist.

## Synthetic Data Disclaimer

All CRM data in this project is synthetic. No real customers, prospects, employer data, or CRM exports are used.

## What I Would Do With Real CRM Data

With access to Salesforce or HubSpot data, I would:

- Connect to opportunity, account, owner, activity, and quota tables
- Validate stage definitions and forecast categories with sales leadership
- Reconcile closed-won revenue against finance-approved bookings data
- Add historical trend analysis by week and quarter
- Add manager hierarchy and territory segmentation
- Track forecast changes over time instead of only final Commit status
- Build scheduled weekly pipeline risk summaries for sales managers
