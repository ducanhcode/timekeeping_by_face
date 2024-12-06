import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import datetime
import os
import subprocess
import threading  # Thêm import threading để sử dụng đa luồng

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Nhận Diện Khuôn Mặt")
        self.root.geometry("800x600")

        # Biến để quản lý luồng video
        self.video_stream = None
        self.running = False

        # Thêm Label và Entry để nhập tên
        self.label_name = tk.Label(root, text="Tên:")
        self.label_name.pack(pady=5)
        self.entry_name = tk.Entry(root)
        self.entry_name.pack(pady=5)

        # Tạo nút mở webcam
        self.btn_open_camera = tk.Button(root, text="Mở Webcam", command=self.open_camera, width=20, height=2)
        self.btn_open_camera.pack(pady=10)

        # Tạo nút quay/dừng
        self.btn_record = tk.Button(root, text="Quay", command=self.toggle_recording, width=20, height=2)
        self.btn_record.pack(pady=10)
        self.btn_record.config(state="disabled")  # Vô hiệu hóa nút quay khi webcam chưa mở

        # Tạo nút CutVideo
        self.btn_cutvideo = tk.Button(root, text="CutVideo", command=self.cut_video, width=20, height=2)
        self.btn_cutvideo.pack(pady=10)

        # Tạo nút Training
        self.btn_training = tk.Button(root, text="Training", command=self.train_model, width=20, height=2)
        self.btn_training.pack(pady=10)

        # Khung để hiển thị video
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Biến để quản lý trạng thái quay video
        self.recording = False
        self.video_writer = None

    def open_camera(self):
        # Kiểm tra nếu webcam chưa được mở
        if not self.running:
            self.video_stream = cv2.VideoCapture(0)
            if not self.video_stream.isOpened():
                messagebox.showerror("Lỗi", "Không thể mở webcam.")
                return
            self.running = True
            self.btn_record.config(state="normal")  # Kích hoạt nút quay
            self.update_frame()

    def update_frame(self):
        # Đọc khung hình từ webcam và hiển thị
        if self.running:
            ret, frame = self.video_stream.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                # Ghi video nếu đang quay
                if self.recording:
                    if self.video_writer is None:
                        # Lấy tên từ ô nhập
                        name = self.entry_name.get().strip()
                        if not name:
                            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên trước khi quay.")
                            self.recording = False
                            self.btn_record.config(text="Quay")
                            return
                        # Tạo thư mục video nếu chưa tồn tại
                        os.makedirs(f"video/{name}", exist_ok=True)
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        video_filename = os.path.join("video", name, f"{timestamp}.mp4")  # Lưu dưới dạng .mp4
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Sử dụng codec mp4v
                        frame_width = int(self.video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
                        frame_height = int(self.video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        self.video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
                        if not self.video_writer.isOpened():
                            messagebox.showerror("Lỗi", "Không thể ghi video. Vui lòng kiểm tra codec và định dạng video.")
                            self.recording = False
                            self.btn_record.config(text="Quay")
                            return
                        # Lưu đường dẫn video vừa quay để sử dụng khi cắt video
                        self.last_video_path = video_filename
                    # Ghi khung hình
                    self.video_writer.write(cv2.cvtColor(cv2image, cv2.COLOR_RGB2BGR))
                else:
                    if self.video_writer is not None:
                        self.video_writer.release()
                        self.video_writer = None

                self.video_label.after(10, self.update_frame)
            else:
                messagebox.showerror("Lỗi", "Không thể nhận khung hình từ webcam.")
                self.close_camera()

    def toggle_recording(self):
        if not self.running:
            messagebox.showwarning("Cảnh báo", "Bạn cần mở webcam trước.")
            return
        self.recording = not self.recording
        if self.recording:
            self.btn_record.config(text="Dừng")
        else:
            self.btn_record.config(text="Quay")
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            messagebox.showinfo("Thông báo", "Video đã được lưu vào thư mục 'video'.")

    def cut_video(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên trước khi cắt video.")
            return
        video_dir = os.path.join("video", name)
        if not os.path.exists(video_dir):
            messagebox.showerror("Lỗi", f"Không tìm thấy thư mục video cho '{name}'.")
            return
        # Tìm video mới nhất trong thư mục
        video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        if not video_files:
            messagebox.showerror("Lỗi", f"Không tìm thấy file video trong thư mục '{video_dir}'.")
            return
        latest_video = max(video_files, key=lambda f: os.path.getmtime(os.path.join(video_dir, f)))
        input_video_path = os.path.join(video_dir, latest_video)
        output_dir = os.path.join("Dataset", "FaceData", "raw", name)
        output_dir_processed = os.path.join("Dataset", "FaceData", "processed", name)
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(output_dir_processed, exist_ok=True)
        try:
            # Thực thi lệnh cắt video
            extract_command = f"python src/face_extract.py --input \"{input_video_path}\" --output \"{output_dir}\""
            subprocess.run(extract_command, check=True, shell=True)
            # Kiểm tra xem dữ liệu đã được tạo hay chưa
            if not os.listdir(output_dir):
                messagebox.showerror("Lỗi", "Không có dữ liệu được tạo ra từ việc cắt video.")
                return
            # Thực thi lệnh căn chỉnh khuôn mặt
            align_command = f"python src/align_dataset_mtcnn.py  Dataset/FaceData/raw Dataset/FaceData/processed --image_size 160 --margin 32  --random_order --gpu_memory_fraction 0.25"
            subprocess.run(align_command, check=True, shell=True)
            messagebox.showinfo("Thông báo", "Cắt video và căn chỉnh khuôn mặt thành công!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi cắt video hoặc căn chỉnh khuôn mặt.\n{e}")

    def train_model(self):
        # Vô hiệu hóa nút Training trong khi huấn luyện
        self.btn_training.config(state="disabled")
        threading.Thread(target=self.run_training_command).start()

    def run_training_command(self):
        command = "python src/classifier.py TRAIN Dataset/FaceData/processed Models/20180402-114759.pb Models/facemodel.pkl --batch_size 1000"
        try:
            subprocess.run(command, check=True, shell=True)
            # Hiển thị thông báo trong luồng chính
            self.root.after(0, lambda: messagebox.showinfo("Thông báo", "Huấn luyện mô hình thành công!"))
        except subprocess.CalledProcessError as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi huấn luyện mô hình.\n{e}"))
        finally:
            # Kích hoạt lại nút Training sau khi hoàn thành
            self.root.after(0, lambda: self.btn_training.config(state="normal"))

    def close_camera(self):
        # Dừng luồng video và giải phóng tài nguyên
        if self.running:
            self.running = False
            if self.video_stream is not None:
                self.video_stream.release()
                self.video_stream = None
            # Xóa hình ảnh khỏi Label
            self.video_label.config(image='')
            # Vô hiệu hóa nút quay
            self.btn_record.config(state="disabled")
            # Nếu đang quay, dừng quay
            if self.recording:
                self.toggle_recording()

    def on_closing(self):
        self.close_camera()
        self.root.destroy()

# Khởi tạo ứng dụng Tkinter
root = tk.Tk()
app = FaceRecognitionApp(root)
root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()
