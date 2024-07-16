import logging
from flask import Flask, send_from_directory, jsonify
from database import init_db
from api.routes import api_bp
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.register_blueprint(api_bp, url_prefix='/api')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f'An error occurred: {str(e)}')
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)