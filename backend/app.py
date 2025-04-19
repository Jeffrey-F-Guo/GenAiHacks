from flask import Flask
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os
from views import api_blueprint
from agents.search_agent import SearchAgent

load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Register the API blueprint
app.register_blueprint(api_blueprint)

@app.route('/')
def home():
    return {"message": 'Hello, World!'}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
    