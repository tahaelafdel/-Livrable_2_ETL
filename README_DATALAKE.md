# README_DATALAKE.md - Data Infrastructure Overview

This project follows a layered architecture to transform raw data into actionable intelligence.

## 1. Bronze Zone (Raw Data Lake)
The landing zone for all raw, unformatted data.
- **Tabular:** `data/raw/tabular/listings.csv` (+70 columns) and `reviews.csv`.
- **Multimodal:** thousands of `.jpg` images in `data/raw/images/` and `.txt` comment files in `data/raw/texts/`.
- **Status:** Immutable. Original files are never modified.

## 2. Silver Zone (Structured Data Warehouse)
The transformation zone where data is filtered, cleaned, and enriched.
- **Location:** `data/processed/`
- **Key Files:**
    - `filtered_elysee.csv`: Only strategic columns for the target neighborhood.
    - `transformed_elysee.csv`: Cleaned data enriched with AI-powered features.
- **Relational Storage:** PostgreSQL table `elysee_listings_silver`.
- **Enrichment:** Includes `standardization_score` and `neighborhood_impact`.

## 3. Data Governance
- **Idempotence:** Every ETL script can be re-run safely.
- **Security:** Credentials managed via `.env`.
- **Documentation:** Specialized READMEs for each pipeline stage (Extract, Profiling, Transform, Load).
