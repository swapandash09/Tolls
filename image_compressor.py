from flask import Flask, request, send_file
from PIL import Image
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

# Image Compressor
@app.route('/compress', methods=['POST'])
def compress_image():
    file = request.files['image']
    quality = int(request.form['quality'])
    img = Image.open(file)
    img = img.resize((int(img.width / 2), int(img.height / 2)), Image.Resampling.LANCZOS)
    img.save('compressed_image.jpg', quality=quality, optimize=True)
    return send_file('compressed_image.jpg', as_attachment=True)

# PDF to JPG
@app.route('/pdf2jpg', methods=['POST'])
def pdf_to_jpg():
    file = request.files['pdf']
    pdf_path = 'input.pdf'
    file.save(pdf_path)
    images = convert_from_path(pdf_path, dpi=300)
    images[0].save('converted_image.jpg', 'JPEG', quality=95)
    os.remove(pdf_path)
    return send_file('converted_image.jpg', as_attachment=True)

# File Merger
@app.route('/merge', methods=['POST'])
def merge_files():
    files = request.files.getlist('files')
    merger = PdfMerger()
    for file in files:
        merger.append(file)
    merger.write('merged_file.pdf')
    merger.close()
    return send_file('merged_file.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
