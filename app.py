from flask import Flask, request, send_file, jsonify
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

# Basic route to check if server is running
@app.route('/', methods=['GET'])
def health_check():
    return "ToolVerse Backend is Running!", 200

# Image Compressor
@app.route('/compress', methods=['POST'])
def compress_image():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if not file.filename:
            return "No file selected", 400
        quality = int(request.form.get('quality', 70))
        print(f"Received file: {file.filename}, Quality: {quality}")
        
        img = Image.open(file.stream)
        img = img.resize((int(img.width / 2), int(img.height / 2)), Image.Resampling.LANCZOS)
        output_path = 'compressed_image.jpg'
        img.save(output_path, quality=quality, optimize=True)
        print(f"Saved file to: {output_path}")
        
        with open(output_path, 'rb') as f:
            response = send_file(
                f,
                mimetype='image/jpeg',
                as_attachment=True,
                download_name='compressed_image.jpg'
            )
        os.remove(output_path)
        return response
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return f"Error: {str(e)}", 500

# PDF to JPG
@app.route('/pdf2jpg', methods=['POST'])
def pdf_to_jpg():
    try:
        if 'pdf' not in request.files:
            return "No PDF uploaded", 400
        file = request.files['pdf']
        if not file.filename:
            return "No file selected", 400
        print(f"Received file: {file.filename}")
        pdf_path = 'input.pdf'
        file.save(pdf_path)
        images = convert_from_path(pdf_path, dpi=300)
        output_path = 'converted_image.jpg'
        images[0].save(output_path, 'JPEG', quality=95)
        os.remove(pdf_path)
        print(f"Saved file to: {output_path}")
        response = send_file(output_path, as_attachment=True, download_name='converted_image.jpg')
        os.remove(output_path)
        return response
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return f"Error: {str(e)}", 500

# File Merger
@app.route('/merge', methods=['POST'])
def merge_files():
    try:
        if 'files' not in request.files:
            return "No files uploaded", 400
        files = request.files.getlist('files')
        if len(files) < 2:
            return "At least 2 files required", 400
        print(f"Received files: {[f.filename for f in files]}")
        merger = PdfMerger()
        for file in files:
            merger.append(file)
        output_path = 'merged_file.pdf'
        merger.write(output_path)
        merger.close()
        print(f"Saved file to: {output_path}")
        response = send_file(output_path, as_attachment=True, download_name='merged_file.pdf')
        os.remove(output_path)
        return response
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return f"Error: {str(e)}", 500

# Image Resizer
@app.route('/resize', methods=['POST'])
def resize_image():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if not file.filename:
            return "No file selected", 400
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        print(f"Received file: {file.filename}, Width: {width}, Height: {height}")
        img = Image.open(file)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        output_path = 'resized_image.jpg'
        img.save(output_path, quality=95, optimize=True)
        print(f"Saved file to: {output_path}")
        response = send_file(output_path, as_attachment=True, download_name='resized_image.jpg')
        os.remove(output_path)
        return response
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return f"Error: {str(e)}", 500

# Color Picker
@app.route('/pick-color', methods=['POST'])
def pick_color():
    try:
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if not file.filename:
            return "No file selected", 400
        print(f"Received file: {file.filename}")
        img = Image.open(file).convert('RGB')
        colors = img.getpixel((img.width // 2, img.height // 2))
        color = f'#{colors[0]:02x}{colors[1]:02x}{colors[2]:02x}'
        return jsonify({'color': color})
    except Exception as e:
        print(f"Backend Error: {str(e)}")
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    print("Starting ToolVerse Backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
