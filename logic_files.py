# logic_files.py

import os
import random # Used here for a quick mock of a Vision AI API

# --- User Profile Data (Mock Database) ---
def get_user_settings(user_id):
    """Fetches personalized settings for the user (your mom)."""
    # This data would be stored securely in a real app's database.
    return {
        "ic_ratio": 12,        # 1 unit per 12g carbs
        "target_bg": 100,
        "correction_factor": 35, # 1 unit lowers BG by 35 mg/dL
        "historical_factors": {"rice": 1.15, "mashed_potatoes": 1.20, "fried_food": 1.35} 
    }

def get_carb_estimate_from_photo(image_file_path):
    """
    MOCK: This function would call the commercial Vision AI/Nutrition API.
    For deployment, you must integrate a service like Spike API or LogMeal here.
    """
    # Simulating the Vision AI result for a file
    # Replace this with your actual API call that reads the image_file_path
    
    # Simple mock: return a high carb meal
    return {
        "carbs_raw": random.randint(55, 75), # Random carb count to test
        "glycemic_load": random.choice(["low", "medium", "high"]),
        "food_components": ["rice", "chicken_breast", "fried_food"]
    }

def generate_meal_prediction(user_id, meal_photo_path, current_bg_str):
    
    current_bg = int(current_bg_str.split()[0])
    settings = get_user_settings(user_id)
    food_data = get_carb_estimate_from_photo(meal_photo_path)
    
    estimated_carbs = food_data['carbs_raw']
    
    # 1. Apply Personalization Multiplier (The AI's value)
    personalization_multiplier = 1.0 
    for food in food_data['food_components']:
        if food in settings['historical_factors']:
            # Apply the specific historical factor (e.g., rice hits 15% harder)
            personalization_multiplier *= settings['historical_factors'][food]
    
    adjusted_carbs = estimated_carbs * personalization_multiplier
    
    # 2. Calculate Predicted Impact
    
    # BG rise estimate: (Adjusted Carbs / IC Ratio) * BG rise per IC Ratio 
    bg_rise_per_ic_ratio = settings['correction_factor'] * 1 
    bg_rise_estimate = (adjusted_carbs / settings['ic_ratio']) * bg_rise_per_ic_ratio
    
    # 3. Determine Timing
    timing_note = "Inject right before eating."
    if food_data['glycemic_load'] == 'low':
        timing_note = "Consider pre-bolusing 15 minutes."
    elif food_data['glycemic_load'] == 'high':
        timing_note = "High Glycemic Load. Consider splitting your dose."

    # 4. Final Output
    return {
        "Estimated Carbs (AI Adjusted)": f"{round(adjusted_carbs)} grams",
        "Recommended Bolus (Estimate)": f"{round(adjusted_carbs / settings['ic_ratio'], 1)} units",
        "Predicted Peak BG": f"Peak ~{round(current_bg + bg_rise_estimate, -1)} mg/dL",
        "Timing Note": timing_note
    }
