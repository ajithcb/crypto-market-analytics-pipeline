import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

DB_NAME = "crypto_analytics.db"

# Page Config
st.set_page_config(page_title="Crypto Analytics Dashboard", layout="wide")
st.title("📈 Live Crypto Market Pipeline & Analytics Suite")
st.markdown("This dashboard extracts records dynamically from your local **SQLite relational database**.")

# Connect to DB and pull data
conn = sqlite3.connect(DB_NAME)
df = pd.read_sql_query("SELECT * FROM market_history ORDER BY captured_at DESC", conn)
conn.close()

if df.empty:
    st.warning("Database is currently empty. Run 'python ingest_data.py' a few times to log data!")
else:
    # Sidebar Filters
    st.sidebar.header("Filter Analytics")
    unique_coins = df['coin_id'].unique()
    selected_coin = st.sidebar.selectbox("Select Asset Ticker", unique_coins)

    # Filtered Data
    filtered_df = df[df['coin_id'] == selected_coin].sort_values('captured_at')

    # Metrics Row
    st.subheader(f"📊 Live Market Metrics: {selected_coin.upper()}")
    col1, col2, col3 = st.columns(3)
    
    latest_record = filtered_df.iloc[-1] if not filtered_df.empty else None
    
    if latest_record is not None:
        col1.metric("Current Price", f"${latest_record['current_price']:,}")
        col2.metric("24h Change", f"{latest_record['price_change_24h']:.2f}%")
        col3.metric("Total Records Logged", len(filtered_df))

        # Layout Split: Historical Chart & Data Grid
        left_chart, right_data = st.columns([2, 1])

        with left_chart:
            st.markdown(f"### Price Trend Analysis over Time")
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.lineplot(data=filtered_df, x='captured_at', y='current_price', marker='o', color='#1f77b4', ax=ax)
            plt.xticks(rotation=45)
            ax.set_ylabel("Price ($)")
            ax.set_xlabel("Timestamp")
            st.pyplot(fig)

        with right_data:
            st.markdown("### Raw Database Ledger Entries")
            st.dataframe(filtered_df[['captured_at', 'current_price', 'price_change_24h']], use_container_width=True)
            
    # Full Ledger Overview Section
    st.markdown("---")
    st.subheader("🗄️ Full SQL Database Audit Log View")
    st.dataframe(df, use_container_width=True)
