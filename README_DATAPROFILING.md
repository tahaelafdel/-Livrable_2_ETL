# README_DATAPROFILING.md - Audit de Qualité des Données (Élysée)

Ce document détaille l'état de santé du jeu de données filtré `data/processed/filtered_elysee.csv` (2 625 lignes).

## Audit des Valeurs Manquantes (NaN)
| Colonne | % Manquant | Stratégie |
| :--- | :--- | :--- |
| `id` | 0% | Aucune |
| `price` | **100%** | **CRITIQUE :** Donnée absente de la source. L'hypothèse économique ne peut pas être testée via les prix tabulaires actuels. |
| `host_response_time` | 25.94% | Imputation : "unknown" (indique souvent un hébergement irrégulier ou non professionnel). |
| `host_response_rate` | 25.94% | Imputation : 0%. Logique : Pas de réponse = 0. |
| `host_is_superhost` | 4.91% | Imputation : 0 (false). |
| `host_listings_count` | 0% | Aucune |
| `availability_365` | 0% | Aucune |

## Statistiques & Valeurs Aberrantes
- **Nombre de propriétés par hôte (Calculated Host Listings Count) :**
    - Min : 1
    - Max : 816 (Indicateur clair d'une professionnalisation massive)
    - Médiane : 3
- **Disponibilité (Availability 365) :**
    - Min : 0 jour
    - Max : 365 jours
    - Moyenne : 174 jours
- **Prix (Price) :**
    - Aucune donnée disponible pour détecter des valeurs aberrantes (0€ ou 15 000€).

## Règles de Nettoyage & Normalisation (Milestone 3)
1. **Gestion des Prix :** La colonne étant vide, l'analyse se concentre sur `availability_365` et `host_listings_count`.
2. **Conversion de Types :** 
    - `host_response_rate` : Conversion du texte "95%" en float 0.95.
    - `host_is_superhost` : Conversion des drapeaux "t"/"f" en binaire 1/0.
3. **Imputation Logique :**
    - Remplacement des NaN par des valeurs neutres ou négatives selon le contexte métier (ex: 0 pour le taux de réponse).
埋
