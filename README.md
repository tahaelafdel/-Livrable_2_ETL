# ImmoVision 360 - Livrable Phase 2 : Pipeline ETL & Enrichissement IA

Ce dépôt contient l'infrastructure logicielle permettant de transformer un **Data Lake** brut (Zone Bronze) en un **Data Warehouse** structuré et enrichi (Zone Silver) pour le quartier de l'Élysée à Paris.

## 🚀 Vision du Projet
L'objectif est de passer de données CSV "muettes" (70+ colonnes) à une base de données **PostgreSQL** "intelligente". Grâce à l'utilisation de l'IA (modèles de Vision et NLP), nous extrayons des indicateurs stratégiques sur la standardisation des logements et l'impact social des locations courte durée.

---

## 🏗️ Architecture du Pipeline (Zone Silver)

Le pipeline est découpé en trois modules autonomes et idempotents :

### 1. Extraction Stratégique (`04_extract.py`)
- **Rôle :** Filtrage du "bruit". On ne conserve que les variables à haut signal.
- **Scope :** Quartier "Élysée" exclusivement.
- **Variables clés :** `price`, `availability_365`, `host_listings_count`, etc.
- [Détails de la stratégie d'extraction](README_EXTRACT.md)

### 2. Nettoyage & Feature Engineering IA (`05_transform.py`)
- **Nettoyage :** Normalisation des taux de réponse, gestion des types de données et imputation des valeurs manquantes (NaN).
- **IA Multimodale :** 
    - **Vision :** Détection du score de standardisation ("Airbnb-style").
    - **NLP :** Analyse des nuisances de voisinage via les commentaires.
- [Détails des transformations et prompts IA](README_TRANSFORM.md)

### 3. Chargement Relationnel (`06_load.py`)
- **Technologie :** SQLAlchemy + Psycopg2.
- **Cible :** Table PostgreSQL `elysee_listings_silver`.
- **Propriété :** Idempotent (peut être relancé sans doublons grâce au mode `replace`).
- [Documentation du Data Warehouse](README_LOAD.md)

---

## 📂 Structure du Dépôt
```text
.
├── scripts/
│   ├── 01_ingestion_images.py   # Phase 1 : Ingestion Images
│   ├── 02_ingestion_texts.py    # Phase 1 : Ingestion Textes
│   ├── 03_sanity_check.py       # Phase 1 : Audit de complétude
│   ├── 04_extract.py            # Phase 2 : Filtrage métier
│   ├── 05_transform.py          # Phase 2 : Nettoyage & IA
│   └── 06_load.py               # Phase 2 : Injection PostgreSQL
├── README_EXTRACT.md            # Justification des features
├── README_DATAPROFILING.md      # Audit de santé des données
├── README_TRANSFORM.md          # Logique d'enrichissement IA
├── README_LOAD.md               # Guide d'intégration BDD
├── README_DATALAKE.md           # Vue d'ensemble Bronze/Silver
└── README.md                    # Ce fichier (Guide Principal)
```

---

## 🛠️ Installation & Utilisation

### Prérequis
- Python 3.x
- Un serveur **PostgreSQL** local ou distant.
- Une clé API **Google AI Studio** (Gemini).

### Setup
1. **Clonage :**
   ```bash
   git clone https://github.com/tahaelafdel/-Livrable_2_ETL.git
   cd -Livrable_2_ETL
   ```
2. **Dépendances :**
   ```bash
   pip install pandas Pillow requests google-generativeai sqlalchemy psycopg2-binary python-dotenv
   ```
3. **Configuration :** Créez un fichier `.env` à la racine :
   ```env
   GEMINI_API_KEY=votre_cle
   DB_USER=votre_user
   DB_PASSWORD=votre_pass
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=immovision_db
   ```

### Exécution du pipeline
```bash
python scripts/04_extract.py
python scripts/05_transform.py
python scripts/06_load.py
```

---

## 📊 État de santé des données (Zone Bronze)
L'audit de santé réalisé lors de la transformation a révélé que la colonne `price` du jeu de données source était vide. L'analyse économique de la Phase 2 se concentre donc sur la **disponibilité** et la **concentration de propriétés** par hôte (jusqu'à 816 annonces pour un seul hôte, signe d'une gestion industrielle massive).
