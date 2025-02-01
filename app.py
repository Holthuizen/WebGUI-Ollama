from flask import Flask, render_template, request, jsonify
import requests
import json
import markdown

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ensure this is the correct API URL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")  # Get message from frontend

    data = {
        "model": "llama3.2",  # Ensure this model exists in Ollama
        "messages": [{"role": "user", "content": user_message}],
        "stream": False
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(OLLAMA_API_URL, data=json.dumps(data), headers=headers)
        response_json = response.json()  # Convert response to JSON
        bot_reply = response_json.get("message", {}).get("content", "Error: No response")
        html_response = markdown.markdown(bot_reply)  # Convert Markdown to HTML
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({"reply": html_response})


app.run(debug=True)
