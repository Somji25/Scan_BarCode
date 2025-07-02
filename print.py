from flask import Flask, request, jsonify
import base64
import tempfile
import os
import win32print
import win32ui
from PIL import Image
import io

app = Flask(__name__)

def print_image_windows(image_path, printer_name, num_copies=1):
    # เปิดเครื่องพิมพ์
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        # สร้าง device context
        hDC = win32print.CreateDC("WINSPOOL", printer_name, None)
        hDC.StartDoc(image_path)
        hDC.StartPage()

        # เปิดรูปภาพด้วย PIL
        img = Image.open(image_path)
        dib = ImageWin.Dib(img)
        # วาดภาพลง device context
        dib.draw(hDC.GetHandleOutput(), (0, 0, img.width, img.height))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    finally:
        win32print.ClosePrinter(hPrinter)

@app.route('/print_barcode', methods=['POST'])
def api_print_barcode():
    data = request.json
    print("Received JSON:", data)

    base64_image = data.get("base64_image")
    printer_name = data.get("printer_name")
    num_images = int(data.get("num_images", 1))

    if not base64_image or not printer_name:
        return jsonify({"error": "Missing required parameters"}), 400

    # ตัด prefix 'data:image/png;base64,' ออกถ้ามี
    if base64_image.startswith("data:image"):
        base64_image = base64_image.split(",")[1]

    try:
        # แปลง base64 เป็น bytes
        image_data = base64.b64decode(base64_image)
    except Exception as e:
        return jsonify({"error": "Invalid base64 image data", "details": str(e)}), 400

    # สร้างไฟล์ชั่วคราวเก็บรูป
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_img_file:
        temp_img_file.write(image_data)
        temp_img_path = temp_img_file.name

    try:
        # พิมพ์ภาพตามจำนวนที่ระบุ
        for _ in range(num_images):
            print_image_windows(temp_img_path, printer_name)
    except Exception as e:
        return jsonify({"error": "Failed to print", "details": str(e)}), 500
    finally:
        # ลบไฟล์ชั่วคราว
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)

    return jsonify({"message": "Print job sent", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
