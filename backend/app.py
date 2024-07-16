from flask import Flask, send_from_directory
from database import init_db
from api.routes import api_bp
import os

app = Flask(__name__, static_folder='../frontend')
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)