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
from PIL import Image, ImageDraw, ImageFont, ImageWin
import win32print
import win32ui
import os

app = Flask(__name__)

def print_image(image_path, printer_name=None):
    if printer_name is None:
        printer_name = win32print.GetDefaultPrinter()
    
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)

        printable_area = hDC.GetDeviceCaps(8), hDC.GetDeviceCaps(10)
        printer_size = hDC.GetDeviceCaps(110), hDC.GetDeviceCaps(111)

        bmp = Image.open(image_path)
        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        scale = min(ratios)
        scaled_width, scaled_height = int(bmp.size[0] * scale), int(bmp.size[1] * scale)
        bmp = bmp.resize((scaled_width, scaled_height), Image.LANCZOS)

        hDC.StartDoc("Barcode Print")
        hDC.StartPage()

        dib = ImageWin.Dib(bmp)
        x = int((printer_size[0] - scaled_width) / 2)
        y = int((printer_size[1] - scaled_height) / 2)
        dib.draw(hDC.GetHandleOutput(), (x, y, x + scaled_width, y + scaled_height))

        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
    finally:
        win32print.ClosePrinter(hPrinter)

@app.route('/print_barcode', methods=['POST'])
def print_barcode():
    data = request.get_json(force=True)
    barcode_text = data.get("barcode_text")
    
    if not barcode_text:
        return jsonify({"error": "Missing barcode_text"}), 400

    # สร้างรูป
    img = Image.new("RGB", (300, 100), color="white")
    d = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    d.text((10, 40), f"{barcode_text}", font=font, fill=(0, 0, 0))

    file_path = "barcode_output.png"
    img.save(file_path)

    # สั่งพิมพ์
    print_image(file_path)

    return jsonify({"status": "Printed", "barcode": barcode_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


