import tkinter as tk
from tkinter import messagebox
from face_login import FaceLogin
import logging
import os

# Thiết lập ghi log
log_path = os.path.join(os.path.dirname(__file__), "gui_login.log")
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def start_login():
    def on_submit():
        user_name = entry.get()
        if user_name:
            logging.info(f"Attempting login with name: {user_name}")
            login_window.destroy()
            try:
                app = FaceLogin(root, user_name)
                app.login_face()
            except Exception as e:
                logging.error(f"Login failed: {str(e)}")
                messagebox.showerror("Error", f"Login failed: {str(e)}")
        else:
            logging.warning("Login attempted with empty name.")
            messagebox.showwarning("Warning", "Please enter your name.")

    def on_cancel():
        logging.info("Login canceled by user.")
        login_window.destroy()

    login_window = tk.Toplevel(root)
    login_window.title("Enter Your Name")
    login_window.geometry("400x200")
    login_window.grab_set()

    label = tk.Label(login_window, text="Enter your name to login:", font=("Helvetica", 14))
    label.pack(pady=20)

    entry = tk.Entry(login_window, font=("Helvetica", 14), width=30)
    entry.pack()
    entry.focus()

    btn_frame = tk.Frame(login_window)
    btn_frame.pack(pady=20)

    submit_btn = tk.Button(btn_frame, text="Login", font=("Helvetica", 12), command=on_submit, width=10)
    submit_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tk.Button(btn_frame, text="Cancel", font=("Helvetica", 12), command=on_cancel, width=10)
    cancel_btn.pack(side=tk.LEFT, padx=10)

# Giao diện chính
root = tk.Tk()
root.title("Face ID System")
root.geometry("320x220")
root.resizable(False, False)

title_label = tk.Label(root, text="Face ID System", font=("Helvetica", 18, "bold"))
title_label.pack(pady=25)

btn_login = tk.Button(root, text="Login with Face", width=25, height=2, font=("Helvetica", 12), command=start_login)
btn_login.pack(pady=10)

logging.info("GUI started.")
root.mainloop()
