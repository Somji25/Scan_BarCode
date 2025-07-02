from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# เปลี่ยนเป็น IP หรือ URL ของ Windows Agent จริง ๆ
WINDOWS_AGENT_URL = "http://10.215.102.125:5001/print"

@app.route('/print_request', methods=['POST'])
def forward_to_windows():
    data = request.json
    # ตรวจสอบ parameter เบื้องต้น
    if not data.get("image_url") or not data.get("printer_name"):
        return jsonify({"error": "Missing required parameters"}), 400
    try:
        # ส่งคำขอไปยัง Windows Agent
        r = requests.post(WINDOWS_AGENT_URL, json=data, timeout=10)
        return jsonify({"message": "Forwarded", "agent_response": r.json()}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # port 5000 หรือพอร์ตที่ Render กำหนด
