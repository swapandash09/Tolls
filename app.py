from flask import Flask, request, send_file
from PIL import Image
import os

app = Flask(__name__)

@app.route('/compress', methods=['POST'])
def compress_image():
    try:
        # File aur quality frontend se lena
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        quality = int(request.form.get('quality', 70))  # Default 70 agar quality nahi mili
        
        # Image process karna
        img = Image.open(file)
        img = img.resize((int(img.width / 2), int(img.height / 2)), Image.Resampling.LANCZOS)
        
        # Output file save karna
        output_path = 'compressed_image.jpg'
        img.save(output_path, quality=quality, optimize=True)
        
        # File bhejna aur cleanup
        response = send_file(output_path, as_attachment=True, download_name='compressed_image.jpg')
        os.remove(output_path)  # Temporary file delete karna
        return response
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
