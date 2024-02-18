from flask import Flask, render_template, request
from gptresponse import ChatGPT
from inference_sdk import InferenceHTTPClient
import os

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
    skin_type = request.form['skin-type']
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
            bot_response = ai_bot.messages(class_name, skin_type)
            bot_responses.append(bot_response)

    return render_template("return.html", bot_responses=bot_responses)

if __name__ == '__main__':
    app.run(debug=True)
