import pandas as pd
import numpy as np
from datasets import load_dataset
from database import SessionLocal, Restaurant, init_db

def clean_rate(rate_str):
    if pd.isna(rate_str) or rate_str == 'NEW' or rate_str == '-' or rate_str is None:
        return None
    try:
        return float(str(rate_str).split('/')[0].strip())
    except Exception:
        return None

def clean_cost(cost_str):
    if pd.isna(cost_str) or cost_str is None:
        return None
    try:
        # Remove commas if present
        cost_str = str(cost_str).replace(',', '')
        return int(cost_str)
    except Exception:
        return None

def get_budget_tier(cost):
    if cost is None or pd.isna(cost):
        return 'Unknown'
    if cost < 500:
        return 'Low'
    elif cost <= 1000:
        return 'Mid'
    else:
        return 'High'

def ingest_data():
    print("Initializing database...")
    init_db()
    
    print("Fetching dataset from Hugging Face...")
    dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation")
    df = pd.DataFrame(dataset['train'])
    
    print("Cleaning data...")
    # Drop completely duplicate names/locations if any
    df = df.drop_duplicates(subset=['name', 'location'], keep='first')
    
    # Process columns
    df['clean_rate'] = df['rate'].apply(clean_rate)
    df['clean_cost'] = df['approx_cost(for two people)'].apply(clean_cost)
    df['budget_tier'] = df['clean_cost'].apply(get_budget_tier)
    
    # Fill NAs in text columns
    df['cuisines'] = df['cuisines'].fillna('Unknown')
    df['location'] = df['location'].fillna('Unknown')
    df['dish_liked'] = df['dish_liked'].fillna('')
    df['rest_type'] = df['rest_type'].fillna('')
    
    # Create features for soft matching (combining rest_type and dish_liked)
    df['features'] = df.apply(lambda row: f"Type: {row['rest_type']} | Liked: {row['dish_liked']}", axis=1)
    
    print(f"Total unique records to insert: {len(df)}")
    
    print("Inserting data into the database...")
    session = SessionLocal()
    
    # Empty existing table for idempotency
    session.query(Restaurant).delete()
    session.commit()
    
    # Process in chunks to avoid memory issues
    chunk_size = 5000
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start+chunk_size]
        restaurants = []
        for _, row in chunk.iterrows():
            r = Restaurant(
                name=str(row['name']),
                location=str(row['location']),
                budget_tier=row['budget_tier'],
                rating=row['clean_rate'],
                cost_for_two=row['clean_cost'],
                cuisines=str(row['cuisines']),
                features=str(row['features'])
            )
            restaurants.append(r)
        
        session.add_all(restaurants)
        session.commit()
        print(f"Inserted {start + len(chunk)} / {len(df)} records.")
        
    session.close()
    print("Data ingestion complete.")

if __name__ == "__main__":
    ingest_data()
