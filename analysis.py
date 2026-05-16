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
    query = "SELECT meal_name, calories, protein, carbs, fats, logged_at FROM meals"
    df = pd.read_sql(query, db)
    db.close()
    return df

if __name__ == "__main__":
    # 1. Fetch the data frame from MySQL
    df = fetch_data_from_db()
    
    print("\n--- 🐼 ALL LOGGED MEALS ---")
    print(df[['meal_name', 'protein', 'calories']]) # Showing specific columns for clarity
    
    # =========================================================
    # DATA MANIPULATION LAYER: Boolean Masking
    # =========================================================
    
    # 2. Define the threshold condition (Targeting meals with more than 45g protein)
    protein_threshold = 45
    
    # 3. Create the Boolean Mask (Evaluates True/False for each row)
    high_protein_mask = df['protein'] > protein_threshold
    
    # 4. Apply the mask to filter the DataFrame
    high_protein_df = df[high_protein_mask]
    
    print(f"\n--- 💪 HIGH-PROTEIN POWER MEALS ONLY (>{protein_threshold}g) ---")
    if high_protein_df.empty:
        print("No meals match this high threshold yet! Go log a heavy steak or chicken bowl.")
    else:
        print(high_protein_df[['meal_name', 'protein', 'calories']])