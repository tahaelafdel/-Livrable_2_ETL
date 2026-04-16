import pandas as pd
import os
import random
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configuration
INPUT_FILE = 'data/processed/filtered_elysee.csv'
OUTPUT_FILE = 'data/processed/transformed_elysee.csv'
IMAGE_DIR = 'data/raw/images'
TEXT_DIR = 'data/raw/texts'

def get_standardization_score_real(listing_id):
    """Real inference using Gemini for a single image (demo)."""
    if not api_key:
        return None
    
    img_path = os.path.join(IMAGE_DIR, f"{listing_id}.jpg")
    if not os.path.exists(img_path):
        return -1
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash") # Using available stable model
        img = Image.open(img_path)
        
        prompt = """
        Analyse cette image et classifie-la strictement dans l'une de ces catégories :
        - 'Appartement industrialisé' (Déco minimaliste, style catalogue, standardisé, froid)
        - 'Appartement personnel' (Objets de vie, livres, décoration hétéroclite, chaleureux)
        - 'Autre' (Si l'image ne montre pas l'intérieur d'un logement)

        Réponds uniquement par le nom de la catégorie.
        """
        response = model.generate_content([prompt, img])
        res_text = response.text.strip()
        
        if 'industrialisé' in res_text: return 1
        if 'personnel' in res_text: return 0
        return -1
    except Exception as e:
        print(f"Inference error for {listing_id}: {e}")
        return -1

def main():
    print(f"Loading filtered data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    # --- STEP A: Cleaning & Normalization ---
    print("Cleaning and normalizing data...")
    
    # 1. host_response_rate: "95%" -> 0.95
    df['host_response_rate'] = df['host_response_rate'].str.replace('%', '').astype(float) / 100.0
    df['host_response_rate'] = df['host_response_rate'].fillna(0) # Logic: No response = 0
    
    # 2. host_is_superhost: 't'/'f' -> 1/0
    df['host_is_superhost'] = df['host_is_superhost'].map({'t': 1, 'f': 0}).fillna(0).astype(int)
    
    # 3. host_response_time: Fill NaN
    df['host_response_time'] = df['host_response_time'].fillna('unknown')
    
    # 4. price: Since it's 100% NaN in source, we ensure it's float (even if empty)
    df['price'] = df['price'].astype(float)

    # --- STEP B: AI Enrichment (Mocked for scale, Real for sample) ---
    print("Enriching with AI features (Vision & NLP)...")
    
    # Mocking for all as per instructions to save quotas
    # standardization_score: 1 (Industrial), 0 (Personal), -1 (Other/Unknown)
    # neighborhood_impact: 1 (Nuisance), 0 (Neutral), -1 (Positive/Unknown)
    
    choices = [1, 0, -1]
    df['standardization_score'] = [random.choice(choices) for _ in range(len(df))]
    df['neighborhood_impact'] = [random.choice(choices) for _ in range(len(df))]

    # Demo of real call for the first listing with an image
    sample_id = None
    for lid in df['id']:
        if os.path.exists(os.path.join(IMAGE_DIR, f"{lid}.jpg")):
            sample_id = lid
            break
    
    if sample_id:
        print(f"Performing real AI demo for listing {sample_id}...")
        real_score = get_standardization_score_real(sample_id)
        df.loc[df['id'] == sample_id, 'standardization_score'] = real_score
        print(f"Real Score for {sample_id}: {real_score}")

    # --- STEP C: Save ---
    print(f"Saving transformed data to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    print("Transformation complete.")

if __name__ == "__main__":
    main()
