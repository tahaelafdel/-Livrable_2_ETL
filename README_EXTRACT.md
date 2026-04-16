# README_EXTRACT.md - Strategic Selection for Élysée Neighborhood

This document justifies the selection of features from the raw `listings.csv` for the transition to the Silver Zone.

## Objective
To filter out the noise from the 70+ columns of the Bronze Zone and retain only the high-signal features that will serve as the foundation for urban policy hypotheses for the Mayor of Paris.

## Selected Features & Hypotheses Mapping

### A. Economic Hypothesis: The Concentration of Wealth
**Question:** Is this a sharing economy or a masked hotel industry?
- `price`: Essential for understanding the economic weight of the sector.
- `property_type` & `room_type`: To distinguish between traditional homes and specialized accommodation.
- `availability_365`: To detect properties that are fully dedicated to tourist rentals.
- `host_listings_count` & `calculated_host_listings_count`: Crucial indicators of professionalization (multi-owners vs. single-property residents).

### B. Social Hypothesis: The Dehumanization of Hospitality
**Question:** Is the social bond between host and guest being lost?
- `host_response_time` & `host_response_rate`: Fast, 100% automated responses are often a sign of professional management agencies.
- `host_is_superhost`: To analyze the correlation between "superhost" status and the level of standardization.
- `number_of_reviews`: Provides context for the reliability of social data.

### C. Technical & Identification
- `id`: Unique identifier required to link tabular data with multimodal data (images in `data/raw/images/` and texts in `data/raw/texts/`).

## Filtering Logic
- **Neighborhood:** The dataset is strictly limited to the **"Élysée"** neighborhood (Paris 8th arrondissement).
- **Result:** 2,625 listings were successfully extracted.
