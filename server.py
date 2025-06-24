from flask import Flask, request, jsonify
from decryptor import decrypt_message
from encryptor import encrypt_message
import os
import json
import base64
import shutil

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

HISTORY_FILE = "history.txt"
SESSION_DIR = "session"

# Ensure session dir exists
os.makedirs(SESSION_DIR, exist_ok=True)

# Helper: Encrypt history line
def encrypt_history_line(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")

# Helper: Decrypt history line
def decrypt_history_line(text):
    return base64.b64decode(text.encode("utf-8")).decode("utf-8")

# Helper: Save to encrypted history file
def save_to_history(entry):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("")

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Auto delete file if over 10 chats
    if len(lines) >= 10:
        os.remove(HISTORY_FILE)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("")

    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(encrypt_history_line(entry) + "\n")

@app.route("/", methods=["GET"])
def home():
    return "🛡️ Sanskrypt Encrypted Chat Server Running"

@app.route("/login", methods=["POST"])
def login_user():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        key_package = data["key_package"]

        # Just log the attempt; you can add real user validation later
        print(f"[LOGIN] {username} authenticated with key: {key_package}")
        return jsonify({"status": "success", "message": "Authenticated"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/send", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()
        username = data["username"]
        encrypted = data["message"]
        key_package = data["key_package"]

        # Save encrypted data to session
        with open(f"{SESSION_DIR}/message.json", "w", encoding="utf-8") as f:
            json.dump({"message": encrypted}, f, ensure_ascii=False, indent=2)
        with open(f"{SESSION_DIR}/key_package.json", "w", encoding="utf-8") as f:
            json.dump(key_package, f, ensure_ascii=False, indent=2)

        # Decrypt message
        result = decrypt_message()

        # Save plain-text message to encrypted history
        save_to_history(result)

        return jsonify({"status": "success", "decrypted": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/history", methods=["GET"])
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return jsonify({"chats": []})

    messages = []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            try:
                decrypted = decrypt_history_line(line.strip())
                if " - " in decrypted:
                    user, msg = decrypted.split(" - ", 1)
                    messages.append({"username": user, "message": msg})
            except Exception as e:
                print(f"[⚠] Failed to decode line: {e}")
    return jsonify({"chats": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
