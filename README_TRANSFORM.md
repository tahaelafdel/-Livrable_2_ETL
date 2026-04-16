# README_TRANSFORM.md - Enrichissement IA & Nettoyage

Ce document décrit la logique de transformation appliquée pour créer le jeu de données de la Zone Silver : `data/processed/transformed_elysee.csv`.

## 1. Règles de Nettoyage & Normalisation
- **Taux de réponse :** La chaîne `host_response_rate` (ex: "95%") a été convertie en float (0.95). Les valeurs manquantes sont imputées par **0** (l'absence de réponse est considérée comme un indicateur négatif).
- **Statut Superhost :** Le drapeau `host_is_superhost` ('t'/'f') a été converti en binaire (1/0). Les valeurs manquantes sont traitées comme **0**.
- **Délai de réponse :** Les valeurs manquantes de `host_response_time` sont remplacées par **"unknown"**.
- **Prix :** Bien que la colonne source soit vide, elle a été forcée en type float pour garantir la cohérence du schéma SQL.

## 2. Enrichissement par IA Multimodale (Gemini)
Le jeu de données a été enrichi de deux nouvelles variables analytiques. Pour cette phase pilote, ces colonnes sont peuplées de scores catégoriels aléatoires (selon les consignes pour préserver les quotas d'API).

### Variable 1 : `standardization_score` (Vision)
- **Concept :** Analyse les images des annonces pour détecter une décoration "industrialisée" par rapport à une décoration "personnelle".
- **Mapping :**
    - `1` : **Industrialisé** (Minimaliste, style hôtel, "Airbnb-style").
    - `0` : **Personnel** (Chaleureux, habité, décoration unique).
    - `-1` : **Autre/Inconnu** (Pas d'image ou photo non intérieure).

### Variable 2 : `neighborhood_impact` (NLP)
- **Concept :** Analyse les commentaires des voyageurs pour détecter les nuisances sociales ou l'intégration communautaire.
- **Mapping :**
    - `1` : **Nuisance** (Plaintes pour bruit, mention de boîtiers à clés, fêtes).
    - `0` : **Neutre**.
    - `-1` : **Impact Positif** (Conseils locaux du propriétaire, interaction humaine forte).

## 3. Détails d'Implémentation
La transformation est orchestrée par le script `05_transform.py`. Il est conçu pour être idempotent et pourra être relancé pour mettre à jour les scores réels une fois l'accès complet aux API activé.
