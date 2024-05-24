import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from cryptography.fernet import Fernet
import os
import string
import random

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

def generate_secure_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(random.choice(characters) for _ in range(length))
    return secure_password

# GUI for Password Manager
class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        # Set the style
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.website_label = ttk.Label(self.mainframe, text="Website")
        self.website_label.grid(row=0, column=0, pady=5, sticky=tk.W)
        self.website_entry = ttk.Entry(self.mainframe, width=25)
        self.website_entry.grid(row=0, column=1, pady=5, sticky=(tk.W, tk.E))

        self.username_label = ttk.Label(self.mainframe, text="Username")
        self.username_label.grid(row=1, column=0, pady=5, sticky=tk.W)
        self.username_entry = ttk.Entry(self.mainframe, width=25)
        self.username_entry.grid(row=1, column=1, pady=5, sticky=(tk.W, tk.E))

        self.password_label = ttk.Label(self.mainframe, text="Password")
        self.password_label.grid(row=2, column=0, pady=5, sticky=tk.W)
        self.password_entry = ttk.Entry(self.mainframe, width=25, show="*")
        self.password_entry.grid(row=2, column=1, pady=5, sticky=(tk.W, tk.E))

        self.add_button = ttk.Button(self.mainframe, text="Add", command=self.add_password)
        self.add_button.grid(row=3, column=0, pady=10, columnspan=2)

        self.show_button = ttk.Button(self.mainframe, text="Show Passwords", command=self.show_passwords)
        self.show_button.grid(row=4, column=0, pady=10, columnspan=2)

        self.generate_button = ttk.Button(self.mainframe, text="Generate Secure Password", command=self.generate_password)
        self.generate_button.grid(row=5, column=0, pady=10, columnspan=2)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if website and username and password:
            add_password(website, username, password)
            messagebox.showinfo("Success", "Password added successfully")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def generate_password(self):
        secure_password = generate_secure_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, secure_password)
        messagebox.showinfo("Generated Password", f"Generated secure password: {secure_password}")

    def show_passwords(self):
        passwords = retrieve_passwords()
        password_window = tk.Toplevel(self.root)
        password_window.title("Stored Passwords")

        for idx, (website, username, encrypted_password) in enumerate(passwords):
            decrypted_password = decrypt_password(encrypted_password)
            ttk.Label(password_window, text=f"Website: {website}").grid(row=idx, column=0, padx=5, pady=2)
            ttk.Label(password_window, text=f"Username: {username}").grid(row=idx, column=1, padx=5, pady=2)
            ttk.Label(password_window, text=f"Password: {decrypted_password}").grid(row=idx, column=2, padx=5, pady=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
