# server.py
from flask import Flask, request, jsonify
from decryptor import decrypt_message
from encryptor import encrypt_message
import os
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

HISTORY_FILE = "history.txt"
os.makedirs("session", exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "🛡️ Sanskrypt Encrypted Chat Server Running"

@app.route("/send", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()
        username = data["username"]
        encrypted = data["message"]
        key_package = data["key_package"]

        # Save the encrypted message and key
        with open("session/message.json", "w", encoding="utf-8") as f:
            json.dump({"message": encrypted}, f, ensure_ascii=False, indent=2)
        with open("session/key_package.json", "w", encoding="utf-8") as f:
            json.dump(key_package, f, ensure_ascii=False, indent=2)

        # Decrypt message
        result = decrypt_message()
        save_to_history(result)

        return jsonify({"status": "success", "decrypted": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/history", methods=["GET"])
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return jsonify({"messages": []})
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return jsonify({"messages": [line.strip() for line in lines[-10:]]})

def save_to_history(entry):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
