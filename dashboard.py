import mysql.connector
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load security environment variables
load_dotenv()

def fetch_data_for_viz() -> pd.DataFrame:
    """Extracts macro data from the live MySQL database."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="nutrition_db"
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT meal_name, protein, carbs, fats FROM meals")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return pd.DataFrame(rows)

def generate_dashboard():
    df = fetch_data_for_viz()
    
    if df.empty:
        print("[!] Error: No data found in the database to plot.")
        return

    # Set up the visual styling
    plt.style.use('ggplot') # Gives a clean, modern grid background
    fig, ax = plt.subplots(figsize=(10, 6))

    # Build a stacked bar chart
    # Fats are stacked on top of Carbs, which are stacked on top of Protein
    p_bars = ax.bar(df['meal_name'], df['protein'], label='Protein (g)', color='#2ecc71')
    c_bars = ax.bar(df['meal_name'], df['carbs'], bottom=df['protein'], label='Carbs (g)', color='#3498db')
    f_bars = ax.bar(df['meal_name'], df['fats'], bottom=df['protein'] + df['carbs'], label='Fats (g)', color='#e74c3c')

    # Add descriptive chart labels
    ax.set_ylabel('Macro Weight (Grams)', fontsize=12, fontweight='bold')
    ax.set_title('🍽️ Macro Nutritional Breakdown Per Logged Meal', fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right')
    
    # Rotate text labels slightly so long meal names fit cleanly
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()

    # 1. Save the visualization as an image file for our GitHub README!
    output_filename = "macro_dashboard.png"
    plt.savefig(output_filename, dpi=300)
    print(f"[+] Dashboard image successfully saved as: {output_filename}")

    # 2. Pop open the interactive chart on your screen
    print("[+] Rendering interactive dashboard window...")
    plt.show()

if __name__ == "__main__":
    generate_dashboard()