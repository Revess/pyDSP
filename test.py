from flask import Flask
from flask import Flask
from flask import request

app = Flask(__name__,static_url_path="",static_folder="./",template_folder="./")

@app.route("/")
def index():
    return app.send_static_file("./index.html")

@app.route("/pitch", methods=["POST"])
def pitch():
    slider = request.form["slider"]
    return slider

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)