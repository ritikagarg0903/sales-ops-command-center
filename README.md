# AI-Assisted Sales Pipeline Command Center

An interactive sales operations portfolio project that analyzes synthetic CRM data for pipeline health, quota attainment, forecast accuracy, rep performance, funnel conversion, and AI-assisted deal risk.

The project is designed for entry-level Sales Operations Analyst, Revenue Operations Analyst, GTM Operations Analyst, and Sales Strategy Analyst roles.

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
- AI-assisted deal risk scoring using free, transparent rules
- Recommended action for risky deals
- Synthetic CRM data generator for safe public portfolio use

## AI Approach

This version does not require a paid AI API.

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

This keeps the demo reliable and free while still showing how unstructured sales notes can be converted into decision-useful insights.

No OpenAI, Anthropic, or paid model key is required for the current version.

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

All required packages are free Python packages.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

The first run creates synthetic data files in the `data/` folder if they do not already exist.

## Demo Talk Track

1. Start with the Executive Overview.
   Explain that raw pipeline is not enough; sales ops also checks weighted coverage against quota gap.

2. Move to Pipeline Health.
   Show where pipeline dollars sit by stage and whether deals are aging.

3. Move to Rep Performance.
   Compare attainment, win rate, average deal size, and sales cycle.

4. Move to Forecast Accuracy.
   Explain why Commit accuracy matters for leadership planning.

5. End with AI Deal Risk.
   Show how notes and activity signals are summarized into risk level, reason, and recommended action.

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
