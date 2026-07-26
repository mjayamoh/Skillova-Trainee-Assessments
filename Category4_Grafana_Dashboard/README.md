# Skillova Category 4 - Grafana Dashboard

## Goal
Visualise one week of website data in Grafana using exactly two panels:

1. **Page Views over Time** - time-series line chart
2. **Total Signups** - stat panel

## Files

- website_data.csv - original seven-day website dataset
- dashboard.pdf - screenshot of the completed dashboard
- FINAL_REPORT.docx - concise project summary
- RESEARCH_log.docx - completed timestamped research log

## How it was built

1. Uploaded website_data.csv to a public GitHub repository.
2. Connected the GitHub Raw URL through the Grafana Infinity data source.
3. Configured Date as Time and Page_Views and Signups as Number fields.
4. Created a Time series panel for Page Views.
5. Created a Stat panel using the Total calculation for Signups.
6. Exported the completed dashboard as JSON.

## Expected result

- Total signups: **328**
- Highest page views: **2130** on **2026-07-18**

## Screenshots to add

Save these files in the `screenshots` folder:

- `dashboard.pdf` - both panels visible
