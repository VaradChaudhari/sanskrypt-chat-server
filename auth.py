# auth.py
users = {
    "varad": "1234",
    "pranav": "5678",
    "amit": "2345"
}

def login():
    print("===== SANSKRYPT LOGIN =====")
    username = input("Username: ").strip().lower()
    password = input("PIN: ").strip()
    if username in users and users[username] == password:
        print(f"[✅] Welcome, {username.upper()}!")
        return username
    else:
        print("[❌] Invalid credentials.")
        return None
