from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import os

app = Flask(__name__)

def print_image(img, printer_name):
    temp_path = "temp_print.png"
    img.save(temp_path)
    os.system(f'mspaint /pt "{temp_path}" "{printer_name}"')
    os.remove(temp_path)

@app.route('/print_barcode', methods=['POST'])
def print_barcode():
    data = request.json
    if not data or 'imageBase64' not in data or 'printer_name' not in data:
        return jsonify({"error": "ข้อมูลไม่ครบ"}), 400

    try:
        img_data = base64.b64decode(data['imageBase64'])
        img = Image.open(io.BytesIO(img_data))
        print_image(img, data['printer_name'])
        return jsonify({"status": "success", "message": "พิมพ์เรียบร้อย"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
