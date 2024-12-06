import sys
import os
import csv
import subprocess
import time
from datetime import datetime
import pickle
import argparse

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer

import cv2
import numpy as np
import imutils
import tensorflow as tf
tf.compat.v1.disable_eager_execution()  # Tắt eager execution nếu TF 2.x
import facenet
import align.detect_face

from pymongo import MongoClient

# Hàm ghi dữ liệu vào file CSV
def save_to_csv(name):
    with open('recognition_log.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([name, now])

# Lớp giao diện được sinh ra từ file .ui (đã cho sẵn)
from testmongodes import Ui_MainWindow

class FaceRecognitionApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(FaceRecognitionApp, self).__init__(parent)
        self.setupUi(self)

        # Kết nối nút với chức năng
        self.pushButton.clicked.connect(self.check_in)     # Nút Check-in
        self.pushButton_2.clicked.connect(self.check_out)  # Nút Check-out

        # Nếu có thêm nút "Kiểm tra" trong giao diện
        # self.pushButton_3.clicked.connect(self.check_image)
        # Đảm bảo bạn đã thêm nút này vào UI và đặt tên pushButton_3

        # Kết nối đến MongoDB
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client['face_recognition']
            self.checkin_collection = self.db['checkins']
            self.checkout_collection = self.db['checkouts']
            print("Kết nối đến MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")

        # Khởi tạo camera
        self.cap = cv2.VideoCapture(0)
        time.sleep(2.0)

        # Khởi tạo các tham số nhận diện khuôn mặt
        self.MINSIZE = 20
        self.THRESHOLD = [0.6, 0.7, 0.7]
        self.FACTOR = 0.709
        self.IMAGE_SIZE = 182
        self.INPUT_IMAGE_SIZE = 160
        self.CLASSIFIER_PATH = 'Models/facemodel.pkl'
        self.FACENET_MODEL_PATH = 'Models/20180402-114759.pb'

        # Load model phân loại
        with open(self.CLASSIFIER_PATH, 'rb') as file:
            self.model, self.class_names = pickle.load(file)
        print("Custom Classifier Loaded Successfully")

        # Thiết lập TensorFlow Session
        self.sess = tf.compat.v1.Session()
        with self.sess.as_default():
            print('Loading feature extraction model')
            facenet.load_model(self.FACENET_MODEL_PATH)

            self.images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            self.embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
            self.phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
            self.embedding_size = self.embeddings.get_shape()[1]

            # Tạo network MTCNN
            self.pnet, self.rnet, self.onet = align.detect_face.create_mtcnn(self.sess, "src/align")

        # Đặt Timer để cập nhật hình ảnh từ camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Cập nhật ~33fps

        self.current_name = "Unknown"
        self.current_frame_image = None

    def check_image(self):
        # Chạy lệnh python src/checkimage.py
        try:
            subprocess.run(["python", "src/checkimage.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi chạy checkimage.py: {e}")

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return
        frame = imutils.resize(frame, width=600)
        frame = cv2.flip(frame, 1)
        self.current_frame_image = frame.copy()

        # Nhận diện khuôn mặt
        bounding_boxes, _ = align.detect_face.detect_face(
            frame, self.MINSIZE, self.pnet, self.rnet, self.onet, self.THRESHOLD, self.FACTOR
        )

        faces_found = bounding_boxes.shape[0]
        try:
            if faces_found > 1:
                cv2.putText(frame, "Only one face", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (255, 255, 255), thickness=1, lineType=2)
                self.current_name = "Unknown"
            elif faces_found > 0:
                det = bounding_boxes[:, 0:4]
                bb = np.zeros((faces_found, 4), dtype=np.int32)
                for i in range(faces_found):
                    bb[i][0] = det[i][0]
                    bb[i][1] = det[i][1]
                    bb[i][2] = det[i][2]
                    bb[i][3] = det[i][3]

                    if (bb[i][3]-bb[i][1])/frame.shape[0] > 0.25:
                        cropped = frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :]
                        scaled = cv2.resize(cropped, (self.INPUT_IMAGE_SIZE, self.INPUT_IMAGE_SIZE),
                                            interpolation=cv2.INTER_CUBIC)
                        scaled = facenet.prewhiten(scaled)
                        scaled_reshape = scaled.reshape(-1, self.INPUT_IMAGE_SIZE, self.INPUT_IMAGE_SIZE, 3)
                        feed_dict = {self.images_placeholder: scaled_reshape, self.phase_train_placeholder: False}
                        emb_array = self.sess.run(self.embeddings, feed_dict=feed_dict)

                        predictions = self.model.predict_proba(emb_array)
                        best_class_indices = np.argmax(predictions, axis=1)
                        best_class_probabilities = predictions[
                            np.arange(len(best_class_indices)), best_class_indices]
                        best_name = self.class_names[best_class_indices[0]]

                        if best_class_probabilities > 0.8:
                            cv2.rectangle(frame, (bb[i][0], bb[i][1]),
                                          (bb[i][2], bb[i][3]), (0, 255, 0), 2)
                            text_x = bb[i][0]
                            text_y = bb[i][3] + 20

                            cv2.putText(frame, best_name, (text_x, text_y),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (255, 255, 255), thickness=1, lineType=2)
                            cv2.putText(frame, str(round(best_class_probabilities[0], 3)), (text_x, text_y + 17),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (255, 255, 255), thickness=1, lineType=2)
                            self.current_name = best_name
                        else:
                            self.current_name = "Unknown"
                    else:
                        self.current_name = "Unknown"
            else:
                self.current_name = "Unknown"
        except Exception as e:
            print(f"Lỗi nhận diện: {e}")
            self.current_name = "Unknown"

        # Chuyển frame sang QImage để hiển thị trên label_3
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(convert_to_qt_format)
        self.label_3.setPixmap(pix)

    def check_in(self):
        # Lấy tên từ nhận diện hiện tại
        name = self.current_name
        # Đặt tên này vào lineEdit cho Check-in
        self.lineEdit.setText(name)

        # Lưu vào DB, CSV ...
        self.save_to_mongodb(name, self.current_frame_image, collection='checkins')
        save_to_csv(name)
        print(f"Check-in: {name}")

    def check_out(self):
        # Lấy tên từ nhận diện hiện tại
        name = self.current_name
        # Đặt tên này vào lineEdit_3 cho Check-out
        self.lineEdit_3.setText(name)

        # Lưu vào DB, CSV ...
        self.save_to_mongodb(name, self.current_frame_image, collection='checkouts')
        save_to_csv(name)
        print(f"Check-out: {name}")

    def save_to_mongodb(self, name, frame_image, collection='checkins'):
        now = datetime.now()
        data = {
            'name': name,
            'timestamp': now
        }
        try:
            if frame_image is not None:
                _, buffer = cv2.imencode('.jpg', frame_image)
                img_bytes = buffer.tobytes()
                data['image'] = img_bytes

            if collection == 'checkins':
                self.checkin_collection.insert_one(data)
            elif collection == 'checkouts':
                self.checkout_collection.insert_one(data)
            else:
                print(f"Collection không hợp lệ: {collection}")
                return
            print(f"Đã lưu vào MongoDB ({collection}): {data}")
        except Exception as e:
            print(f"Lỗi khi lưu vào MongoDB: {e}")

    def closeEvent(self, event):
        # Đóng camera, session, kết nối db
        if self.cap.isOpened():
            self.cap.release()
        self.sess.close()
        self.client.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec())
