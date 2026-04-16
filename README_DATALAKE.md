# README_DATALAKE.md - Architecture de l'Infrastructure de Données

Ce projet suit une architecture en couches pour transformer la donnée brute en intelligence décisionnelle.

## 1. Zone Bronze (Data Lake Brut)
C'est la zone de réception de toutes les données brutes, non formatées.
- **Tabulaire :** `data/raw/tabular/listings.csv` (+70 colonnes) et `reviews.csv`.
- **Multimodal :** Des milliers d'images `.jpg` dans `data/raw/images/` et des fichiers de commentaires `.txt` dans `data/raw/texts/`.
- **Statut :** Immuable. Les fichiers originaux ne sont jamais modifiés.

## 2. Zone Silver (Data Warehouse Structuré)
La zone de transformation où la donnée est filtrée, nettoyée et enrichie.
- **Emplacement :** `data/processed/`
- **Fichiers Clés :**
    - `filtered_elysee.csv` : Uniquement les colonnes stratégiques pour le quartier cible.
    - `transformed_elysee.csv` : Données nettoyées et enrichies par les scores de l'IA.
- **Stockage Relationnel :** Table PostgreSQL `elysee_listings_silver`.
- **Enrichissement :** Inclut les colonnes `standardization_score` (Vision) et `neighborhood_impact` (NLP).

## 3. Gouvernance de la Donnée
- **Idempotence :** Chaque script ETL peut être relancé en toute sécurité sans corrompre la base.
- **Sécurité :** Gestion des accès via un fichier `.env`.
- **Documentation :** Des README spécialisés pour chaque étape du pipeline (Extraction, Profiling, Transformation, Chargement).
