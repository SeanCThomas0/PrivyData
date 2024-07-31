import logging
from flask import Flask, send_from_directory, jsonify
from database import init_db
from api.routes import api_bp
import os
import sys



#os.environ['OPENDP_LIB_DIR']=r'C:\student_api_project\venv\Lib\site-packages\opendp\lib'

# opendp_lib_path = r"C:\student_api_project\venv\Lib\site-packages"
# opendp_lib_path2 = r"C:\student_api_project\venv\Lib\site-packages\opendp"
# opendp_lib_path3 = r"C:\student_api_project\venv\Lib\site-packages\opendp\lib"
# sys.path.append(opendp_lib_path)
# sys.path.append(opendp_lib_path2)
#sys.path.append(opendp_lib_path3)
# print(sys.path)
import opendp.prelude as dp
dp.enable_features('contrib')
laplace_mechanism = dp.space_of(float) >> dp.m.then_laplace(scale=1.)
dp_value = laplace_mechanism(123.0)
print(dp_value)

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