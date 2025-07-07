# app.py
from flask import Flask, render_template, request, jsonify, flash
import base64
import io
import os
import cv2
import numpy as np
from PIL import Image
from google.cloud import vision
from solve_equation_file import solve_equation
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcdef'
app.config['UPLOAD_FOLDER'] = 'static'

# Initialize Google Cloud Vision client
API_KEY = os.getenv("GOOGLE_API_KEY")
client = vision.ImageAnnotatorClient(client_options={"api_key": API_KEY})

def binarize(image):
    """Binarize the image for better OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def google_ocr_equation(img_path):
    """Use Google Cloud Vision API to extract text from an image."""
    try:
        input_image = cv2.imread(img_path)
        bw_img = binarize(input_image)
        cv2.imwrite(img_path, bw_img)
        with open(img_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        if not texts:
            return "No text detected in the image"
        detected_text = texts[0].description.strip()
        # Post-process for mathematical equations
        detected_text = detected_text.replace('\n', '')
        detected_text = detected_text.replace('x', '*').replace('÷', '/').replace('^', '**')
        detected_text = detected_text.replace('y2', 'y**2').replace('x2', 'x**2')
        detected_text = detected_text.replace('y0', 'y*0').replace('x0', 'x*0')
        detected_text = detected_text.replace(' ', '').replace('−', '-')
        print(f"Raw OCR: {texts[0].description}")  # Debug
        print(f"Processed OCR: {detected_text}")  # Debug
        return detected_text
    except Exception as e:
        return f"Error in OCR processing: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if 'equation.png' in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'equation.png'))
    return render_template('uploadimage.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        flash('No file part', 'danger')
        return render_template('uploadimage.html')
    file = request.files['image']
    if file.filename == '':
        flash('No selected file', 'danger')
        return render_template('uploadimage.html')
    if file:
        filename = 'equation.png'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image uploaded successfully', 'success')
        return render_template('uploadimage.html', filename=os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/canvas_image', methods=['GET', 'POST'])
def canvas_image():
    return render_template('canvasimage.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.form['canvas_data']
    img_data = base64.b64decode(data.split(',')[1])
    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'equation.png'), 'wb') as f:
        f.write(img_data)
    return 'Image saved'

@app.route('/predict_upload_image', methods=['GET'])
def predict_upload_image():
    if 'equation.png' not in os.listdir(app.config['UPLOAD_FOLDER']):
        return jsonify("Please write or upload an image first")
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'equation.png')
    equation = google_ocr_equation(img_path)
    if equation.startswith("Error") or equation == "No text detected in the image":
        return jsonify(equation)
    display_equation = equation.replace('**', '^')
    return jsonify(display_equation)

@app.route('/square', methods=['GET'])
def square():
    if 'equation.png' not in os.listdir(app.config['UPLOAD_FOLDER']):
        return jsonify({'error': 'Please upload or write something'})
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'equation.png')
    equation = google_ocr_equation(img_path)
    print(f"Equation sent to solver: {equation}")  # Debug
    if equation.startswith("Error") or equation == "No text detected in the image":
        return jsonify({'error': equation})
    try:
        result = solve_equation(equation)
        if 'equation.png' in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'equation.png'))
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f"Error solving equation: {str(e)}"})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True, host='127.0.0.1', port=5000)