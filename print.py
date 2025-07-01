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
import os

app = Flask(__name__)

def mm_to_px(mm, dpi=203):
    return int(mm * dpi / 25.4)

def print_barcode(image_path, printer_name, num_images=5):
    label_width_mm = 45
    label_height_mm = 20
    image_width_mm = 13
    image_height_mm = 9
    dpi = 1500

    canvas_width_px = mm_to_px(label_width_mm, dpi)
    canvas_height_px = mm_to_px(label_height_mm * num_images, dpi)
    canvas = Image.new("RGB", (canvas_width_px, canvas_height_px), "white")

    image_size = (mm_to_px(image_width_mm, dpi), mm_to_px(image_height_mm, dpi))
    img = Image.open(image_path).resize(image_size, Image.LANCZOS)

    for i in range(num_images):
        x = (canvas.width - img.width) // 2
        y = (mm_to_px(label_height_mm, dpi) * i) + ((mm_to_px(label_height_mm, dpi) - img.height) // 2)
        canvas.paste(img, (x, y))

    output_path = r"C:\temp\barcode_print.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path)

    os.system(f'mspaint /pt "{output_path}" "{printer_name}"')
    return output_path

@app.route('/print_barcode', methods=['POST'])
def api_print_barcode():
    data = request.json
    image_path = data.get("image_path")
    printer_name = data.get("printer_name")
    num_images = data.get("num_images", 5)

    if not image_path or not printer_name:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        output = print_barcode(image_path, printer_name, int(num_images))
        return jsonify({"status": "success", "output_file": output})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

