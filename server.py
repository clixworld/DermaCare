from flask import Flask, render_template, request, session
from gptresponse import ChatGPT
from inference_sdk import InferenceHTTPClient
import os
import ast
import smtplib
from threading import Lock
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

ai_bot = ChatGPT()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("OPENAI_API_KEY")

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="w6Up93MdGNyb5HbWu18r"
)


app.config['BOT_RESPONSES_LOCK'] = Lock()
app.config['SKIN_TYPE_LOCK'] = Lock()

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
        
        result = CLIENT.infer(temp_path, model_id="acne-detection-5x7wb/1")
        
        class_name = result['predictions'][0]['class'] if result['predictions'] else None
        all_classes.append(class_name)
        
        os.remove(temp_path)

    bot_responses = []
    exists = []
    for class_name in all_classes:
        if class_name is not None:
            if class_name.upper() not in exists:
                bot_response = ai_bot.messages(class_name, skin_type)
                bot_response = ast.literal_eval(bot_response)
                bot_responses.append(bot_response)
                exists.append(class_name.upper())
            
    with app.config['BOT_RESPONSES_LOCK']:
        session['bot_responses'] = bot_responses

    with app.config['SKIN_TYPE_LOCK']:
        session['skin_type'] = skin_type

    return render_template("return.html", bot_responses=bot_responses, skin_type=skin_type)

@app.route('/send_email', methods=['POST'])
def send_message():
    user_email = request.form["email"]
    bot_responses = session.get('bot_responses', [])
    skin_type = session.get('skin_type', '')

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))

        message = MIMEMultipart()
        message["From"] = os.getenv("EMAIL")
        message["To"] = user_email
        message["Subject"] = "DermaCare"

        body = "Here's your suggestions: \n\n"
        for response in bot_responses:
            body += f"Evaluation: {response['diagnosis']}\n Overview: {response['overview']}\n Suggestion: {response['suggestion']}\n\n"

        message.attach(MIMEText(body, "plain"))

        connection.sendmail(from_addr=os.getenv("EMAIL"), to_addrs=user_email, msg=message.as_string())

        return render_template("return.html", bot_responses=bot_responses, skin_type=skin_type)
    
if __name__ == '__main__':
    app.run(debug=True)
