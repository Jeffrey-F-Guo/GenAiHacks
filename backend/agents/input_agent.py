import openai
import json
from dotenv import load_dotenv
import os
from datetime import datetime
import google.generativeai as genai

load_dotenv()
# Configure the API with your key
def configure_genai(api_key):
    genai.configure(api_key=api_key)



# Example usage

# Your API key (in a real app, this should be stored securely, e.g., as an environment variable)
GEMINI_API_KEY = os.getenv('GOOGLE_GENAI_API_KEY')
model = genai.GenerativeModel("gemini-1.5-pro")
# Configure the API
configure_genai(GEMINI_API_KEY)

# Example prompt
prompt = "What is fun to do in LA this weekend?"

try:
    # Generate response
    response = model.generate_content(prompt).text
    print("Gemini response:")
    print(response)
except Exception as e:
    print(f"Error: {e}")



# if __name__ == "__main__":
#     main()