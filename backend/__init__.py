from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register blueprints here
    from backend.controllers.chat_controller import chat_bp
    app.register_blueprint(chat_bp)

    return app
