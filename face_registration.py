import cv2
import dlib
import threading
import numpy as np
import face_recognition
import pyodbc
from tkinter import messagebox, Tk
from imutils import face_utils
import tkinter.simpledialog as simpledialog


class FaceRegistration:
    def __init__(self, root, user_name=None):
        self.root = root
        self.user_no = None  # Khởi tạo user_no là None
        self.user_name = user_name
        self.cap = None
        self.stop_event = threading.Event()
        self.face_saved = False

    def register_face_id(self):
        if not self.user_name:
            messagebox.showerror("Error", "Cannot register face without a user name!", parent=self.root)
            self.root.quit()
            return

        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot open the camera!", parent=self.root)
                self.root.quit()
                return

            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor("D:/HK2_2025/DACN_Project/shape_predictor_68_face_landmarks/shape_predictor_68_face_landmarks.dat")

            cv2.namedWindow("Face Scanning")

            self.prev_face_location = None
            self.prev_light_intensity = None
            self.blink_count = 0
            self.eye_closed_frames = 0
            self.no_movement_frames = 0
            self.no_light_change_frames = 0

            def calculate_ear(eye):
                A = np.linalg.norm(eye[1] - eye[5])
                B = np.linalg.norm(eye[2] - eye[4])
                C = np.linalg.norm(eye[0] - eye[3])
                return (A + B) / (2.0 * C)

            def detect_liveness():
                if self.stop_event.is_set() or self.face_saved:
                    return

                ret, frame = self.cap.read()
                if not ret:
                    return

                frame = cv2.resize(frame, (640, 480))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_frame, model="hog")
                if not face_locations:
                    cv2.putText(frame, "No face detected", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow("Face Scanning", frame)
                    self.root.after(10, detect_liveness)
                    return

                top, right, bottom, left = face_locations[0]
                offset = 25
                top = max(0, top - offset)
                bottom = min(frame.shape[0], bottom + offset)
                left = max(0, left - offset)
                right = min(frame.shape[1], right + offset)

                face_crop = frame[top:bottom, left:right]
                if face_crop.shape[0] > 0 and face_crop.shape[1] > 0:
                    cv2.imshow("Cropped Face", face_crop)
                cv2.rectangle(frame, (left, top), (right, bottom), (34, 139, 34), 2)

                sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
                if sharpness < 50:
                    self.stop_face_scan()
                    messagebox.showerror("Warning", "Detected a printed photo! Please use a real face.", parent=self.root)
                    self.root.quit()
                    return

                light_intensity = np.mean(gray[top:bottom, left:right])
                if self.prev_light_intensity is not None:
                    if abs(light_intensity - self.prev_light_intensity) < 5:
                        self.no_light_change_frames += 1
                    else:
                        self.no_light_change_frames = 0
                    if self.no_light_change_frames >= 60:
                        self.stop_face_scan()
                        messagebox.showerror("Warning", "No lighting change detected!", parent=self.root)
                        self.root.quit()
                        return
                self.prev_light_intensity = light_intensity

                if self.prev_face_location is not None:
                    dx = abs(self.prev_face_location[3] - left) + abs(self.prev_face_location[1] - right)
                    dy = abs(self.prev_face_location[0] - top) + abs(self.prev_face_location[2] - bottom)
                    if dx < 25 and dy < 25:
                        self.no_movement_frames += 1
                    else:
                        self.no_movement_frames = 0
                    if self.no_movement_frames >= 30:
                        self.stop_face_scan()
                        messagebox.showerror("Warning", "No movement detected!", parent=self.root)
                        self.root.quit()
                        return
                self.prev_face_location = face_locations[0]

                rects = detector(gray, 0)
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    leftEye = shape[36:42]
                    rightEye = shape[42:48]
                    ear = (calculate_ear(leftEye) + calculate_ear(rightEye)) / 2.0
                    if ear < 0.22:
                        self.eye_closed_frames += 1
                    else:
                        if self.eye_closed_frames >= 2:
                            self.blink_count += 1
                            self.eye_closed_frames = 0

                if self.blink_count >= 3:
                    image_path = f"face_data/{self.user_no}.png"
                    cv2.imwrite(image_path, face_crop)
                    face_encoding = self.encode_face(rgb_frame, face_locations, face_crop)
                    if face_encoding and self.save_face_to_db(face_encoding):
                        self.face_saved = True
                        self.stop_face_scan()
                        messagebox.showinfo("Success", f"Face saved for {self.user_no}!", parent=self.root)
                        self.root.quit()
                        return
                    else:
                        self.stop_face_scan()
                        messagebox.showerror("Error", "Failed to save data to the database!", parent=self.root)
                        self.root.quit()
                        return

                cv2.putText(frame, f"Blinks: {self.blink_count}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.putText(frame, f"Sharpness: {int(sharpness)}", (20, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                cv2.imshow("Face Scanning", frame)

                self.root.after(10, detect_liveness)

            self.root.after(10, detect_liveness)
            self.root.protocol("WM_DELETE_WINDOW", self.stop_face_scan)

        except Exception as e:
            self.stop_face_scan()
            messagebox.showerror("Error", f"System error: {str(e)}", parent=self.root)
            self.root.quit()

    def encode_face(self, rgb_frame, face_locations, cropped_face=None):
        try:
            if cropped_face is not None and cropped_face.shape[0] > 0 and cropped_face.shape[1] > 0:
                face_crop_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
                cropped_encoding = face_recognition.face_encodings(face_crop_rgb)
                if cropped_encoding:
                    return np.array(cropped_encoding[0], dtype=np.float64).tobytes()
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_frame, [face_locations[0]])
                if face_encodings:
                    return np.array(face_encodings[0], dtype=np.float64).tobytes()
        except Exception as e:
            print(f"[ERROR] Face encoding error: {e}")
        return None

    def save_face_to_db(self, face_encoding):
        if not face_encoding:
            messagebox.showerror("Error", "Missing face encoding", parent=self.root)
            return False

        conn = None
        cursor = None
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-AHFDNV5\\SQLEXPRESS;'
                'DATABASE=Face_ID_Management;'
                'Trusted_Connection=yes;'
            )
            cursor = conn.cursor()

            # Nếu self.user_no có -> cập nhật. Ngược lại -> thêm mới
            if self.user_no:
                cursor.execute("SELECT COUNT(*) FROM Users WHERE user_no = ?", (self.user_no,))
                exists = cursor.fetchone()[0] > 0
            else:
                exists = False

            if exists:
                cursor.execute(
                    "UPDATE Users SET Face_ID = ? WHERE user_no = ?",
                    (pyodbc.Binary(face_encoding), self.user_no)
                )
            else:
                if not self.user_name:
                    self.user_name = simpledialog.askstring("Input", "Enter user name:", parent=self.root)
                    if not self.user_name:
                        messagebox.showerror("Error", "User name is required!", parent=self.root)
                        return False

                cursor.execute(
                    "INSERT INTO Users (Name, Face_ID) VALUES (?, ?)",
                    (self.user_name, pyodbc.Binary(face_encoding))
                )

                # Lấy lại user_no vừa thêm
                cursor.execute("SELECT SCOPE_IDENTITY()")
                self.user_no = cursor.fetchone()[0]

            conn.commit()
            return True

        except Exception as ex:
            print(f"[DB ERROR] {type(ex).__name__}: {ex}")
            return False
        finally:
            try:
                if cursor: cursor.close()
                if conn: conn.close()
            except:
                pass

    def stop_face_scan(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        self.stop_event.set()


if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ chính nếu không dùng giao diện chính

    app = FaceRegistration(root)  # Không cần truyền user_no
    app.register_face_id()

    root.mainloop()


