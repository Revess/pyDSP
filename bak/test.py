from flask import Flask
from flask import Flask
from flask import request

app = Flask(__name__,static_url_path="",static_folder="./",template_folder="./")

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == "POST":
        print(request.get_data())
        return "done"
    else:
        return app.send_static_file("./index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)