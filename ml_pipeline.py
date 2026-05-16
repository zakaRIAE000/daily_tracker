import mysql.connector
import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression

# Load security environment variables
load_dotenv()

def get_data_for_ml() -> pd.DataFrame:
    """Extracts features directly via database cursor to optimize pipeline execution."""
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="nutrition_db"
    )
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT calories, protein, carbs, fats FROM meals"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # Close resources cleanly
    cursor.close()
    db.close()
    
    # Constructing DataFrame directly from dictionaries bypasses SQLAlchemy dependency warnings
    return pd.DataFrame(rows)

def train_nutrition_model():
    df = get_data_for_ml()
    
    if len(df) < 3:
        print("\n[!] ML Error: Not enough data points in the database to train a model.")
        return

    # 1. Isolate Features (X) and Target (y)
    X = df[['protein', 'carbs', 'fats']]
    y = df['calories']

    # 2. Fit the Linear Regression Model
    model = LinearRegression()
    model.fit(X, y)

    weights = model.coef_
    intercept = model.intercept_

    print("\n=============================================")
    print("      🤖 MACHINE LEARNING MODEL TRAINED")
    print("=============================================")
    print("The AI analyzed your meals and discovered these rules:")
    print(f" -> 1g of Protein = {weights[0]:.2f} kcal (True: 4.0)")
    print(f" -> 1g of Carbs   = {weights[1]:.2f} kcal (True: 4.0)")
    print(f" -> 1g of Fat     = {weights[2]:.2f} kcal (True: 9.0)")
    print(f" -> Model Baseline Intercept: {intercept:.2f}")
    print("=============================================\n")

    # 3. Create structured DataFrame for prediction to maintain feature alignment
    test_meal = pd.DataFrame([[40, 50, 15]], columns=['protein', 'carbs', 'fats'])
    predicted_calories = model.predict(test_meal)[0]
    
    print(f"🔮 AI Prediction: A meal with 40g P, 50g C, 15g F will be approx {predicted_calories:.0f} calories.")

if __name__ == "__main__":
    train_nutrition_model()