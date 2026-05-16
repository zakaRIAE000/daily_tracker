import json
import os
from typing import List, Dict

# ==========================================
# OOP SECTION: The Multi-Dimensional Blueprint
# ==========================================
class DailyTracker:
    def __init__(self, target_calories: int, target_protein: int, target_carbs: int, target_fats: int, filename: str = "daily_meals.json"):
        self.target_calories = target_calories
        self.target_protein = target_protein
        self.target_carbs = target_carbs
        self.target_fats = target_fats
        self.filename = filename
        self.meals: List[Dict[str, int]] = self.load_data()

    def load_data(self) -> List[Dict[str, int]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.meals, file, indent=4)

    def add_meal(self, name: str, calories: int, protein: int, carbs: int, fats: int):
        self.meals.append({
            "name": name, 
            "calories": calories, 
            "protein": protein,
            "carbs": carbs,
            "fats": fats
        })
        self.save_data()
        print(f"\n[+] Successfully Logged: {name}!")

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
        print("    📊 FULL MACRO REPORT")
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
    # 1. Initialize the tracker 
    tracker = DailyTracker(target_calories=2500, target_protein=135, target_carbs=300, target_fats=80)

    # 2. Start the infinite Application Loop
    while True:
        print("\n--- 🟢 NUTRITION TRACKER MENU ---")
        print("1. Log a new meal")
        print("2. View daily report")
        print("3. Exit")
        
        # input() pauses the script and waits for the user to type something
        choice = input("Select an option (1-3): ")
        
        if choice == '1':
            print("\n-- Enter Meal Details --")
            name = input("Meal name: ")
            
            # Using try/except for Error Handling (Crucial for Data Science!)
            # If the user types "apple" instead of a number for calories, it won't crash the program.
            try:
                cals = int(input("Calories: "))
                prot = int(input("Protein (g): "))
                carbs = int(input("Carbs (g): "))
                fats = int(input("Fats (g): "))
                tracker.add_meal(name, cals, prot, carbs, fats)
            except ValueError:
                print("\n[!] Data Error: Please enter valid numbers for macros, not letters.")
                
        elif choice == '2':
            tracker.generate_report()
            
        elif choice == '3':
            print("\nExiting tracker. Stay disciplined!")
            break # This breaks the while loop and ends the program
            
        else:
            print("\n[!] Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()