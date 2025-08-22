import cohere
import flask 
from dotenv import load_dotenv
import os

from flask_cors import CORS

load_dotenv()

api_key = os.getenv("API_KEY")
co = cohere.ClientV2(api_key)


def chat_with_cohere(prompt, message):
    
    response = co.chat(
        model="command-light",
        messages= [{"role":"system", "content": "Você é um assistente amigável e prestativo."}]+message,
        max_tokens=100,
        temperature=0.5
    )
    return response.message.content[0].text
    

if __name__ == "__main__":
    message =[]
    app = flask.Flask(__name__)
    CORS(app)
    @app.route("/chat", methods=["POST"])
    def chat():
        data = flask.request.json
        user_message = data.get("message")
        message.append({"role": "user", "content": user_message})
        if not user_message:
            return flask.jsonify({"error": "No message provided"}), 400
        
        response_text = chat_with_cohere(user_message, message)
        return flask.jsonify({"response": response_text})

    app.run(debug=True)