import pandas as pd
import database_manager

def run_cloud_analytical_queries():
    """Extracts target records dynamically from cloud tables to generate evaluation insights."""
    try:
        conn = database_manager.get_connection()
        
        print("\n==================================================")
        print("📈 COMPONENT REPORT 1: Database Asset Metrics Summary")
        print("==================================================")
        query1 = """
            SELECT coin_id, COUNT(*) as tracked_ticks, AVG(current_price)::numeric(10,2) as avg_price 
            FROM market_history 
            GROUP BY coin_id;
        """
        df1 = pd.read_sql_query(query1, conn)
        print(df1.to_string(index=False))

        print("\n==================================================")
        print("⚠️ COMPONENT REPORT 2: Detected Volatility Flags (> 2%)")
        print("==================================================")
        query2 = """
            SELECT coin_id, current_price, price_change_24h::numeric(10,2), captured_at 
            FROM market_history 
            WHERE ABS(price_change_24h) > 2.0 
            ORDER BY captured_at DESC;
        """
        df2 = pd.read_sql_query(query2, conn)
        
        if df2.empty:
            print("System Audit: No extreme asset variance movements found in active table traces.")
        else:
            print(df2.to_string(index=False))
            
        conn.close()
    except Exception as e:
        print(f"❌ Analysis Execution Failure: {e}")

if __name__ == "__main__":
    print("📊 Triggering PostgreSQL Data Verification Suite...")
    run_cloud_analytical_queries()
