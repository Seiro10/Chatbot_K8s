from flask import Flask
from backend.controllers.chat_controller import chat_bp
import os

def create_app():
    # Set the template path to the frontend folder
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/templates"))

    app = Flask(__name__, template_folder=template_dir)  # ✅ Use templates from frontend/

    # Register Blueprints
    app.register_blueprint(chat_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
