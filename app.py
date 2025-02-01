from flask import Flask, render_template, request, jsonify
import requests
import json
import markdown

app = Flask(__name__)
OLLAMA_API_URL = "http://localhost:11434/api/chat"  # Ensure this is the correct API URL
MODEL = "deepseek-r1:14b"


@app.route('/')
def index():
    response = requests.get("http://localhost:11434/api/tags")
    response_json = response.json()
    # Create a list of formatted model names in Markdown
    model_names = [model['name'] for model in response_json["models"]]
    return render_template('index.html', current_model = MODEL, models=model_names)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")  # Get message from frontend
    selected_model = request.json.get("model", MODEL)  # Use default MODEL if none is provided

    data = {
        "model":selected_model ,  # Ensure this model exists in Ollama
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

@app.route('/list', methods=['GET'])
def list_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response_json = response.json()
        # Create a list of formatted model names in Markdown
        model_names_md = "\n".join([f"- **{model['name']}**" for model in response_json["models"]])
        # Convert the markdown text to HTML
        html_response = markdown.markdown(model_names_md)
    except Exception as e:
        html_response = f"Error: {str(e)}"

    # Render the 'list.html' template and pass the HTML-formatted response
    return render_template("list.html", html_response=html_response)

app.run(debug=True)