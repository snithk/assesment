from flask import Flask
from flask_cors import CORS
from config import Config
from routes import auth_bp, video_bp
from extensions import mongo

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    mongo.init_app(app)
    
    # Pass mongo instance to blueprints / models if needed, 
    # or use current_app extensions pattern.
    app.mongo = mongo

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(video_bp, url_prefix='/')

    @app.route('/')
    def index():
        return "API Video Backend is Running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
