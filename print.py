import os
import base64
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify

app = Flask(__name__)

def mm_to_px(mm, dpi=203):
    return int(mm * dpi / 25.4)

def print_barcode(img: Image.Image, printer_name, num_images=5):
    label_width_mm = 45
    label_height_mm = 20
    image_width_mm = 13
    image_height_mm = 9
    dpi = 1500

    canvas_width_px = mm_to_px(label_width_mm, dpi)
    canvas_height_px = mm_to_px(label_height_mm * num_images, dpi)
    canvas = Image.new("RGB", (canvas_width_px, canvas_height_px), "white")

    image_size = (mm_to_px(image_width_mm, dpi), mm_to_px(image_height_mm, dpi))
    img = img.resize(image_size, Image.LANCZOS)

    for i in range(num_images):
        x = (canvas.width - img.width) // 2
        y = (mm_to_px(label_height_mm, dpi) * i) + ((mm_to_px(label_height_mm, dpi) - img.height) // 2)
        canvas.paste(img, (x, y))

    output_path = r"C:\temp\barcode_print.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    canvas.save(output_path)

    # สั่งพิมพ์ด้วย mspaint (Windows)
    os.system(f'mspaint /pt "{output_path}" "{printer_name}"')
    return output_path

@app.route('/print_barcode', methods=['POST'])
def api_print_barcode():
    data = request.json

    base64_image = data.get("base64_image")
    printer_name = data.get("printer_name")
    num_images = int(data.get("num_images", 5))

    if not base64_image or not printer_name:
        return jsonify({"error": "Missing required parameters"}), 400

    try:
        # ตัด prefix "data:image/png;base64," ออกถ้ามี
        if base64_image.startswith("data:image"):
            base64_image = base64_image.split(",", 1)[1]

        img_data = base64.b64decode(base64_image)
        img = Image.open(BytesIO(img_data))
        output = print_barcode(img, printer_name, num_images)
        return jsonify({"status": "success", "output_file": output})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
