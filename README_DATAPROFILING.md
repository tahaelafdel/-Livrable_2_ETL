# README_DATAPROFILING.md - Data Quality Audit for Élysée

This document details the health of the filtered dataset `data/processed/filtered_elysee.csv` (2,625 rows).

## Missing Values (NaN) Audit
| Column | Missing % | Strategy |
| :--- | :--- | :--- |
| `id` | 0% | None |
| `price` | **100%** | **CRITICAL:** Data missing from source. Economic hypothesis cannot be fully tested with current tabular data. |
| `host_response_time` | 25.94% | Imputation: "N/A" (indicates irregular/unprofessional hosting). |
| `host_response_rate` | 25.94% | Imputation: 0% or mean. Logic: No response = 0. |
| `host_is_superhost` | 4.91% | Drop rows or impute "f" (false). |
| `host_listings_count` | 0% | None |
| `availability_365` | 0% | None |

## Statistics & Outliers
- **Calculated Host Listings Count:**
    - Min: 1
    - Max: 816 (Clear indicator of massive professionalization)
    - Median: 3
- **Availability 365:**
    - Min: 0 days
    - Max: 365 days
    - Mean: 174 days
- **Prices:**
    - No data available to detect outliers (0€ or 15,000€).

## Cleaning & Normalization Rules for Milestone 3
1. **Price Handling:** Since the `price` column is empty, we will focus on `availability_365` and `host_listings_count` for the economic hypothesis.
2. **Type Conversion:** 
    - `host_response_rate`: Convert "95%" string to float 0.95.
    - `host_is_superhost`: Convert "t"/"f" to boolean/int.
3. **NaN Imputation:**
    - `host_response_time`: Replace NaN with "unknown".
    - `host_response_rate`: Replace NaN with 0.
