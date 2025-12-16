# app.py

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
# Import the functions from your separate logic files
from logic_files import get_carb_estimate_from_photo, generate_meal_prediction 

app = Flask(__name__)
# Enable CORS for communication between Netlify frontend and this backend
# IMPORTANT: In production, change the origin to your Netlify URL (e.g., origin="https://my-carb-app.netlify.app")
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Define a temporary directory for uploaded files (required for Render/hosting)
UPLOAD_FOLDER = '/tmp'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# This endpoint handles the prediction request
@app.route('/predict', methods=['POST'])
def predict():
    if 'image_file' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    if 'current_bg' not in request.form:
        return jsonify({"error": "No current_bg provided"}), 400
    
    image_file = request.files['image_file']
    current_bg_str = request.form['current_bg']
    
    # Save the uploaded file temporarily
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)
    
    # *** 1. CALL THE CORE LOGIC ***
    try:
        # User ID is hardcoded for simplicity, but in a real app, it would be authenticated
        user_id = "mom_user_123" 
        
        # This function executes the Vision AI call and the Personalization Model
        prediction = generate_meal_prediction(user_id, image_path, current_bg_str)
        
        return jsonify(prediction), 200
    
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({"error": "Internal server error during prediction."}), 500
    
    finally:
        # IMPORTANT: Clean up the temporary file
        if os.path.exists(image_path):
            os.remove(image_path)


# Optional health check endpoint
@app.route('/', methods=['GET'])
def home():
    return "Carb Estimator Backend is running.", 200

if __name__ == '__main__':
    # When running locally, Flask runs on port 5000
    app.run(debug=True, port=5000)
