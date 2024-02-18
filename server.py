from flask import Flask, render_template, request
from gptresponse import ChatGPT
from inference_sdk import InferenceHTTPClient
import os
import ast

ai_bot = ChatGPT()

app = Flask(__name__)

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="w6Up93MdGNyb5HbWu18r"
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
        temp_path = os.path.join('static/images', file.filename)
        file.save(temp_path)
        
        # Call the Roboflow API with the image
        result = CLIENT.infer(temp_path, model_id="acne-detection-5x7wb/1")
        
        # Extract the class from the result
        class_name = result['predictions'][0]['class'] if result['predictions'] else None
        all_classes.append(class_name)
        
        # Clean up the saved file
        os.remove(temp_path)

    # Pass the extracted classes to the chatbot
    bot_responses = []
    exists = []
    for class_name in all_classes:
        if class_name is not None:
            if class_name.upper() not in exists:
                bot_response = ai_bot.messages(class_name, skin_type)
                bot_response = ast.literal_eval(bot_response)
                print(bot_response["diagnosis"])
                bot_responses.append(bot_response)
                exists.append(class_name.upper())
            

    return render_template("return.html", bot_responses=bot_responses, skin_type=skin_type)

if __name__ == '__main__':
    app.run(debug=True)
