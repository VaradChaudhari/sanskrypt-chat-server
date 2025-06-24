from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

HISTORY_FILE = "history.txt"
os.makedirs("session", exist_ok=True)

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

        print(f"[LOGIN] {username} connected with key_package: {key_package}")

        return jsonify({"status": "success", "message": "Authenticated."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/send", methods=["POST"])
def receive_message():
    try:
        data = request.get_json()
        username = data["username"]
        message = data["message"]
        key_package = data["key_package"]

        # Save encrypted message and key
        with open("session/message.json", "w", encoding="utf-8") as f:
            json.dump({"message": message}, f, ensure_ascii=False, indent=2)
        with open("session/key_package.json", "w", encoding="utf-8") as f:
            json.dump(key_package, f, ensure_ascii=False, indent=2)

        # Combine username with encrypted message
        entry = f"{username} - {message}"
        save_to_history(entry)

        return jsonify({"status": "success", "decrypted": entry})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/history", methods=["GET"])
def get_history():
    if not os.path.exists(HISTORY_FILE):
        return jsonify({"messages": []})
    
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Return last 10 full lines (username + encrypted message)
    return jsonify({"messages": [line.strip() for line in lines[-10:]]})

def save_to_history(entry):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry.strip() + "\n")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
