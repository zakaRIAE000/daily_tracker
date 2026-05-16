import mysql.connector
from datetime import date
from typing import List, Dict

# ==========================================
# OOP SECTION: The MySQL Database Pipeline
# ==========================================
class DailyTracker:
    def __init__(self, target_calories: int, target_protein: int, target_carbs: int, target_fats: int):
        self.target_calories = target_calories
        self.target_protein = target_protein
        self.target_carbs = target_carbs
        self.target_fats = target_fats
        
        # 1. Establish the Database Connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="08102000@Zakariae", # <-- UPDATE THIS!
            database="nutrition_db"
        )
        # Using dictionary=True means SQL rows come back as Python dictionaries!
        self.cursor = self.db.cursor(dictionary=True) 
        self.meals: List[Dict] = self.load_data()

    def load_data(self) -> List[Dict]:
        """Runs a SQL query to pull ONLY today's meals."""
        query = "SELECT * FROM meals WHERE DATE(logged_at) = CURDATE()"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_meal(self, name: str, calories: int, protein: int, carbs: int, fats: int):
        """Inserts a new row into the MySQL database."""
        sql = """
            INSERT INTO meals (meal_name, calories, protein, carbs, fats) 
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, calories, protein, carbs, fats)
        self.cursor.execute(sql, values)
        self.db.commit() # Locks the transaction into the database
        
        # Update the local Python list so the report works immediately
        self.meals.append({
            "meal_name": name, 
            "calories": calories, 
            "protein": protein,
            "carbs": carbs,
            "fats": fats
        })
        print(f"\n[+] Successfully Inserted into MySQL: {name}!")

    def get_totals(self) -> Dict[str, int]:
        return {
            "calories": sum(m["calories"] for m in self.meals),
            "protein": sum(m["protein"] for m in self.meals),
            "carbs": sum(m["carbs"] for m in self.meals),
            "fats": sum(m["fats"] for m in self.meals)
        }

    def generate_report(self):
        totals = self.get_totals()
        print("\n===============================")
        print(f"  📊 DB REPORT FOR: {date.today()}")
        print("===============================")
        print(f"Calories: {totals['calories']:>4} / {self.target_calories} kcal")
        print(f"Protein:  {totals['protein']:>4} / {self.target_protein} g")
        print(f"Carbs:    {totals['carbs']:>4} / {self.target_carbs} g")
        print(f"Fats:     {totals['fats']:>4} / {self.target_fats} g")
        print("===============================\n")

# ==========================================
# EXECUTION: Interactive CLI Menu
# ==========================================
def main():
    # If the password is wrong, the program will crash here with an Access Denied error.
    try:
        tracker = DailyTracker(target_calories=2500, target_protein=135, target_carbs=300, target_fats=80)
    except mysql.connector.Error as err:
        print(f"Error: Could not connect to database. {err}")
        return

    while True:
        print("\n--- 🟢 SQL NUTRITION TRACKER ---")
        print("1. Log a new meal to Database")
        print("2. View daily report")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            print("\n-- Enter Meal Details --")
            name = input("Meal name: ")
            try:
                cals = int(input("Calories: "))
                prot = int(input("Protein (g): "))
                carbs = int(input("Carbs (g): "))
                fats = int(input("Fats (g): "))
                tracker.add_meal(name, cals, prot, carbs, fats)
            except ValueError:
                print("\n[!] Data Error: Please enter valid numbers.")
                
        elif choice == '2':
            tracker.generate_report()
            
        elif choice == '3':
            print("\nDisconnecting from database. Goodbye!")
            # Always close the connection cleanly!
            tracker.cursor.close()
            tracker.db.close()
            break
        else:
            print("\n[!] Invalid choice.")

if __name__ == "__main__":
    main()