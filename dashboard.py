import subprocess
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import database_manager

st.set_page_config(page_title="Cloud Crypto Analytics Platform", layout="wide")
st.title("📈 Live Crypto Market Pipeline & Analytics Suite")
st.markdown("This interface queries records dynamically from a **Render Cloud PostgreSQL Relational Database Instance**.")

# Automatically runs the ingestion pipeline once every 5 minutes when a user opens the page
@st.cache_data(ttl=300)
def auto_trigger_ingestion_pipeline():
    print("🔄 Web Client access tracking: Refreshing background cloud database table rows...")
    subprocess.run(["python", "ingest_data.py"])

auto_trigger_ingestion_pipeline()

# Load fresh information from PostgreSQL database storage tables
try:
    conn = database_manager.get_connection()
    df = pd.read_sql_query("SELECT * FROM market_history ORDER BY captured_at DESC", conn)
    conn.close()
except Exception as e:
    st.error(f"❌ Failed to extract records from cloud database service: {e}")
    df = pd.DataFrame()

if df.empty:
    st.warning("⚠️ Database ledger is empty. Wait a moment for background workers to complete data ingestion updates!")
else:
    # Sidebar Filters
    st.sidebar.header("Asset Selection Filter")
    unique_assets = df['coin_id'].unique()
    selected_asset = st.sidebar.selectbox("Select Target Cryptocurrency", unique_assets)

    # Filter metrics based on choices
    filtered_df = df[df['coin_id'] == selected_asset].sort_values('captured_at')

    # Visual Display Metrics Grid Layout Panel
    st.subheader(f"📊 Live Market Metrics: {selected_asset.upper()}")
    col1, col2, col3 = st.columns(3)
    
    if not filtered_df.empty:
        latest_tick = filtered_df.iloc[-1]
        col1.metric("Current Market Valuation", f"${float(latest_tick['current_price']):,}")
        col2.metric("24h Price Delta Variance", f"{float(latest_tick['price_change_24h'] clay):.2f}%")
        col3.metric("Total Datapoints Tracked", len(filtered_df))

        # Charts and Data Visualization Grid Layouts
        chart_col, table_col = st.columns(2)
        
        with chart_col:
            st.markdown("### Structural Asset Price Trajectory Over Time")
            fig, ax = plt.subplots(figsize=(10, 4.5))
            sns.lineplot(data=filtered_df, x='captured_at', y='current_price', marker='o', linewidth=2.5, color='#00cc96', ax=ax)
            plt.xticks(rotation=35)
            ax.set_ylabel("Price Index (USD)")
            ax.set_xlabel("Server Capture Timeline Frame")
            st.pyplot(fig)
            
        with table_col:
            st.markdown("### Raw Sub-Ledger Transaction Entries")
            st.dataframe(filtered_df[['captured_at', 'current_price', 'price_change_24h']].sort_values('captured_at', ascending=False), use_container_width=True)

    # Base Audit Database File Log Views
    st.markdown("---")
    st.subheader("🗄️ Global System Relational Audit Logs")
    st.dataframe(df, use_container_width=True)
