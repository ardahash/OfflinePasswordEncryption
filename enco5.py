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

def delete_password(website, username):
    passwords = retrieve_passwords()
    with open("passwords.txt", "w") as file:
        for line in passwords:
            if line[0] == website and line[1] == username:
                continue
            file.write(",".join(line) + "\n")

def update_password(old_website, old_username, new_website, new_username, new_password):
    passwords = retrieve_passwords()
    with open("passwords.txt", "w") as file:
        for line in passwords:
            if line[0] == old_website and line[1] == old_username:
                encrypted_password = encrypt_password(new_password)
                file.write(f"{new_website},{new_username},{encrypted_password}\n")
            else:
                file.write(",".join(line) + "\n")

# GUI for Password Manager
class PasswordManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Hurbas Simple Offline Password Manager")

        # set the size of the window
        

        # Set the style
        style = ttk.Style()
        style.theme_use('clam')  # Use the 'clam' theme
        style.configure(".", background="black", foreground="white")  # Set background and foreground color for all elements
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        self.root.geometry("800x600")
        self.root.configure(bg='black')


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

        self.tree = ttk.Treeview(password_window, columns=("Website", "Username", "Password"), show="headings")
        self.tree.heading("Website", text="Website")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.column("Website", width=200)
        self.tree.column("Username", width=200)
        self.tree.column("Password", width=200)

        for website, username, encrypted_password in passwords:
            decrypted_password = decrypt_password(encrypted_password)
            self.tree.insert("", "end", values=(website, username, decrypted_password))

        self.tree.pack(fill=tk.BOTH, expand=True)

        self.delete_button = ttk.Button(password_window, text="Delete Selected", command=self.delete_selected)
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.modify_button = ttk.Button(password_window, text="Modify Selected", command=self.modify_selected)
        self.modify_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def delete_selected(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")
        website, username, _ = values
        delete_password(website, username)
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Password deleted successfully")

    def modify_selected(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, "values")
        old_website, old_username, old_password = values

        def save_modification():
            new_website = website_entry.get()
            new_username = username_entry.get()
            new_password = password_entry.get()
            if new_website and new_username and new_password:
                update_password(old_website, old_username, new_website, new_username, new_password)
                messagebox.showinfo("Success", "Password modified successfully")
                modification_window.destroy()
                self.tree.item(selected_item, values=(new_website, new_username, new_password))
            else:
                messagebox.showwarning("Input Error", "Please fill all fields")

        modification_window = tk.Toplevel(self.root)
        modification_window.title("Modify Password")

        ttk.Label(modification_window, text="Website").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        website_entry = ttk.Entry(modification_window, width=25)
        website_entry.grid(row=0, column=1, padx=10, pady=5)
        website_entry.insert(0, old_website)

        ttk.Label(modification_window, text="Username").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        username_entry = ttk.Entry(modification_window, width=25)
        username_entry.grid(row=1, column=1, padx=10, pady=5)
        username_entry.insert(0, old_username)

        ttk.Label(modification_window, text="Password").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        password_entry = ttk.Entry(modification_window, width=25, show="*")
        password_entry.grid(row=2, column=1, padx=10, pady=5)
        password_entry.insert(0, old_password)

        save_button = ttk.Button(modification_window, text="Save", command=save_modification)
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManager(root)
    root.mainloop()
