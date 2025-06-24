# encryptor.py
import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from lang_map import generate_language_map
import os
import shutil

def pad(msg):
    pad_len = 16 - len(msg.encode('utf-8')) % 16
    return msg + chr(pad_len) * pad_len

def encrypt_message(username, message):
    # ✅ Delete old session to prevent map mismatch
    if os.path.exists("session"):
        shutil.rmtree("session")
    os.makedirs("session", exist_ok=True)

    # Generate AES key and cipher
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    padded = pad(message)
    ciphertext = cipher.encrypt(padded.encode("utf-8"))

    # Generate a fresh random language map
    lang_map = generate_language_map()

    # Map encrypted bytes to characters
    encrypted_text = ''.join([lang_map[str(b)] for b in ciphertext])

    # Save encryption data
    key_package = {
        "aes_key": base64.b64encode(key).decode(),
        "lang_map": lang_map,
        "sender": username
    }

    with open("session/key_package.json", "w", encoding="utf-8") as f:
        json.dump(key_package, f, ensure_ascii=False, indent=2)

    with open("session/message.json", "w", encoding="utf-8") as f:
        json.dump({"message": encrypted_text}, f, ensure_ascii=False, indent=2)

    return encrypted_text
