# from PIL import Image
# import os

# def mm_to_px(mm, dpi=203):
#     return int(mm * dpi / 25.4)

# # ขนาดฉลากต่อ 1 รูป
# label_width_mm = 45
# label_height_mm = 20

# # จำนวนรูปต่อแผ่น
# num_images = 5

# # ขนาดรูปจริง
# image_width_mm = 13
# image_height_mm = 9

# # DPI
# dpi = 1500

# # Path
# printer_name = "HP LaserJet M1536dnf MFP"
# image_path = r"C:\Users\nawaphon\OneDrive - KMITL\Desktop\myproject\PL14942.png"
# output_path = r"C:\Users\nawaphon\OneDrive - KMITL\Desktop\myproject\barcode_with_margin_5in1.png"

# # ขนาด canvas รวม
# canvas_width_px = mm_to_px(label_width_mm, dpi)
# canvas_height_px = mm_to_px(label_height_mm * num_images, dpi)
# canvas = Image.new("RGB", (canvas_width_px, canvas_height_px), "white")

# # โหลดและ resize รูป
# image_size = (mm_to_px(image_width_mm, dpi), mm_to_px(image_height_mm, dpi))
# img = Image.open(image_path).resize(image_size, Image.LANCZOS)

# # วางรูปทั้งหมด
# for i in range(num_images):
#     x = (canvas.width - img.width) // 2
#     y = (mm_to_px(label_height_mm, dpi) * i) + ((mm_to_px(label_height_mm, dpi) - img.height) // 2)
#     canvas.paste(img, (x, y))

# # เซฟและสั่งพิมพ์
# canvas.save(output_path)
# os.system(f'mspaint /pt "{output_path}" "{printer_name}"')


from flask import Flask, request, jsonify
from PIL import Image
import io
import base64
import win32api

app = Flask(__name__)

def mm_to_px(mm, dpi=203):
    return int(mm * dpi / 25.4)

def generate_label_sheet(image_data_base64, copies, output_path):
    # กำหนดขนาดฉลากและภาพ
    label_width_mm = 45
    label_height_mm = 20
    image_width_mm = 13
    image_height_mm = 9
    dpi = 1500

    # ขนาด canvas (รวมฉลากหลายชุดตามจำนวน copies)
    canvas_width_px = mm_to_px(label_width_mm, dpi)
    canvas_height_px = mm_to_px(label_height_mm * copies, dpi)
    canvas = Image.new("RGB", (canvas_width_px, canvas_height_px), "white")

    # เปิดรูปจาก base64 และ resize
    image = Image.open(io.BytesIO(base64.b64decode(image_data_base64)))
    image_size = (mm_to_px(image_width_mm, dpi), mm_to_px(image_height_mm, dpi))
    image = image.resize(image_size, Image.LANCZOS)

    # วางรูปลงใน canvas ตามจำนวน copies
    for i in range(copies):
        x = (canvas.width - image.width) // 2
        y = (mm_to_px(label_height_mm, dpi) * i) + ((mm_to_px(label_height_mm, dpi) - image.height) // 2)
        canvas.paste(image, (x, y))

    canvas.save(output_path)
    return output_path

def print_image(image_path):
    printer_name = "HP LaserJet M1536dnf MFP"  # <-- เปลี่ยนชื่อเครื่องปริ้นที่นี่ตามจริง
    win32api.ShellExecute(
        0,
        "printto",
        image_path,
        f'"{printer_name}"',
        ".",
        0
    )

@app.route('/print_barcode', methods=['POST'])
def print_barcode():
    try:
        data = request.json
        image_base64 = data.get("image_base64")  # Base64 ของรูปภาพจาก Power Automate
        copies = int(data.get("copies", 1))      # จำนวนฉลากที่ต้องการพิมพ์

        if not image_base64:
            return jsonify({"status": "error", "message": "Missing image_base64"}), 400

        output_path = "barcode_sheet.png"
        generate_label_sheet(image_base64, copies, output_path)
        print_image(output_path)

        return jsonify({"status": "success", "message": f"Printed {copies} copies."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
