from flask import Flask, request, jsonify
from database import init_db, db_session
from models import Student
from api.routes import api_bp
from utils.privacy import add_noise

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)