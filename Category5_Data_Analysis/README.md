# Skillova Trainee Assessment - Category 5: Data Analysis

## What this project does

This project cleans a synthetic dataset of 1,000 customer-support tickets and answers two questions:

1. What is the average resolution time after cleaning?
2. Which ticket category takes the longest to solve?

## Data source

The assessment allows candidates to generate a messy dataset.

The file `customer_support_tickets_messy.csv` was generated using Python with a fixed random seed. The script `generate_dataset.py` is included so the same dataset can be reproduced.

The dataset contains:

- 1,000 rows
- 40 blank resolution-time values
- 10 extreme resolution-time values of 999,999 hours

## Files

```text
Category5_Data_Analysis/
├── customer_support_tickets_messy.csv
├── generate_dataset.py
├── customer_support_ticket_analysis.ipynb
├── customer_support_tickets_cleaned.csv
├── category_resolution_summary.csv
├── FINAL_REPORT.pdf
├── Research_Log.docx
└── README.md