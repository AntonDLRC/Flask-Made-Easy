from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    #home page
    return "<p>Hello, again!</p>"

if __name__ == "__main__":
    app.run(debug=True)