import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

# Generate and load encryption key
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

if not os.path.exists("key.key"):
    generate_key()

key = load_key()
cipher_suite = Fernet(key)

# Functions for password management
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def add_password(website, username, password):
    encrypted_password = encrypt_password(password)
    with open("passwords.txt", "a") as file:
        file.write(f"{website},{username},{encrypted_password}\n")

def retrieve_passwords():
    if not os.path.exists("passwords.txt"):
        return []
    
    with open("passwords.txt", "r") as file:
        passwords = file.readlines()
    
    return [line.strip().split(",") for line in passwords]

# GUI for Password Manager
class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        self.website_label = tk.Label(root, text="Website")
        self.website_label.grid(row=0, column=0)
        self.website_entry = tk.Entry(root)
        self.website_entry.grid(row=0, column=1)

        self.username_label = tk.Label(root, text="Username")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(root, text="Password")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(root)
        self.password_entry.grid(row=2, column=1)

        self.add_button = tk.Button(root, text="Add", command=self.add_password)
        self.add_button.grid(row=3, column=0, columnspan=2)

        self.show_button = tk.Button(root, text="Show Passwords", command=self.show_passwords)
        self.show_button.grid(row=4, column=0, columnspan=2)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            add_password(website, username, password)
            messagebox.showinfo("Success", "Password added successfully")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def show_passwords(self):
        passwords = retrieve_passwords()
        password_window = tk.Toplevel(self.root)
        password_window.title("Stored Passwords")

        for idx, (website, username, encrypted_password) in enumerate(passwords):
            decrypted_password = decrypt_password(encrypted_password)
            tk.Label(password_window, text=f"Website: {website}").grid(row=idx, column=0)
            tk.Label(password_window, text=f"Username: {username}").grid(row=idx, column=1)
            tk.Label(password_window, text=f"Password: {decrypted_password}").grid(row=idx, column=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
