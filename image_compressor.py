from flask import Flask, request, send_file
from PIL import Image
app = Flask(__name__)
@app.route('/compress', methods=['POST'])
def compress_image():
    file = request.files['image']
    quality = int(request.form['quality'])
    img = Image.open(file)
    img = img.resize((int(img.width / 2), int(img.height / 2)), Image.Resampling.LANCZOS)  # Better resizing
    img.save('compressed_image.jpg', quality=quality, optimize=True)
    return send_file('compressed_image.jpg', as_attachment=True)
if __name__ == '__main__':
    app.run(port=5000)
