import mysql.connector
import os
from dotenv import load_dotenv
from datetime import date
from typing import List, Dict

load_dotenv()

class DailyTracker:
    def __init__(self):
        db_password = os.getenv("DB_PASSWORD")
        if not db_password:
            raise ValueError("Security Error: 'DB_PASSWORD' not found in your .env file.")

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=db_password,
            database="nutrition_db"
        )
        self.cursor = self.db.cursor(dictionary=True)

    # === MEAL TABLE OPERATIONS ===
    def add_meal(self, name: str, calories: int, protein: int, carbs: int, fats: int):
        sql = """
            INSERT INTO meals (meal_name, calories, protein, carbs, fats) 
            VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (name, calories, protein, carbs, fats))
        self.db.commit()
        print(f"\n[+] Relational Logged: {name} saved to 'meals' table!")

    def generate_meal_report(self):
        query = "SELECT * FROM meals WHERE DATE(logged_at) = CURDATE()"
        self.cursor.execute(query)
        meals = self.cursor.fetchall()
        
        cals = sum(m["calories"] for m in meals)
        prot = sum(m["protein"] for m in meals)
        
        print("\n===============================")
        print(f" 📊 MEAL TOTALS FOR TODAY")
        print("===============================")
        print(f"Calories: {cals} kcal | Protein: {prot}g")
        print("===============================\n")

    # === PROGRESS TABLE OPERATIONS ===
    def log_daily_progress(self, weight: float, energy: int, sleep: float):
        """Inserts or updates the progress metrics for the current date."""
        sql = """
            INSERT INTO daily_progress (log_date, body_weight, energy_level, sleep_hours)
            VALUES (CURDATE(), %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                body_weight = VALUES(body_weight),
                energy_level = VALUES(energy_level),
                sleep_hours = VALUES(sleep_hours)
        """
        self.cursor.execute(sql, (weight, energy, sleep))
        self.db.commit()
        print("\n[+] Relational Logged: Today's physical metrics updated in 'daily_progress'!")

    def close(self):
        self.cursor.close()
        self.db.close()


def main():
    try:
        tracker = DailyTracker()
    except Exception as err:
        print(f"\n[!] Connection Error: {err}")
        return

    while True:
        print("--- 🟢 RELATIONAL DATA PIPELINE ---")
        print("1. Log a new meal")
        print("2. Log daily progress metrics (Weight/Energy)")
        print("3. View today's meal report")
        print("4. Exit")
        
        choice = input("Select an option (1-4): ")
        
        if choice == '1':
            name = input("Meal name: ")
            try:
                cals = int(input("Calories: "))
                prot = int(input("Protein (g): "))
                carbs = int(input("Carbs (g): "))
                fats = int(input("Fats (g): "))
                tracker.add_meal(name, cals, prot, carbs, fats)
            except ValueError:
                print("\n[!] Input Error: Enter valid integer values.")
                
        elif choice == '2':
            print("\n-- Enter Daily Metrics --")
            try:
                weight = float(input("Body Weight (kg): "))
                energy = int(input("Energy Level (1-10): "))
                sleep = float(input("Sleep Duration (Hours): "))
                if not (1 <= energy <= 10):
                    print("[!] Validation Error: Energy level must be between 1 and 10.")
                    continue
                tracker.log_daily_progress(weight, energy, sleep)
            except ValueError:
                print("\n[!] Input Error: Enter valid numerical values.")
                
        elif choice == '3':
            tracker.generate_meal_report()
            
        elif choice == '4':
            print("\nDisconnecting engines...")
            tracker.close()
            break
        else:
            print("\n[!] Invalid selection.")

if __name__ == "__main__":
    main()