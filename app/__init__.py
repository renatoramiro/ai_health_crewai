from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configure Flask to handle trailing slashes
    app.url_map.strict_slashes = False

    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app