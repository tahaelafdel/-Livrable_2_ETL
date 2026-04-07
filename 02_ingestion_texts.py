import os
import pandas as pd
import re
import concurrent.futures
from collections import defaultdict

# Configuration
LISTINGS_FILE = 'listings.csv'
REVIEWS_FILE = 'reviews.csv'
OUTPUT_DIR = os.path.join('data', 'raw', 'texts')
TARGET_NEIGHBOURHOOD = 'Élysée'
MAX_WORKERS = 8  # For parallel file writing

def clean_text(text):
    """Cleans HTML tags and normalizes whitespace."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<br\s*/?>', ' ', text, flags=re.IGNORECASE)
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def save_comments_to_file(listing_id, comments):
    """Writes comments to a .txt file."""
    output_path = os.path.join(OUTPUT_DIR, f"{listing_id}.txt")
    try:
        with open(output_path, mode='w', encoding='utf-8') as f:
            f.write(f"Commentaires pour l'annonce {listing_id}:\n\n")
            for comment in comments:
                f.write(f"- {comment}\n")
        return True
    except Exception:
        return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(LISTINGS_FILE) or not os.path.exists(REVIEWS_FILE):
        print("Error: Source CSV files missing.")
        return

    # 1. Faster Filtering with Pandas
    print(f"=== Step 1: Filtering listings for {TARGET_NEIGHBOURHOOD} ===")
    df_listings = pd.read_csv(LISTINGS_FILE, usecols=['id', 'neighbourhood_cleansed'], low_memory=False)
    # Ensure IDs are strings for consistent mapping
    df_listings['id'] = df_listings['id'].astype(str)
    
    target_ids = set(df_listings[df_listings['neighbourhood_cleansed'].str.contains(TARGET_NEIGHBOURHOOD, na=False)]['id'])
    print(f"-> Found {len(target_ids)} target listings.")

    # 2. Optimized Review Extraction
    print("\n=== Step 2: Extracting reviews (Fast Ingestion) ===")
    reviews_by_listing = defaultdict(list)
    
    # Process reviews in chunks to handle large files efficiently
    chunk_size = 100000
    for chunk in pd.read_csv(REVIEWS_FILE, usecols=['listing_id', 'comments'], chunksize=chunk_size, low_memory=False):
        chunk['listing_id'] = chunk['listing_id'].astype(str)
        
        # Filter reviews for our target listings
        filtered_chunk = chunk[chunk['listing_id'].isin(target_ids)]
        
        for _, row in filtered_chunk.iterrows():
            cleaned = clean_text(row['comments'])
            if cleaned:
                reviews_by_listing[row['listing_id']].append(cleaned)

    print(f"-> Collected comments for {len(reviews_by_listing)} listings.")

    # 3. Parallel File Writing
    print("\n=== Step 3: Writing text files in parallel ===")
    success_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(save_comments_to_file, lid, comms): lid for lid, comms in reviews_by_listing.items()}
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1

    print(f"\n=== Bilan Final ===")
    print(f"Fichiers TXT créés : {success_count}")

if __name__ == "__main__":
    main()
