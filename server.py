from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template('index.html')

@app.route("/user_photos", methods=['POST'])
def user_photos():
    user_files = request.files.getlist('files[]')
    for file in user_files:
        print(file.filename)

    return "Files Received"

if __name__ == '__main__':
    app.run(debug=True)