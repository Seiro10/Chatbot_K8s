from flask import Blueprint, render_template, request, jsonify
from backend.models.chatbot import process_user_message 


chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/")
def home():
    return render_template("index.html")  # Renders the frontend

@chat_bp.route("/chat", methods=["POST"])
def chat():
    """Receives user input and returns chatbot response in Markdown format."""
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    formatted_input = f"""
    Please format the answer to make it readable. Use:
    - H1, H2, H3 for important sections
    - Code blocks for technical terms
    - Highlight information via bulleted list
    - Tables if necessary
    - Keep responses structured and readable.

    **User Message:** {user_input}
    """

    response = process_user_message(formatted_input)
    return jsonify({"response": response})
