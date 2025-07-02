from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

LOCAL_PC_API_URL = "http://127.0.0.1:6000/print"  # เปลี่ยนเป็น IP และ port เครื่อง Local PC

@app.route('/print_barcode', methods=['POST'])
def print_barcode():
    data = request.json
    image_base64 = data.get('imageBase64')
    printer_name = data.get('printer_name')

    if not image_base64 or not printer_name:
        return jsonify({"error": "Missing imageBase64 or printer_name"}), 400

    # ส่งข้อมูลต่อไปยัง Local PC API
    payload = {
        "imageBase64": image_base64,
        "printer_name": printer_name
    }

    try:
        resp = requests.post(LOCAL_PC_API_URL, json=payload, timeout=10)
        if resp.status_code == 200:
            return jsonify({"status": "sent to local pc", "response": resp.json()})
        else:
            return jsonify({"status": "error from local pc", "detail": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"status": "error sending to local pc", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

