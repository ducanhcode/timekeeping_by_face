import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from makedatades import Ui_MainWindow  # Import lớp giao diện từ makedatades.py
import cv2
from PyQt6.QtGui import QImage, QPixmap
import datetime
import os
import subprocess
import threading

class FaceRecognitionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(FaceRecognitionApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Cập nhật văn bản cho các thành phần giao diện
        self.setWindowTitle("Ứng dụng Nhận Diện Khuôn Mặt")
        self.ui.label.setText("Nhập Họ Và Tên:")
        self.ui.btn_open_camera.setText("Mở Webcam")
        self.ui.btn_record.setText("Quay")
        self.ui.btn_cutvideo.setText("Cắt Video")
        self.ui.btn_Train.setText("Training")
        self.ui.label_video.setText("")

        # Vô hiệu hóa nút Quay khi webcam chưa mở
        self.ui.btn_record.setEnabled(False)

        # Kết nối các nút với các chức năng
        self.ui.btn_open_camera.clicked.connect(self.open_camera)
        self.ui.btn_record.clicked.connect(self.toggle_recording)
        self.ui.btn_cutvideo.clicked.connect(self.cut_video)
        self.ui.btn_Train.clicked.connect(self.train_model)

        # Biến để quản lý trạng thái
        self.video_stream = None
        self.running = False
        self.recording = False
        self.video_writer = None

        # Timer để cập nhật khung hình
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)

    def open_camera(self):
        if not self.running:
            self.video_stream = cv2.VideoCapture(0)
            if not self.video_stream.isOpened():
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể mở webcam.")
                return
            self.running = True
            self.ui.btn_record.setEnabled(True)
            self.timer.start(20)

    def update_frame(self):
        if self.running:
            ret, frame = self.video_stream.read()
            if ret:
                # Chuyển đổi khung hình để hiển thị
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = cv2image.shape
                bytesPerLine = 3 * width
                qimg = QImage(cv2image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.ui.label_video.setPixmap(pixmap)

                # Ghi video nếu đang quay
                if self.recording:
                    if self.video_writer is None:
                        # Lấy tên từ ô nhập
                        name = self.ui.lineEdit.text().strip()
                        if not name:
                            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên trước khi quay.")
                            self.recording = False
                            self.ui.btn_record.setText("Quay")
                            return
                        # Tạo thư mục video nếu chưa tồn tại
                        os.makedirs(f"video/{name}", exist_ok=True)
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        video_filename = os.path.join("video", name, f"{timestamp}.mp4")
                        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                        frame_width = int(self.video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
                        frame_height = int(self.video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        self.video_writer = cv2.VideoWriter(video_filename, fourcc, 20.0, (frame_width, frame_height))
                        if not self.video_writer.isOpened():
                            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể ghi video. Vui lòng kiểm tra codec và định dạng video.")
                            self.recording = False
                            self.ui.btn_record.setText("Quay")
                            return
                        # Lưu đường dẫn video vừa quay
                        self.last_video_path = video_filename
                    # Ghi khung hình vào video
                    self.video_writer.write(frame)
                else:
                    if self.video_writer is not None:
                        self.video_writer.release()
                        self.video_writer = None
            else:
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Không thể nhận khung hình từ webcam.")
                self.close_camera()

    def toggle_recording(self):
        if not self.running:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Bạn cần mở webcam trước.")
            return
        self.recording = not self.recording
        if self.recording:
            self.ui.btn_record.setText("Dừng")
        else:
            self.ui.btn_record.setText("Quay")
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            QtWidgets.QMessageBox.information(self, "Thông báo", "Video đã được lưu vào thư mục 'video'.")

    def cut_video(self):
        name = self.ui.lineEdit.text().strip()
        if not name:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên trước khi cắt video.")
            return
        video_dir = os.path.join("video", name)
        if not os.path.exists(video_dir):
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không tìm thấy thư mục video cho '{name}'.")
            return
        # Tìm video mới nhất trong thư mục
        video_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
        if not video_files:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Không tìm thấy file video trong thư mục '{video_dir}'.")
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
            # Kiểm tra xem dữ liệu đã được tạo ra chưa
            if not os.listdir(output_dir):
                QtWidgets.QMessageBox.critical(self, "Lỗi", "Không có dữ liệu được tạo ra từ việc cắt video.")
                return
            # Thực thi lệnh căn chỉnh khuôn mặt
            align_command = f"python src/align_dataset_mtcnn.py Dataset/FaceData/raw Dataset/FaceData/processed --image_size 160 --margin 32 --random_order --gpu_memory_fraction 0.25"
            subprocess.run(align_command, check=True, shell=True)
            QtWidgets.QMessageBox.information(self, "Thông báo", "Cắt video và căn chỉnh khuôn mặt thành công!")
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi cắt video hoặc căn chỉnh khuôn mặt.\n{e}")

    def train_model(self):
        # Vô hiệu hóa nút Training trong khi huấn luyện
        self.ui.btn_Train.setEnabled(False)
        threading.Thread(target=self.run_training_command).start()

    def run_training_command(self):
        command = "python src/classifier.py TRAIN Dataset/FaceData/processed Models/20180402-114759.pb Models/facemodel.pkl --batch_size 1000"
        try:
            subprocess.run(command, check=True, shell=True)
            # Hiển thị thông báo trong luồng chính
            QtCore.QTimer.singleShot(0, lambda: QtWidgets.QMessageBox.information(self, "Thông báo", "Huấn luyện mô hình thành công!"))
        except subprocess.CalledProcessError as e:
            error_message = str(e)
            QtCore.QTimer.singleShot(0, lambda: QtWidgets.QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi huấn luyện mô hình.\n{error_message}"))
        finally:
            # Kích hoạt lại nút Training sau khi hoàn thành
            QtCore.QTimer.singleShot(0, lambda: self.ui.btn_Train.setEnabled(True))

    def close_camera(self):
        if self.running:
            self.running = False
            self.timer.stop()
            if self.video_stream is not None:
                self.video_stream.release()
                self.video_stream = None
            self.ui.label_video.clear()
            self.ui.btn_record.setEnabled(False)
            if self.recording:
                self.toggle_recording()

    def closeEvent(self, event):
        self.close_camera()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
