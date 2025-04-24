from flask import Flask
from flask_cors import CORS

from backend.SessionTimelineAnalysisDashboardFolder.ClientSentimentData import client_sentiment_bp
from backend.SessionTimelineAnalysisDashboardFolder.ClientTenseData import client_tense_bp
from backend.SessionTimelineAnalysisDashboardFolder.TalkingTimeData import talking_time_bp
from config import Config
from extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True, origins=Config.FRONTEND_URL)


    from routes.user_routes import user_bp
    from routes.session_routes import session_bp
    from routes.protected_routes import protected_bp
    from routes.patient_routes import patient_bp

    app.register_blueprint(talking_time_bp)
    app.register_blueprint(client_tense_bp)
    # app.register_blueprint(speech_cadence_bp)
    app.register_blueprint(client_sentiment_bp)
    # app.register_blueprint(session_timeline_visualization_bp)
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(session_bp, url_prefix='/api/sessions')
    app.register_blueprint(protected_bp, url_prefix='/api')
    app.register_blueprint(patient_bp,url_prefix='/api/patient')

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
