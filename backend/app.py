from flask import Flask, jsonify
from flask_cors import CORS
from mongoengine import connect

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, supports_credentials=True, origins=Config.FRONTEND_URL)

    connect(host=app.config['MONGO_URI'])


    from routes.user_routes import user_bp
    from routes.session_routes import session_bp
    from routes.protected_routes import protected_bp

    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    app.register_blueprint(protected_bp, url_prefix='/api')


    @app.route('/')
    def index():
        return jsonify({'message': 'Chatbot API is running'})

    return app


if __name__ == '__main__':
    create_app().run(debug=True)
