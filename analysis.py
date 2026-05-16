import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv

# Load security environment variables
load_dotenv()

def fetch_data_from_db() -> pd.DataFrame:
    """Connects to MySQL and extracts all table data into a Pandas DataFrame."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="nutrition_db"
    )
    
    # The analytical SQL query
    query = "SELECT meal_name, calories, protein, carbs, fats, logged_at FROM meals"
    
    # Pandas reads the SQL query directly using the database connection
    df = pd.read_sql(query, db)
    
    db.close()
    return df

if __name__ == "__main__":
    # 1. Load the data frame
    df = fetch_data_from_db()
    
    print("\n--- 🐼 RAW PANDAS DATAFRAME ---")
    # head() prints the top 5 rows in a beautiful structured grid
    print(df.head()) 
    
    print("\n--- 📊 AUTOMATED STATISTICAL SUMMARY ---")
    # describe() automatically calculates count, mean, min, max, and quartiles for every macro!
    print(df.describe())