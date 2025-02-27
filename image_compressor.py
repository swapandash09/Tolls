from flask import Flask, request, send_file
from PIL import Image
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return "Image Compressor Backend is Running!", 200

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

if __name__ == '__main__':
    print("Starting Image Compressor Backend...")
    app.run(host='0.0.0.0', port=5000, debug=True)
