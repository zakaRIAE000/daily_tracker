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
    
    # =========================================================
    # DATA MANIPULATION LAYER: Time-Series Aggregation
    # =========================================================
    
    # 2. Convert the 'logged_at' timestamp string into actual Python datetime objects
    df['logged_at'] = pd.to_datetime(df['logged_at'])
    
    # 3. Extract JUST the date (YYYY-MM-DD) and create a new column
    df['logged_date'] = df['logged_at'].dt.date
    
    # 4. Group by the date and sum up all the numeric macro columns
    daily_totals = df.groupby('logged_date')[['calories', 'protein', 'carbs', 'fats']].sum().reset_index()
    
    print("\n=============================================")
    print("      📈 HISTORICAL DAILY PROGRESS")
    print("=============================================")
    
    # 5. Iterate through the daily totals to check your targets
    target_protein = 135
    
    for index, row in daily_totals.iterrows():
        print(f"Date: {row['logged_date']}")
        print(f" -> Total Calories: {row['calories']} kcal")
        print(f" -> Total Protein:  {row['protein']}g / {target_protein}g")
        
        # Check if you met your 135g muscle development goal
        if row['protein'] >= target_protein:
            print(" -> 🎯 Status: Target Crushed! Great day of hitting macros.")
        else:
            deficit = target_protein - row['protein']
            print(f" -> ⏳ Status: Deficit. You missed your target by {deficit}g.")
        print("-" * 45)