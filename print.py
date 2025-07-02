from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload_barcode', methods=['POST'])
def upload_barcode():
    # ตรวจสอบว่ามีไฟล์มาไหม
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # ตรวจสอบว่าเลือกไฟล์มาหรือยัง
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # ป้องกันชื่อไฟล์ไม่ปลอดภัย
    filename = secure_filename(file.filename)
    
    # บันทึกไฟล์ไปที่โฟลเดอร์ uploads
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # ส่งกลับ path หรือ URL สำหรับให้ client ดึงไฟล์ไปพิมพ์ต่อได้
    # (ปรับ URL ตามโดเมนจริงของคุณ)
    file_url = f"http://your-render-domain/uploads/{filename}"
    
    return jsonify({
        "status": "success",
        "message": f"File saved as {filename}",
        "file_url": file_url
    })

if __name__ == '__main__':
    # รัน server บนพอร์ต 5000
    app.run(host="0.0.0.0", port=5000)
