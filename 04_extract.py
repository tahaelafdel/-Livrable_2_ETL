import pandas as pd
import os

# Configuration
INPUT_FILE = 'data/raw/tabular/listings.csv'
OUTPUT_FILE = 'data/processed/filtered_elysee.csv'
TARGET_NEIGHBOURHOOD = 'Élysée'

# Strategic Selection based on Hypotheses:
# A. Economic (Concentration): price, property_type, room_type, availability_365, calculated_host_listings_count
# B. Social (Dehumanization): host_response_time, host_response_rate, host_is_superhost
# C. Technical Link: id, number_of_reviews (to filter texts later if needed)
COLS_TO_KEEP = [
    'id', 
    'neighbourhood_cleansed', 
    'price', 
    'property_type', 
    'room_type', 
    'availability_365', 
    'host_listings_count',
    'calculated_host_listings_count', 
    'host_response_time', 
    'host_response_rate',
    'host_is_superhost',
    'number_of_reviews'
]

def main():
    print(f"Loading data from {INPUT_FILE}...")
    # Using chunksize if file is very large, but let's try direct load first as listings is usually manageable
    try:
        df = pd.read_csv(INPUT_FILE, usecols=COLS_TO_KEEP, low_memory=False)
    except ValueError as e:
        print(f"Error: Missing columns in the dataset: {e}")
        return

    print(f"Filtering for neighborhood: {TARGET_NEIGHBOURHOOD}...")
    filtered_df = df[df['neighbourhood_cleansed'] == TARGET_NEIGHBOURHOOD].copy()
    
    # Save the result
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    filtered_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Extraction complete. {len(filtered_df)} listings saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()
