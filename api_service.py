import mysql.connector
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import datetime

# Load security environment variables
load_dotenv()

# Initialize the core FastAPI application instance
app = FastAPI(
    title="⚡ Zakariae's Nutrition & Fitness Analytics API",
    description="Production-ready backend engine serving multi-table relational metrics.",
    version="1.0.0"
)

def get_db_connection():
    """Establishes an atomic transaction connection to the MySQL server."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_PASSWORD"),
            database="nutrition_db"
        )
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database Engine Error: {err}")

# ==========================================
# REST API ENDPOINTS (ROUTES)
# ==========================================

@app.get("/", tags=["Root"])
def read_root():
    """System heartbeat route confirming server status."""
    return {
        "status": "online",
        "message": "Fitness Pipeline API is actively serving requests.",
        "endpoints": ["/meals/today", "/progress/all"]
    }

@app.get("/meals/today", tags=["Nutrition"])
def get_today_meals():
    """Fetches all meal records entered for the current calendar date."""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT id, meal_name, calories, protein, carbs, fats, logged_at FROM meals WHERE DATE(logged_at) = CURDATE()"
    cursor.execute(query)
    meals = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    # Format the timestamps seamlessly into strings for JSON compatibility
    for meal in meals:
        meal['logged_at'] = str(meal['logged_at'])
        
    return JSONResponse(content={"date": str(datetime.date.today()), "count": len(meals), "data": meals})

@app.get("/progress/all", tags=["Biometrics"])
def get_historical_progress():
    """Retrieves tracking data from the progress table and serializes metrics to floats."""
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT log_date, body_weight, energy_level, sleep_hours FROM daily_progress ORDER BY log_date DESC"
    cursor.execute(query)
    records = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    # Convert data types so they are completely JSON compatible
    for row in records:
        row['log_date'] = str(row['log_date'])
        row['body_weight'] = float(row['body_weight'])  # Convert Decimal -> Float
        row['sleep_hours'] = float(row['sleep_hours'])  # Convert Decimal -> Float
        
    return JSONResponse(content={"total_records": len(records), "data": records})