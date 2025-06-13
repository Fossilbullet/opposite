import os
from flask import Flask, request, jsonify
import http.client
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://a-i-face-video-generator-wnb1vi.flutterflow.app/"])

@app.route('/get-task-status', methods=['GET'])
def get_task_status():
    API_KEY = os.getenv("PIAPI_API_KEY")
    if not API_KEY:
        return jsonify({"error": "API key not set in environment"}), 500

    task_id = request.args.get("task_id")
    if not task_id:
        return jsonify({"error": "Missing task_id parameter"}), 400
    
    conn = http.client.HTTPSConnection("api.piapi.ai")
    headers = {
        'x-api-key': API_KEY
    }

    try:
        conn.request("GET", f"/api/v1/task/{task_id}", headers=headers)
        res = conn.getresponse()
        response_data = res.read().decode("utf-8")
        return jsonify(json.loads(response_data))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Render requires listening on 0.0.0.0 and the port from the PORT environment variable
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
