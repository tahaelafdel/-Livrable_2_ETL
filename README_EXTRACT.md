# README_EXTRACT.md - Sélection Stratégique pour le Quartier Élysée

Ce document justifie le choix des variables extraites du fichier brut `listings.csv` pour la transition vers la Zone Silver.

## Objectif
Filtrer le "bruit" des 70+ colonnes de la Zone Bronze pour ne conserver que les indicateurs à haut signal qui serviront de base aux hypothèses de politique urbaine pour la Mairie de Paris.

## Cartographie des Variables & Hypothèses

### A. Hypothèse Économique : La Concentration des Biens
**Question :** S'agit-il d'une économie de partage ou d'une industrie hôtelière masquée ?
- `price` : Essentiel pour comprendre le poids économique du secteur.
- `property_type` & `room_type` : Pour distinguer les logements traditionnels des hébergements spécialisés.
- `availability_365` : Pour détecter les biens entièrement dédiés à la location touristique.
- `host_listings_count` & `calculated_host_listings_count` : Indicateurs cruciaux de professionnalisation (multi-propriétaires vs résidents uniques).

### B. Hypothèse Sociale : La Déshumanisation de l'Accueil
**Question :** Le lien social entre l'hôte et le voyageur se perd-il ?
- `host_response_time` & `host_response_rate` : Des réponses rapides et à 100 % sont souvent le signe d'agences de gestion automatisées.
- `host_is_superhost` : Pour analyser la corrélation entre le statut "superhost" et le niveau de standardisation.
- `number_of_reviews` : Donne du contexte sur la fiabilité des données sociales.

### C. Lien Technique & Identification
- `id` : Identifiant unique nécessaire pour lier les données tabulaires aux données multimodales (images dans `data/raw/images/` et textes dans `data/raw/texts/`).

## Logique de Filtrage
- **Quartier :** Le jeu de données est strictement limité au quartier **"Élysée"** (8ème arrondissement de Paris).
- **Résultat :** 2 625 annonces ont été extraites avec succès.
