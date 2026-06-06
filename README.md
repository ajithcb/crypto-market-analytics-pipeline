# Automated Crypto Market Pipeline & SQL Analytics Suite

A full-stack Python application that simulates a production data engineering and analytics pipeline. This system automatically ingests financial data from an API, structures it into a relational SQLite database, runs automated analytical business logic reports via SQL, and visualizes market trends on an interactive Streamlit web dashboard.

##  Tech Stack & Tools Used
*   **Backend & Automation**: Python 3, Object-Oriented Programming (OOP)
*   **Data Manipulation**: Pandas, NumPy
*   **Database Management**: SQLite, Relational Database Modeling, SQL Queries
*   **Data Visualization**: Streamlit Web UI, Matplotlib, Seaborn
*   **Network & Integration**: RESTful API Consumption (`requests`), Robust Error Fallbacks

## System Architecture
1.  **Data Extraction Layer (`ingest_data.py`)**: Connects to the live CoinGecko API with data-cleaning logic. Includes a custom mock-data pipeline fallback system to guarantee continuous integration if the API is rate-limited.
2.  **Storage Engine (`database_manager.py`)**: Manages database connectivity and safely appends fresh transactional data feeds to an immutable ledger table.
3.  **Analytics Layer (`analyze_data.py`)**: Runs SQL aggregations, window metrics, and anomaly detection filters to isolate assets experiencing high market volatility.
4.  **Presentation Dashboard (`dashboard.py`)**: A live interactive frontend application that allows stakeholders to filter assets, track live pricing metrics, and audit raw ledger records.

##  How to Run Locally
1. Clone or download this repository.
2. Install dependencies:
   ```bash
   pip install pandas requests streamlit matplotlib seaborn
   ```
3. Run the ingestion pipeline to fetch data and update the SQL database:
   ```bash
   python ingest_data.py
   ```
4. Launch the interactive web analytics dashboard:
   ```bash
   streamlit run dashboard.py
   ```
