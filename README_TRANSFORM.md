# README_TRANSFORM.md - AI Enrichment & Cleaning

This document describes the transformation logic applied to create the Silver Zone dataset: `data/processed/transformed_elysee.csv`.

## 1. Cleaning & Normalization Rules
- **Response Rate:** The `host_response_rate` string (e.g., "95%") was converted to a float (0.95). Missing values were imputed with **0** (assuming no response is a negative indicator).
- **Superhost Status:** The `host_is_superhost` flag ('t'/'f') was converted to binary (1/0). Missing values were treated as **0**.
- **Response Time:** Missing `host_response_time` values were filled with **"unknown"**.
- **Price:** Although the source column was empty, it was cast to float to maintain schema consistency.

## 2. Multimodal AI Enrichment (Gemini)
The dataset was enriched with two new analytical features. Due to API quota constraints for the pilot phase, these columns are currently populated with randomized categorical scores as per instructions.

### Feature 1: `standardization_score` (Vision)
- **Concept:** Analyzes listing images to detect "industrialized" vs. "personal" decor.
- **Mapping:**
    - `1`: **Industrialized** (Minimalist, hotel-style, "Airbnb-style").
    - `0`: **Personal** (Warm, lived-in, unique decor).
    - `-1`: **Other/Unknown** (No image or non-interior photo).

### Feature 2: `neighborhood_impact` (NLP)
- **Concept:** Analyzes guest comments to detect social nuisances or community integration.
- **Mapping:**
    - `1`: **Nuisance** (Noise complaints, automated lockbox mentions, party issues).
    - `0`: **Neutral**.
    - `-1`: **Positive Impact** (Mention of local tips, interaction with host).

## 3. Implementation Details
The transformation is handled by `scripts/05_transform.py`, which is designed to be idempotent and can be re-run to update scores once full API access is established.
