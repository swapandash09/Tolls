from flask import Flask, request, send_file
from pdf2image import convert_from_path
import os

app = Flask(__name__)

@app.route('/pdf2jpg', methods=['POST'])
def pdf_to_jpg():
    file = request.files['pdf']
    pdf_path = 'input.pdf'
    file.save(pdf_path)
    images = convert_from_path(pdf_path, dpi=300)  # Better quality
    images[0].save('converted_image.jpg', 'JPEG', quality=95)
    os.remove(pdf_path)
    return send_file('converted_image.jpg', as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
