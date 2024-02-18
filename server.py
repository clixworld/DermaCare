from flask import Flask, render_template, request, jsonify
from gptresponse import ChatGPT
from inference_sdk import InferenceHTTPClient

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
    bot_response = ai_bot.messages("Mild Acne", "Oily", "Benzoyl Peroxide")
    print(bot_response)
    for file in user_files:
        print(file.filename)

    return "Files Received"

@app.route('/test_infer', methods=['GET'])
def test_infer():
    # Provide the path to your pimple.jpeg image
    image_path = 'static/images/pimple.jpeg'  # Adjust the path as necessary

    # Call the Roboflow API with the image
    result = CLIENT.infer(image_path, model_id="pimples-detection/4")

    # Return the result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)