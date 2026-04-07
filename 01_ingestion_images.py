import os
import csv
import concurrent.futures
import requests
from PIL import Image
from io import BytesIO

# Configuration
CSV_FILE = 'listings.csv'
OUTPUT_DIR = os.path.join('data', 'raw', 'images')
TARGET_NEIGHBOURHOOD = 'Élysée'
MAX_WORKERS = 10  # Number of parallel downloads (Adjust based on connection)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (DataCollectionProject / Academic-Educational Use)'
}

def download_and_process_image(row):
    """Downloads, resizes, and saves a single image."""
    listing_id = row.get('id')
    picture_url = row.get('picture_url')
    
    if not listing_id or not picture_url:
        return "skipped"

    output_path = os.path.join(OUTPUT_DIR, f"{listing_id}.jpg")
    
    # Idempotence check
    if os.path.exists(output_path):
        return "exists"

    try:
        # Download
        response = requests.get(picture_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # Process Image
        img = Image.open(BytesIO(response.content))
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img = img.resize((320, 320))
        img.save(output_path, 'JPEG')
        return "success"
        
    except Exception as e:
        return f"error: {str(e)}"

def main():
    # Setup directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        return

    # 1. Load and Filter Data
    tasks = []
    print(f"=== Scanning CSV for neighbourhood: {TARGET_NEIGHBOURHOOD} ===")
    with open(CSV_FILE, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            neighbourhood = row.get('neighbourhood_cleansed', '')
            if TARGET_NEIGHBOURHOOD in neighbourhood:
                tasks.append(row)

    print(f"Found {len(tasks)} target images. Starting parallel ingestion with {MAX_WORKERS} workers...")

    # 2. Parallel Execution
    stats = {"success": 0, "exists": 0, "error": 0, "skipped": 0}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Map tasks to the download function
        future_to_id = {executor.submit(download_and_process_image, row): row.get('id') for row in tasks}
        
        for future in concurrent.futures.as_completed(future_to_id):
            result = future.result()
            if result == "success":
                stats["success"] += 1
            elif result == "exists":
                stats["exists"] += 1
            elif result.startswith("error"):
                stats["error"] += 1
                # print(f"ID {future_to_id[future]} {result}") # Uncomment to see specific errors
            else:
                stats["skipped"] += 1

    print("\n=== Bilan de l'ingestion (Optimisée) ===")
    print(f"Images ciblées       : {len(tasks)}")
    print(f"Images téléchargées  : {stats['success']}")
    print(f"Images ignorées      : {stats['exists']} (déjà existantes)")
    print(f"Erreurs rencontrées  : {stats['error']}")

if __name__ == "__main__":
    main()
