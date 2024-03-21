import os
from flask_cors import CORS
from flask import Flask, request, jsonify, make_response
from service import run_program, get_stars_to_explore

app = Flask(__name__)
# CORS(app)
# CORS(app, origins='http://localhost:3000')
cors = CORS(app, origins='*')
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Чи папка існує
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')    # 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@app.route('/upload', methods=['POST'])
def upload_image():
    # Чи надіслано зображення
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    # Чи файл існує
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Обробка зображення
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    print(file_path)

    try:
        result = run_program(file_path)
        return jsonify({'message': result})
    except Exception as e:
        return jsonify({'message': f'Error processing the image: {str(e)}'}), 500


@app.route('/explore', methods=['POST', 'OPTIONS'])
def explore():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')   # 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    request_data = request.get_json()
    latitude = request_data.get('latitude')
    longitude = request_data.get('longitude')
    stars_data = get_stars_to_explore(latitude, longitude)
    return jsonify({'stars': stars_data})


if __name__ == '__main__':
    app.run(debug=True)
