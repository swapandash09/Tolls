from flask import Flask, request, send_file, jsonify
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
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

# File Merger
@app.route('/merge', methods=['POST'])
def merge_files():
    try:
        if 'files' not in request.files:
            return "No files uploaded", 400
        files = request.files.getlist('files')
        merger = PdfMerger()
        for file in files:
            merger.append(file)
        output_path = 'merged_file.pdf'
        merger.write(output_path)
        merger.close()
        response = send_file(output_path, as_attachment=True, download_name='merged_file.pdf')
        os.remove(output_path)
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

# Image Resizer
@app.route('/resize', methods=['POST'])
def resize_image():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        img = Image.open(file)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        output_path = 'resized_image.jpg'
        img.save(output_path, quality=95, optimize=True)
        response = send_file(output_path, as_attachment=True, download_name='resized_image.jpg')
        os.remove(output_path)
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

# Color Picker
@app.route('/pick-color', methods=['POST'])
def pick_color():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        img = Image.open(file).convert('RGB')
        colors = img.getpixel((img.width // 2, img.height // 2))
        color = f'#{colors[0]:02x}{colors[1]:02x}{colors[2]:02x}'
        return jsonify({'color': color})
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
