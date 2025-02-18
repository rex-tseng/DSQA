from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 你的 Figma API Key（在 Railway 環境變數設定）
FIGMA_API_KEY = "figd_FA2D6DIhpL6S6RY8sbA6YaLZQUO1vZkCuq0GJgug"
HEADERS = {"X-Figma-Token": FIGMA_API_KEY}

# 讀取 Figma 設計數據
def get_figma_data(file_id, node_id=None):
    url = f"https://api.figma.com/v1/files/{file_id}"
    if node_id:
        url += f"/nodes?ids={node_id}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# API 端點：讓 GPTs 請求 Figma 設計數據
@app.route("/check_ui", methods=["GET"])
def check_ui():
    file_id = request.args.get("file_id")
    node_id = request.args.get("node_id", None)

    if not file_id:
        return jsonify({"error": "Missing file_id"}), 400
    
    ui_data = get_figma_data(file_id, node_id)
    return jsonify({"UI Data": ui_data})

# 啟動 Flask 伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
