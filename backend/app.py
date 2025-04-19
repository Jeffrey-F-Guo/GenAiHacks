from flask import Flask
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"message":'Hello, World!'}

if __name__ == '__main__':
    app.run(debug=True)