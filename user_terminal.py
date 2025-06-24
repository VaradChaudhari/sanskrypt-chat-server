# user_terminal.py

import os
from auth import login
from encryptor import encrypt_message
from decryptor import decrypt_message

def chat_loop(username):
    while True:
        print("\n[1] Send Message")
        print("[2] Receive Message")
        print("[3] Exit")
        choice = input("Choose: ")

        if choice == "1":
            msg = input("Enter your message: ")
            encrypted = encrypt_message(msg)
            print(f"\n[🔐 ENCRYPTED MESSAGE]:\n{encrypted}")

        elif choice == "2":
            try:
                original = decrypt_message()
                print(f"\n[📥 RECEIVED MESSAGE]:\n{original}")
            except Exception as e:
                print(f"[❌] Error: {e}")
        elif choice == "3":
            break
        else:
            print("[!] Invalid choice")

if __name__ == "__main__":
    user = login()
    if user:
        chat_loop(user)
