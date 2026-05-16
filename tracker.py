from typing import List, Dict

# ==========================================
# OOP SECTION: Defining the Blueprint
# ==========================================
class DailyTracker:
    def __init__(self, target_protein: int):
        # The __init__ method sets up our initial state when we create a new day
        self.target_protein = target_protein
        self.meals: List[Dict[str, int]] = [] 

    def add_meal(self, name: str, protein: int):
        # A method that modifies the object's state
        self.meals.append({"name": name, "protein": protein})
        print(f"[+] Logged: {name} ({protein}g protein)")

    # ==========================================
    # FUNCTIONAL SECTION: Processing the Data
    # ==========================================
    def get_total_protein(self) -> int:
        # Instead of a messy 'for loop', we use a functional approach here.
        # 'List comprehension' extracts just the protein numbers, and sum() calculates the total.
        return sum(meal["protein"] for meal in self.meals)

    def get_high_protein_meals(self, threshold: int) -> List[str]:
        # Functional 'filter' concept: We filter the data without changing the original list.
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
            
        print("Best meals today:", ", ".join(self.get_high_protein_meals(30)))

# ==========================================
# EXECUTION: Running the Script
# ==========================================
if __name__ == "__main__":
    # 1. Instantiate the object (Set your specific daily target)
    today = DailyTracker(target_protein=135)

    # 2. Add some data
    today.add_meal("Eggs and Oats", 30)
    today.add_meal("Chicken Breast", 55)
    today.add_meal("Greek Yogurt", 20)

    # 3. Process and view the output
    today.generate_report()