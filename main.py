# main.py
from auth import login
from encryptor import encrypt_message
from decryptor import decrypt_message
import os
import shutil
import base64

active_users = []

def start_session():
    if not os.path.exists("session"):
        os.mkdir("session")
    if not os.path.exists("history.txt"):
        with open("history.txt", "w", encoding="utf-8") as f:
            f.write("")

def destroy_session():
    if os.path.exists("session"):
        shutil.rmtree("session")

def encrypt_history_line(text):
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")

def decrypt_history_line(text):
    return base64.b64decode(text.encode("utf-8")).decode("utf-8")

def save_to_history(entry):
    if not os.path.exists("history.txt"):
        with open("history.txt", "w", encoding="utf-8") as f:
            f.write("")

    with open("history.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    if len(lines) >= 10:
        os.remove("history.txt")
        with open("history.txt", "w", encoding="utf-8") as f:
            f.write("")

    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(encrypt_history_line(entry) + "\n")

def show_history():
    if not os.path.exists("history.txt"):
        print("[📜] No history available.")
        return
    with open("history.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            print("[📜] No messages yet.")
            return
        print("\n[📜 LAST 10 MESSAGES]:")
        for line in lines:
            try:
                print(decrypt_history_line(line.strip()))
            except:
                print("[⚠] Error decoding line.")

def chat_loop(username):
    if username not in active_users:
        active_users.append(username)
        print(f"[👤] {username.upper()} joined the chat.")
    start_session()

    try:
        while True:
            print("\n[1] Send Message")
            print("[2] Receive Message")
            print("[3] Exit")
            print("[4] View Last 10 Messages")
            choice = input("Choose: ").strip()

            if choice == "1":
                msg = input("Your message: ")
                encrypted = encrypt_message(username, msg)
                print(f"[🔐 Encrypted] {username} - {encrypted}")
                save_to_history(f"{username} - {msg}")

            elif choice == "2":
                result = decrypt_message()
                print(f"[📩] {result}")
                if " - " in result:
                    save_to_history(result)

            elif choice == "3":
                print(f"[👋] {username.upper()} left the chat.")
                active_users.remove(username)
                if not active_users:
                    destroy_session()
                break

            elif choice == "4":
                show_history()

            else:
                print("[!] Invalid option")

    except KeyboardInterrupt:
        print("\n[⚠] Interrupted")
        active_users.remove(username)
        if not active_users:
            destroy_session()

if __name__ == "__main__":
    user = login()
    if user:
        chat_loop(user)
