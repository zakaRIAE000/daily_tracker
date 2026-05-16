import json
import os
from typing import List, Dict

# ==========================================
# OOP SECTION: Defining the Blueprint
# ==========================================
class DailyTracker:
    def __init__(self, target_protein: int, filename: str = "daily_meals.json"):
        self.target_protein = target_protein
        self.filename = filename
        # When we start the script, try to load existing data first
        self.meals: List[Dict[str, int]] = self.load_data()

    def load_data(self) -> List[Dict[str, int]]:
        """Loads data from the JSON file if it exists."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file) # Converts JSON text back into a Python list
        return [] # If no file exists yet, start with an empty list

    def save_data(self):
        """Saves the current meals list to the JSON file."""
        with open(self.filename, "w") as file:
            json.dump(self.meals, file, indent=4) # Converts Python list to formatted JSON text

    def add_meal(self, name: str, protein: int):
        self.meals.append({"name": name, "protein": protein})
        self.save_data() # Automatically save to the file every time a meal is added
        print(f"[+] Logged: {name} ({protein}g protein)")

    # ==========================================
    # FUNCTIONAL SECTION: Processing the Data
    # ==========================================
    def get_total_protein(self) -> int:
        return sum(meal["protein"] for meal in self.meals)

    def get_high_protein_meals(self, threshold: int) -> List[str]:
        return [meal["name"] for meal in self.meals if meal["protein"] >= threshold]

    def generate_report(self):
        total = self.get_total_protein()
        remaining = max(0, self.target_protein - total)
        
        print("\n--- 📊 DAILY PROGRESS REPORT ---")
        print(f"Target: {self.target_protein}g | Current: {total}g")
        
        if remaining == 0:
            print("✅ Goal crushed!")
        else:
            print(f"⏳ Need {remaining}g more to hit the target.")
            
        if self.meals:
            print("Best meals today:", ", ".join(self.get_high_protein_meals(30)))

# ==========================================
# EXECUTION: Running the Script
# ==========================================
if __name__ == "__main__":
    today = DailyTracker(target_protein=135)

    # Note: If you run this script twice, it will add these meals TWICE because 
    # it is saving them to the file. 
    today.add_meal("Steak", 50)
    
    today.generate_report()