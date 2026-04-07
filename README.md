# Création du Data Lake pour ImmoVision 360 (Optimisé Cloud)

## 1. Contexte et Objectifs
Ce projet a pour objectif la mise en place d'un Data Lake robuste en vue d'alimenter la Phase 2 du projet **ImmoVision 360** (analyse par IA multimodale : Vision et NLP). 

Les données proviennent initialement de catalogues Open Data (Inside Airbnb). Afin d'optimiser le stockage et la pertinence de l'analyse, l'ingestion a été ciblée sur un périmètre géographique strict (quartier "Élysée"). Les images ont été aspirées, redimensionnées et standardisées, tandis que les avis textuels ont été nettoyés et agrégés par annonce, constituant ainsi un corpus de qualité, prêt pour l'analyse algorithmique.

---

## 2. Optimisation des Performances (Cloud & Parallélisme)
Initialement, le traitement séquentiel (une image à la fois avec délai de courtoisie) était trop lent pour un usage industriel. Le pipeline a été migré vers **Google Colab** pour bénéficier de la puissance du Cloud et de la bande passante réseau de Google.

**Améliorations majeures :**
- **Exécution sur Google Colab :** Utilisation d'instances distantes pour accélérer les téléchargements et le traitement CPU.
- **Multithreading (Parallélisme) :** Refactorisation de `01_ingestion_images.py` avec `ThreadPoolExecutor` (10 workers) pour télécharger plusieurs images simultanément.
- **Optimisation Pandas :** Refactorisation de `02_ingestion_texts.py` utilisant `pandas` pour une lecture par "chunks" de 100 000 lignes, permettant de traiter des fichiers CSV massifs sans saturer la mémoire vive.

---

## 3. Structure du Répertoire
```text
.
├── 00_data.ipynb                 # Notebook d'exploration initiale
├── 01_ingestion_images.py        # Script optimisé (Parallel Ingestion)
├── 02_ingestion_texts.py         # Script optimisé (Pandas + Parallel Writing)
├── 03_sanity_check.py            # Script d'audit croisé (Sanity Check)
├── listings.csv                  # Référentiel source des annonces
├── reviews.csv                   # Base source des commentaires
├── README.md                     # Documentation et rapport de livraison (ce fichier)
└── data/                         # Racine du Data Lake
    └── raw/
        ├── images/               # Images ingérées (320x320 px, JPEG)
        └── texts/                # Corpus NLP ingéré (.txt)
```

---

## 4. Notice d'Exécution (Mode Cloud Colab)

**Étape 1 : Connexion Drive**
Montez votre Google Drive dans un notebook Colab :
```python
from google.colab import drive
drive.mount('/content/drive')
os.chdir('/content/drive/MyDrive/Data Collection Project')
```

**Étape 2 : Installation des Dépendances**
```bash
!pip install pandas Pillow requests
```

**Étape 3 : Lancement du Pipeline**
```bash
!python 01_ingestion_images.py
!python 02_ingestion_texts.py
!python 03_sanity_check.py
```

---

## 5. Audit des Données (Résultats Finaux)

Suite à l'exécution optimisée sur Google Colab, voici le bilan de santé du Data Lake pour le quartier **Élysée** :

- **Périmètre cible** : Élysée
- **Nombre total d'annonces de référence** : 2625

**Bilan Images (.jpg) :**
- Images attendues théoriquement : 2625
- Images physiquement présentes : **2490**
- Taux de complétion : **94.86%**
- Pertes (erreurs DL / liens morts) : 135 (5.14%)

**Bilan Textes (.txt) :**
- Fichiers textes attendus (annonces avec commentaires) : 1965
- Fichiers textes physiquement présents : **1965**
- Taux de complétion : **100.00%**
- Note : 3 fichiers textes semblent anormalement vides/petits et nécessiteront une vérification manuelle.

**Cohérence Croisée (Multimodale) :**
- Annonces avec image mais SANS texte (ex: pas d'avis voyageurs) : 622
- Annonces avec texte mais SANS image (ex: erreur de téléchargement) : 97

---

## 6. Analyse des Pertes (Data Loss Analysis)

La déperdition de ~5% sur les images est structurelle et s'explique par :
1. **Liens morts (404/410) :** Annonces supprimées ou photos purgées du CDN Airbnb depuis le dernier export Open Data.
2. **Timeouts réseau :** Latence serveurs distants dépassant les 10s de sécurité.
3. **Fichiers corrompus :** Encodages exotiques non supportés par Pillow lors de la conversion RGB.

L'écart entre le nombre d'images (2490) et de textes (1965) est normal : de nombreuses annonces n'ont tout simplement pas encore reçu d'avis clients, bien que leur photo soit valide.
