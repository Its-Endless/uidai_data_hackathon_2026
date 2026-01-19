# UIDAI Data Hackathon 2026 - Equity and Efficiency in Aadhaar Processes

## Overview
Analysis of anonymized Aadhaar enrolment/update data (March-Dec 2025) to identify patterns, trends, anomalies, and predictive indicators. Focus: Regional equity (per-capita normalization), process efficiency (conversion rates), age disparities, and forecasting.

Key insights: Equity gaps (NE states lead per-capita), child-focused enrolments, early 2025 anomalies, stabilization forecasts.

## Requirements
- Python 3.10+
- pandas, matplotlib, seaborn, prophet

Install: `pip install pandas matplotlib seaborn prophet`

## Files
- concat.py: Combines chunked CSV files into combined datasets.
- explore.py: Initial data understanding (shapes, dates, totals).
- insights_fixed.py: Core analysis (grouping, normalization, plots, anomalies).
- predict_fixed.py: Time-series forecasting with Prophet.

## How to Run
1. Place UIDAI-provided CSV chunks in a folder.
2. Run concat.py → generates combined_*.csv
3. Run explore.py → basic stats
4. Run insights_fixed.py → main insights + plots
5. Run predict_fixed.py → forecasts + plots

Note: Actual datasets not included (UIDAI-provided anonymized data).
