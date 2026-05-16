import json
import os
from typing import List, Dict

# ==========================================
# OOP SECTION: The Multi-Dimensional Blueprint
# ==========================================
class DailyTracker:
    def __init__(self, target_calories: int, target_protein: int, target_carbs: int, target_fats: int, filename: str = "daily_meals.json"):
        # Now tracking 4 separate targets
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

    # Updated to accept all macros
    def add_meal(self, name: str, calories: int, protein: int, carbs: int, fats: int):
        self.meals.append({
            "name": name, 
            "calories": calories, 
            "protein": protein,
            "carbs": carbs,
            "fats": fats
        })
        self.save_data()
        print(f"[+] Logged: {name} ({calories} kcal, {protein}g P)")

    # ==========================================
    # FUNCTIONAL SECTION: Aggregating Data
    # ==========================================
    def get_totals(self) -> Dict[str, int]:
        # Using a dictionary to cleanly return all 4 totals at once
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
        # Formatting the output so it aligns nicely in the terminal
        print(f"Calories: {totals['calories']:>4} / {self.target_calories} kcal")
        print(f"Protein:  {totals['protein']:>4} / {self.target_protein} g")
        print(f"Carbs:    {totals['carbs']:>4} / {self.target_carbs} g")
        print(f"Fats:     {totals['fats']:>4} / {self.target_fats} g")
        print("===============================\n")

# ==========================================
# EXECUTION
# ==========================================
if __name__ == "__main__":
    # 1. Initialize with your full daily goals
    today = DailyTracker(
        target_calories=2500, 
        target_protein=135, 
        target_carbs=300, 
        target_fats=80
    )

    # 2. Add a complex meal
    today.add_meal("Chicken, Rice, and Avocado", calories=650, protein=50, carbs=60, fats=20)
    
    # 3. View the new multidimensional report
    today.generate_report()