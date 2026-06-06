import sqlite3
import smtplib
from email.mime.text import MIMEText

DB_NAME = "crypto_analytics.db"

# EMAIL CONFIGURATION (Optional setup for later)
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password" 

def initialize_database():
    """Creates a local SQLite database file and defines the schema table."""
    print("🗄️ Initializing SQLite database storage...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            coin_id TEXT NOT NULL,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            current_price REAL NOT NULL,
            market_cap REAL,
            total_volume REAL,
            price_change_24h REAL,
            captured_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database connection active. File created: '{DB_NAME}'")

def send_email_alert(coin_id, price, change):
    """Simulates or sends a real email alert when volatility is detected."""
    subject = f"⚠️ CRITICAL ALERT: {coin_id.upper()} Volatility Detected!"
    body = f"The asset {coin_id.upper()} has shifted by {change:.2f}% and is currently trading at ${price:,}!"
    
    print(f"\n📢 [ALERT TRIGGERED] Sending email to {RECEIVER_EMAIL}...")
    print(f"Subject: {subject}\nBody: {body}\n")

    # This block is ready for real email delivery when you provide real credentials
    if "your_email" not in SENDER_EMAIL:
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = RECEIVER_EMAIL
            
            with smtplib.SMTP_SSL('://gmail.com', 465) as server:
                server.login(SENDER_EMAIL, EMAIL_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
            print("✉️ Real email sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send real email: {e}")

def save_dataframe_to_sql(df):
    """Appends data rows directly from a Pandas DataFrame into the SQL table."""
    if df is None or df.empty:
        return
        
    conn = sqlite3.connect(DB_NAME)
    df_to_insert = df.rename(columns={"price_change_percentage_24h": "price_change_24h"})
    df_to_insert.to_sql("market_history", conn, if_exists="append", index=False)
    conn.close()
    print(f"💾 SUCCESS: Appended {len(df)} rows into 'market_history' SQL table.")
    
    # Check each row we just saved for high volatility (> 2% shift)
    for _, row in df.iterrows():
        change_val = row['price_change_percentage_24h']
        if abs(change_val) > 2.0:
            send_email_alert(row['coin_id'], row['current_price'], change_val)
