# README_LOAD.md - Intégration du Data Warehouse

Ce document présente l'étape finale du pipeline ETL : le chargement des données enrichies de la Zone Silver dans une base de données relationnelle PostgreSQL.

## 1. Vue d'Ensemble de la Destination
- **Moteur de base de données :** PostgreSQL
- **Nom de la base :** `immovision_db`
- **Nom de la table :** `elysee_listings_silver`
- **Nombre de lignes chargées :** 2 625

## 2. Pile Technique & Sécurité
- **Chargeur :** Python avec `SQLAlchemy` et `psycopg2`.
- **Méthode :** `to_sql` avec l'option `if_exists="replace"` pour garantir l'idempotence.
- **Gestion des Secrets :** Les identifiants de connexion (utilisateur, mot de passe, hôte, port) sont stockés dans un fichier `.env` et chargés via `python-dotenv`. **Le fichier .env est exclu du contrôle de version pour des raisons de sécurité.**

## 3. Points Forts du Schéma SQL
La table est générée automatiquement à partir du DataFrame Pandas, garantissant un typage strict pour les indicateurs clés :
- `id` : BigInt (Identifiant Unique)
- `price` : Double Precision (Float)
- `host_response_rate` : Double Precision
- `host_is_superhost` : Integer (Binaire)
- `standardization_score` : Integer (-1, 0, 1)
- `neighborhood_impact` : Integer (-1, 0, 1)

## 4. Mode d'Emploi
1. Vérifiez que votre serveur PostgreSQL est démarré.
2. Créez la base de données `immovision_db`.
3. Configurez votre fichier `.env` avec les bons identifiants.
4. Exécutez le script : `python scripts/06_load.py`.
