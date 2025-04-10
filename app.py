from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    print("📁 Current working directory:", os.getcwd())
    print("📁 Flask looking for templates in:", app.template_folder)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
