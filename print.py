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
from PIL import Image, ImageDraw, ImageFont
import io
import base64

app = Flask(__name__)

@app.route("/print_barcode", methods=["POST"])
def print_barcode():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)

        barcode_text = data.get("barcode_text")
        if not barcode_text:
            return jsonify({"error": "barcode_text is required"}), 400
        
        # ตัวอย่าง: สร้างรูปบาร์โค้ดแบบง่ายๆ (จะเปลี่ยนเป็นบาร์โค้ดจริงก็ได้)
        img = Image.new('RGB', (300, 100), color='white')
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        d.text((10, 40), f"Barcode: {barcode_text}", font=font, fill=(0,0,0))

        # แปลงรูปเป็น base64 ส่งกลับ (ถ้าต้องการ)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # หรือจะสั่งพิมพ์ที่เครื่องเซิร์ฟเวอร์ได้ที่นี่ (ไม่ขอลงรายละเอียดสั่งพิมพ์นะ)

        return jsonify({"status": "success", "image_base64": img_str})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


