# Phase 2: Data Transformation & Silver Zone Implementation

This plan outlines the transition from raw data (Bronze Zone) to a structured, AI-enriched PostgreSQL Data Warehouse (Silver Zone).

## Strategic Objectives
- **Structural Mutation:** Transform ~70 columns of raw CSV data into a lean, queryable relational schema.
- **Multimodal Enrichment:** Use Gemini AI to derive new features from images (Standardization Score) and text (Sentiment/Nuisance analysis).
- **Industrial Reliability:** Implement an idempotent, documented, and specialized ETL pipeline.

---

## Milestones

### Milestone 1: Strategic Extraction (The Filter)
**Goal:** Reduce noise by selecting only high-signal features relevant to urban policy hypotheses.
- [ ] **Research:** Identify key columns for Economic (concentration) and Social (dehumanization) hypotheses.
- [ ] **Implementation (`04_extract.py`):**
    - Filter raw `listings.csv` for the "Élysée" neighborhood.
    - Select specific columns (`price`, `host_listings_count`, `availability_365`, etc.).
    - Save to `data/processed/filtered_elysee.csv`.
- [ ] **Documentation:** Create `README_EXTRACT.md` justifying feature selection.

### Milestone 2: Data Profiling & Diagnostic
**Goal:** Understand data health before automation.
- [ ] **Audit:** Analyze `filtered_elysee.csv` for:
    - Missing values (NaN) percentages.
    - Outliers (e.g., 0€ or 15,000€ prices).
    - Data type inconsistencies (e.g., "$120.00" string vs float).
- [ ] **Documentation:** Create `README_DATAPROFILING.md` detailing findings and cleaning strategies (Imputation vs. Drop).

### Milestone 3: AI-Powered Transformation (The Alchemy)
**Goal:** Enrich the dataset with multimodal intelligence.
- [ ] **Implementation (`05_transform.py`):**
    - **Step A (Cleaning):** Apply rules from Milestone 2 (Float conversion, NaN handling).
    - **Step B (Image Inference):** Integrate Gemini 2.5 Flash to generate `Standardization_Score` from `data/raw/images/`.
    - **Step C (Text Inference):** (TBD from full instructions) Analyze sentiment/nuisances from `data/raw/texts/`.
- [ ] **Output:** Save enriched data to `data/processed/transformed_elysee.csv`.
- [ ] **Documentation:** Create `README_TRANSFORM.md` describing AI prompts and mapping logic.

### Milestone 4: Relational Loading (The Anchor)
**Goal:** Persist data into a production-ready PostgreSQL environment.
- [ ] **Setup:** Configure `.env` with database credentials and update `.gitignore`.
- [ ] **Implementation (`06_load.py`):**
    - Design a strictly typed SQL schema.
    - Implement idempotent loading using SQLAlchemy (replace/append logic).
- [ ] **Validation:** Run cross-check queries to verify data integrity in PostgreSQL.
- [ ] **Documentation:** Create `README_LOAD.md` with schema definitions and loading protocols.

### Milestone 5: Final Delivery & Documentation
- [ ] **Integration:** Ensure all scripts run sequentially as a cohesive pipeline.
- [ ] **Reporting:** Update main `README.md` with the Phase 2 overview and results.
- [ ] **Cleanup:** Ensure the `data/processed/` directory is correctly structured.

---

## Technical Stack
- **Data Handling:** Pandas (Chunk-based processing).
- **AI/ML:** Google AI Studio (Gemini 2.5 Flash).
- **Database:** PostgreSQL + SQLAlchemy.
- **Environment:** Python 3.x, `.env` for secrets management.
