from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
WINDOWS_AGENT_URL = "http://<WINDOWS_IP>:5001/print"  # เปลี่ยนเป็น IP จริง

@app.route('/print_request', methods=['POST'])
def forward_to_windows():
    data = request.json
    if not data.get("image_url") or not data.get("printer_name"):
        return jsonify({"error": "Missing required parameters"}), 400
    try:
        r = requests.post(WINDOWS_AGENT_URL, json=data, timeout=10)
        return jsonify({"message": "Forwarded", "agent": r.json()}), r.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
