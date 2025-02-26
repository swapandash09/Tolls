from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
import os

app = Flask(__name__)

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
