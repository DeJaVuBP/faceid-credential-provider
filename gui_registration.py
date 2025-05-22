import tkinter as tk
from tkinter import messagebox
from face_registration import FaceRegistration

def start_register():
    def on_submit():
        user_name = entry.get()
        if user_name:
            register_window.destroy()
            app = FaceRegistration(root, user_name=user_name)
            app.register_face_id()
        else:
            messagebox.showwarning("Warning", "Please enter your name.")

    def on_cancel():
        register_window.destroy()

    register_window = tk.Toplevel(root)
    register_window.title("Register User")
    register_window.geometry("400x200")
    register_window.grab_set()

    label = tk.Label(register_window, text="Enter your name to register:", font=("Helvetica", 14))
    label.pack(pady=20)

    entry = tk.Entry(register_window, font=("Helvetica", 14), width=30)
    entry.pack()
    entry.focus()

    btn_frame = tk.Frame(register_window)
    btn_frame.pack(pady=20)

    submit_btn = tk.Button(btn_frame, text="Register", font=("Helvetica", 12), command=on_submit, width=10)
    submit_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tk.Button(btn_frame, text="Cancel", font=("Helvetica", 12), command=on_cancel, width=10)
    cancel_btn.pack(side=tk.LEFT, padx=10)


# Giao diện chính
root = tk.Tk()
root.title("Face ID System")
root.geometry("320x250")
root.resizable(False, False)

title_label = tk.Label(root, text="Face ID System", font=("Helvetica", 18, "bold"))
title_label.pack(pady=25)

btn_register = tk.Button(root, text="Register with Face", width=25, height=2, font=("Helvetica", 12), command=start_register)
btn_register.pack(pady=10)

root.mainloop()
