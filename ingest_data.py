import random
from datetime import datetime, timezone
import pandas as pd
import requests

COINS = "bitcoin,ethereum,solana,cardano"

URL = "https://coingecko.com" + COINS



def fetch_live_market_data():
    """Fetches live cryptocurrency data or generates mock data if the API fails."""
    try:
        print("📡 Connecting to CoinGecko API...")
        response = requests.get(URL, timeout=10)

        print(f"📊 API Response Status Code: {response.status_code}")

        if response.status_code == 429:
            print("⚠️ Rate limit reached! Switching to mock data generation...")
            return generate_mock_data()

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"❌ Connection error details: {e}")
        print("⚠️ Switching to mock data generation so you can keep working...")
        return generate_mock_data()


def generate_mock_data():
    """Generates fake market data so your pipeline never freezes during development."""
    return [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": random.randint(60000, 65000),
            "market_cap": 1200000000,
            "total_volume": 25000000,
            "price_change_percentage_24h": random.uniform(-5.0, 5.0),
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "current_price": random.randint(3000, 3500),
            "market_cap": 400000000,
            "total_volume": 15000000,
            "price_change_percentage_24h": random.uniform(-5.0, 5.0),
        },
        {
            "id": "solana",
            "symbol": "sol",
            "name": "Solana",
            "current_price": random.randint(130, 160),
            "market_cap": 65000000,
            "total_volume": 3000000,
            "price_change_percentage_24h": random.uniform(-8.0, 8.0),
        },
    ]


def clean_and_process_data(raw_data):
    """Transforms data into a dataframe and standardizes columns."""
    if not raw_data:
        print("❌ No raw data received to process.")
        return None

    df = pd.DataFrame(raw_data)
    columns_to_keep = [
        "id",
        "symbol",
        "name",
        "current_price",
        "market_cap",
        "total_volume",
        "price_change_percentage_24h",
    ]
    df = df[columns_to_keep]
    df = df.rename(columns={"id": "coin_id"})

    
    df["captured_at"] = (
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    )
    return df

if __name__ == "__main__":
    print("🚀 Running updated pipeline...")
    
    
    import database_manager
    
   
    database_manager.initialize_database()

    
    raw_market_data = fetch_live_market_data()
    
    
    cleaned_df = clean_and_process_data(raw_market_data)

    if cleaned_df is not None:
        print("\n✅ DataFrame successfully created inside memory!")
        
      
        cleaned_df.to_csv("live_market_data.csv", index=False)
        
    
        database_manager.save_dataframe_to_sql(cleaned_df)
    else:
        print("❌ Pipeline failed. Dataframe was empty.")
