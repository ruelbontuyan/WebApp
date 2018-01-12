from flask import Flask

app = Flask(__name__)

@app.route('/')
def add():
    return "add:"

if __name__ == "__main__":
    app.run()