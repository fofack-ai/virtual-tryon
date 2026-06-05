from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
import base64
from PIL import Image
from rembg import remove
from verify import overlay_cloth_on_model
from verify2 import overlay_lower_body_garment

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = os.path.join('static', 'results')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def remove_background(input_path, output_path):
    try:
        with open(input_path, 'rb') as f:
            input_bytes = f.read()
        output_bytes = remove(input_bytes)
        with open(output_path, 'wb') as f:
            f.write(output_bytes)
        return True
    except Exception as e:
        print(f"Background removal error: {e}")
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/homw')
def homw():
    return render_template('homw.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        model_image = request.files.get('model_image')
        clothes_image = request.files.get('clothes_image')
        garment_type = request.form.get('garment_type')

        if not model_image or not clothes_image:
            return jsonify({'error': 'Files not provided or invalid file names'})

        model_filename = secure_filename(model_image.filename)
        clothes_filename = secure_filename(clothes_image.filename)

        model_path = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
        clothes_path = os.path.join(app.config['UPLOAD_FOLDER'], clothes_filename)
        clothes_no_bg_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no_bg_' + clothes_filename)

        output_filename = 'output_' + model_filename
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        model_image.save(model_path)
        clothes_image.save(clothes_path)

        if not remove_background(clothes_path, clothes_no_bg_path):
            return jsonify({'error': 'Failed to remove background from clothes image'})

        if garment_type == 'lower_body':
            result_path, message = overlay_lower_body_garment(model_path, clothes_no_bg_path, output_path)
        elif garment_type == 'upper_body':
            result_path, message = overlay_cloth_on_model(model_path, clothes_no_bg_path, output_path)
        else:
            return jsonify({'error': 'Invalid garment type specified'})

        if result_path:
            with open(output_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            return render_template('result.html', img_data=img_data)
        else:
            return jsonify({'error': message})

    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)
