# decryptor.py
import json
import base64
from Crypto.Cipher import AES
import os
import shutil

def unpad(s):
    pad_len = ord(s[-1])
    return s[:-pad_len]

def decrypt_message():
    try:
        with open("session/key_package.json", "r", encoding="utf-8") as f:
            key_package = json.load(f)
        with open("session/message.json", "r", encoding="utf-8") as f:
            msg_data = json.load(f)

        aes_key = base64.b64decode(key_package["aes_key"])
        reverse_map = {v: k for k, v in key_package["lang_map"].items()}
        sender = key_package["sender"]
        encrypted = msg_data["message"]
        byte_values = bytes([int(reverse_map[c]) for c in encrypted])
        ciphertext = bytes(byte_values)

        cipher = AES.new(aes_key, AES.MODE_ECB)
        decrypted_bytes = cipher.decrypt(ciphertext)
        message = decrypted_bytes.decode("utf-8")
        plain = unpad(message)

        return f"{sender} - {plain}"
    except Exception as e:
        return f"[❌] Decryption failed: {e}"
