from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_barcode', methods=['POST'])
def upload_barcode():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # คุณอาจส่ง URL หรือ path ให้ client ดึงไปพิมพ์ได้ เช่น
    # return jsonify({"status": "success", "file_path": filepath})

    return jsonify({"status": "success", "message": f"File saved to {filepath}"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
