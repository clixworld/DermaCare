from flask import Flask, render_template, request, jsonify
from gptresponse import ChatGPT
from inference_sdk import InferenceHTTPClient
import os
import json

ai_bot = ChatGPT()

app = Flask(__name__)

# Initialize the InferenceHTTPClient with your API key and URL
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="w6Up93MdGNyb5HbWu18r"  # Replace with your actual API key
)

@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route("/user_photos", methods=['POST'])
def user_photos():
    user_files = request.files.getlist('files[]')
    all_classes = []
    
    for file in user_files:
        # Save file to a temporary path
        temp_path = os.path.join('static/images', file.filename)
        file.save(temp_path)
        
        # Call the Roboflow API with the image
        result = CLIENT.infer(temp_path, model_id="pimples-detection/4")
        
        # Extract the class from the result
        class_name = result['predictions'][0]['class'] if result['predictions'] else None
        all_classes.append(class_name)
        
        # Clean up the saved file
        os.remove(temp_path)

    # Pass the extracted classes to the chatbot
    bot_responses = []
    for class_name in all_classes:
        if class_name is not None:
            # You might need to adjust the message format based on your bot's functionality
            bot_response = ai_bot.messages(class_name, "Oily", "Benzoyl Peroxide")
            bot_responses.append(bot_response)

    # Return the bot responses as JSON
    return jsonify(bot_responses)

if __name__ == '__main__':
    app.run(debug=True)
