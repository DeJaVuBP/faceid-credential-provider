import cv2
import dlib
import threading
import numpy as np
import face_recognition
import pyodbc
import subprocess  # ⬅️ Thêm để dùng shutdown /l
from tkinter import messagebox, Tk, simpledialog



class FaceLogin:
    def __init__(self, root, user_name=None):
        self.root = root
        self.user_name = user_name
        self.cap = None
        self.stop_event = threading.Event()
        self.login_success = False

    def login_face(self):
        if not self.user_name or self.user_name == "Unknown":
            self.user_name = simpledialog.askstring("Input", "Enter your user name:", parent=self.root)
            if not self.user_name:
                messagebox.showerror("Error", "User name is required!", parent=self.root)
                self.root.quit()
                return

        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open the camera!", parent=self.root)
                self.root.quit()
                return

            cv2.namedWindow("Face Login")
            self.root.protocol("WM_DELETE_WINDOW", self.stop_face_scan)

            def detect_face():
                if self.stop_event.is_set() or self.login_success:
                    return

                ret, frame = self.cap.read()
                if not ret:
                    self.root.after(10, detect_face)
                    return

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame, model="hog")

                if not face_locations:
                    cv2.putText(frame, "No face detected", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                else:
                    top, right, bottom, left = face_locations[0]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    face_encodings = face_recognition.face_encodings(rgb_frame, [face_locations[0]])
                    if face_encodings:
                        face_encoding = np.array(face_encodings[0], dtype=np.float64).tobytes()
                        if self.verify_face(face_encoding):
                            self.login_success = True
                            self.stop_face_scan()
                            messagebox.showinfo("Success", f"Login successful for {self.user_name}!", parent=self.root)
                            self.root.quit()
                            return
                        else:
                            self.stop_face_scan()
                            messagebox.showerror("Login Failed", "Face not recognized. Returning to login screen.", parent=self.root)
                            self.root.quit()
                            subprocess.run("shutdown /l")  # ⬅️ Đăng xuất về màn hình login
                            return

                cv2.imshow("Face Login", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    self.stop_face_scan()
                    self.root.quit()
                    return

                self.root.after(10, detect_face)

            self.root.after(10, detect_face)

        except Exception as e:
            self.stop_face_scan()
            messagebox.showerror("Error", f"System error: {str(e)}", parent=self.root)
            self.root.quit()

    def verify_face(self, face_encoding):
        try:
            # Kết nối với cơ sở dữ liệu
            with pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=DESKTOP-AHFDNV5\\SQLEXPRESS;'
                    'DATABASE=Face_ID_Management;'
                    'Trusted_Connection=yes;'
            ) as conn:
                with conn.cursor() as cursor:
                    # Truy vấn theo tên người dùng
                    cursor.execute("SELECT Face_ID FROM Users WHERE Name = ?", (self.user_name,))
                    row = cursor.fetchone()

                    # Kiểm tra nếu người dùng tồn tại
                    if row and row[0]:
                        # Giải mã Face_ID lưu trữ trong cơ sở dữ liệu
                        stored_face_encoding = np.frombuffer(row[0], dtype=np.float64)

                        # Kiểm tra xem face_encoding có hợp lệ không
                        if face_encoding is None or len(face_encoding) == 0:
                            print("[ERROR] Invalid face encoding received")
                            return False

                        # So sánh khuôn mặt
                        match = face_recognition.compare_faces([stored_face_encoding],
                                                               np.frombuffer(face_encoding, dtype=np.float64))
                        return match[0]
                    else:
                        print(f"[ERROR] No face encoding found for user: {self.user_name}")
                        return False

        except pyodbc.Error as sql_err:
            print(f"[SQL ERROR] {sql_err}")
            return False
        except Exception as ex:
            print(f"[SYSTEM ERROR] {ex}")
            return False

    def stop_face_scan(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.stop_event.set()


if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính nếu không dùng giao diện chính

    user_name = simpledialog.askstring("Input", "Enter your username:", parent=root)
    if not user_name:
        messagebox.showerror("Error", "Username is required!", parent=root)
        root.quit()
    else:
        app = FaceLogin(root, user_name)  # Khởi tạo với user_name thay vì user_no
        app.login_face()

    root.mainloop()

