from flask import Flask, request, send_file
from PIL import Image
from pdf2image import convert_from_path
import os

app = Flask(__name__)

# Image Compressor
@app.route('/compress', methods=['POST'])
def compress_image():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        quality = int(request.form.get('quality', 70))
        img = Image.open(file)
        img = img.resize((int(img.width / 2), int(img.height / 2)), Image.Resampling.LANCZOS)
        output_path = 'compressed_image.jpg'
        img.save(output_path, quality=quality, optimize=True)
        response = send_file(output_path, as_attachment=True, download_name='compressed_image.jpg')
        os.remove(output_path)
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

# PDF to JPG
@app.route('/pdf2jpg', methods=['POST'])
def pdf_to_jpg():
    try:
        if 'pdf' not in request.files:
            return "No PDF uploaded", 400
        file = request.files['pdf']
        pdf_path = 'input.pdf'
        file.save(pdf_path)
        images = convert_from_path(pdf_path, dpi=300)
        output_path = 'converted_image.jpg'
        images[0].save(output_path, 'JPEG', quality=95)
        os.remove(pdf_path)
        response = send_file(output_path, as_attachment=True, download_name='converted_image.jpg')
        os.remove(output_path)
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
