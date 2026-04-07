import os
import csv

def main():
    target_neighbourhood = 'Élysée'
    listings_file = 'listings.csv'
    reviews_file = 'reviews.csv'
    images_dir = os.path.join('data', 'raw', 'images')
    texts_dir = os.path.join('data', 'raw', 'texts')

    print(f"=== Bilan de Santé de la Donnée (Sanity Check) ===")
    print(f"Périmètre cible : {target_neighbourhood}\n")

    # 1. Analyse théorique à partir des sources CSV
    target_listing_ids = set()
    expected_images_ids = set()
    
    if not os.path.exists(listings_file):
        print(f"Erreur : Fichier {listings_file} introuvable.")
        return

    # A. Comptage théorique des images (IDs du périmètre avec une URL d'image valide)
    try:
        with open(listings_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                neighbourhood = row.get('neighbourhood_cleansed', '')
                if target_neighbourhood in neighbourhood:
                    listing_id = row.get('id')
                    picture_url = row.get('picture_url')
                    target_listing_ids.add(listing_id)
                    
                    if picture_url and picture_url.strip():
                        expected_images_ids.add(listing_id)
    except Exception as e:
        print(f"Erreur lors de la lecture de {listings_file} : {e}")
        return

    # B. Comptage théorique des textes (IDs du périmètre ayant au moins un commentaire)
    expected_texts_ids = set()
    if os.path.exists(reviews_file):
        try:
            with open(reviews_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    listing_id = row.get('listing_id')
                    comment = row.get('comments')
                    if listing_id in target_listing_ids and comment and str(comment).strip():
                        expected_texts_ids.add(listing_id)
        except Exception as e:
            print(f"Erreur lors de la lecture de {reviews_file} : {e}")

    print(f"-> {len(target_listing_ids)} annonces de référence trouvées pour le quartier {target_neighbourhood}.")

    # 2. Comptage physique sur le disque
    present_images_ids = set()
    if os.path.exists(images_dir):
        present_images_ids = {f.split('.')[0] for f in os.listdir(images_dir) if f.endswith('.jpg')}

    present_texts_ids = set()
    empty_texts_ids = set()
    if os.path.exists(texts_dir):
        for f_name in os.listdir(texts_dir):
            if f_name.endswith('.txt'):
                file_id = f_name.split('.')[0]
                present_texts_ids.add(file_id)
                # Vérification de fichier anormalement vide ou trop petit (ex: juste l'en-tête)
                file_path = os.path.join(texts_dir, f_name)
                if os.path.getsize(file_path) < 50: # Moins de 50 octets = potentiellement juste le titre
                    empty_texts_ids.add(file_id)

    # 3. Calculs des écarts (Jointures)
    missing_images = expected_images_ids - present_images_ids
    completion_images = (len(present_images_ids) / len(expected_images_ids) * 100) if expected_images_ids else 0.0

    missing_texts = expected_texts_ids - present_texts_ids
    completion_texts = (len(present_texts_ids) / len(expected_texts_ids) * 100) if expected_texts_ids else 0.0

    # 4. Cohérence croisée
    images_without_texts = present_images_ids - present_texts_ids
    texts_without_images = present_texts_ids - present_images_ids

    # 5. Génération du Rapport
    print("\n--- [ Images (.jpg) ] ---")
    print(f"Attendues théoriquement : {len(expected_images_ids)}")
    print(f"Présentes physiquement  : {len(present_images_ids)}")
    print(f"Taux de complétion      : {completion_images:.2f}%")
    if missing_images:
        print(f"Images manquantes (orphelines) : {len(missing_images)}")
        print(f"-> 5 premiers IDs sans .jpg : {list(missing_images)[:5]}")
    
    print("\n--- [ Textes (.txt) ] ---")
    print(f"Attendus théoriquement  : {len(expected_texts_ids)} (annonces avec commentaires)")
    print(f"Présents physiquement   : {len(present_texts_ids)}")
    print(f"Taux de complétion      : {completion_texts:.2f}%")
    if missing_texts:
        print(f"Textes manquants (orphelins) : {len(missing_texts)}")
        print(f"-> 5 premiers IDs sans .txt : {list(missing_texts)[:5]}")
    if empty_texts_ids:
        print(f"Attention : {len(empty_texts_ids)} fichiers textes semblent anormalement vides/petits.")
        print(f"-> 5 premiers IDs concernés : {list(empty_texts_ids)[:5]}")

    print("\n--- [ Cohérence Croisée (Multimodale) ] ---")
    print(f"Annonces AVEC image mais SANS texte (ex: pas d'avis) : {len(images_without_texts)}")
    if images_without_texts:
         print(f"-> Exemples : {list(images_without_texts)[:5]}")
    
    print(f"Annonces AVEC texte mais SANS image (ex: erreur DL) : {len(texts_without_images)}")
    if texts_without_images:
         print(f"-> Exemples : {list(texts_without_images)[:5]}")

    print("\n=== Fin du Sanity Check ===")

if __name__ == "__main__":
    main()
