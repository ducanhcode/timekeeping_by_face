from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
tf.compat.v1.disable_eager_execution()  # Tắt eager execution nếu sử dụng TensorFlow 2.x

from imutils.video import VideoStream

import csv
from datetime import datetime

import time

import argparse
import facenet
import imutils
import os
import sys
import math
import pickle
import align.detect_face
import numpy as np
import cv2
import collections
from sklearn.svm import SVC

import tkinter as tk
from PIL import Image, ImageTk
import threading

# Hàm ghi dữ liệu vào file CSV
def save_to_csv(name):
    with open('recognition_log.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([name, now])

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        # Khởi tạo các biến
        self.last_name = ""
        self.current_name = ""
        self.frame = None

        # Tạo canvas để hiển thị video
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Ô hiển thị tên
        self.name_label = tk.Label(root, text="Tên:", font=("Arial", 14))
        self.name_label.pack()

        self.name_display = tk.Label(root, text="", font=("Arial", 14))
        self.name_display.pack()

        # Nút Check-in
        self.checkin_button = tk.Button(root, text="Check-in", command=self.check_in)
        self.checkin_button.pack()

        # Khởi động nhận diện khuôn mặt
        self.init_face_recognition()

        # Bắt đầu luồng video
        self.video_stream = VideoStream(src=0).start()
        time.sleep(2.0)  # Đợi camera khởi động

        self.update_video()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def init_face_recognition(self):
        # Các tham số
        self.MINSIZE = 20
        self.THRESHOLD = [0.6, 0.7, 0.7]
        self.FACTOR = 0.709
        self.IMAGE_SIZE = 182
        self.INPUT_IMAGE_SIZE = 160
        self.CLASSIFIER_PATH = 'Models/facemodel.pkl'
        self.FACENET_MODEL_PATH = 'Models/20180402-114759.pb'

        # Load mô hình phân loại tùy chỉnh
        with open(self.CLASSIFIER_PATH, 'rb') as file:
            self.model, self.class_names = pickle.load(file)
        print("Custom Classifier, Successfully loaded")

        # Thiết lập đồ thị và session TensorFlow
        self.sess = tf.compat.v1.Session()
        with self.sess.as_default():
            # Load mô hình FaceNet
            print('Loading feature extraction model')
            facenet.load_model(self.FACENET_MODEL_PATH)

            # Lấy các tensor đầu vào và đầu ra từ mô hình
            self.images_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("input:0")
            self.embeddings = tf.compat.v1.get_default_graph().get_tensor_by_name("embeddings:0")
            self.phase_train_placeholder = tf.compat.v1.get_default_graph().get_tensor_by_name("phase_train:0")
            self.embedding_size = self.embeddings.get_shape()[1]

            # Tạo các mạng P-Net, R-Net, O-Net cho MTCNN
            self.pnet, self.rnet, self.onet = align.detect_face.create_mtcnn(self.sess, "src/align")

    def update_video(self):
        self.frame = self.video_stream.read()
        self.frame = imutils.resize(self.frame, width=600)
        self.frame = cv2.flip(self.frame, 1)

        # Nhận diện khuôn mặt
        bounding_boxes, _ = align.detect_face.detect_face(self.frame, self.MINSIZE, self.pnet, self.rnet, self.onet, self.THRESHOLD, self.FACTOR)

        faces_found = bounding_boxes.shape[0]
        try:
            if faces_found > 1:
                cv2.putText(self.frame, "Only one face", (0, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (255, 255, 255), thickness=1, lineType=2)
            elif faces_found > 0:
                det = bounding_boxes[:, 0:4]
                bb = np.zeros((faces_found, 4), dtype=np.int32)
                for i in range(faces_found):
                    bb[i][0] = det[i][0]
                    bb[i][1] = det[i][1]
                    bb[i][2] = det[i][2]
                    bb[i][3] = det[i][3]

                    if (bb[i][3]-bb[i][1])/self.frame.shape[0] > 0.25:
                        cropped = self.frame[bb[i][1]:bb[i][3], bb[i][0]:bb[i][2], :]
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
                        print("Name: {}, Probability: {}".format(best_name, best_class_probabilities))

                        if best_class_probabilities > 0.8:
                            cv2.rectangle(self.frame, (bb[i][0], bb[i][1]), (bb[i][2], bb[i][3]), (0, 255, 0), 2)
                            text_x = bb[i][0]
                            text_y = bb[i][3] + 20

                            name = self.class_names[best_class_indices[0]]
                            cv2.putText(self.frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (255, 255, 255), thickness=1, lineType=2)
                            cv2.putText(self.frame, str(round(best_class_probabilities[0], 3)), (text_x, text_y + 17),
                                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (255, 255, 255), thickness=1, lineType=2)
                            self.current_name = name
                        else:
                            name = "Unknown"
                            self.current_name = name
        except:
            pass

        # Chuyển đổi frame sang định dạng Image cho Tkinter
        cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        # Hiển thị hình ảnh trên label
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # Cập nhật sau 10ms
        self.root.after(10, self.update_video)

    def check_in(self):
        # Khi nhấn nút Check-in, hiển thị tên vào ô hiển thị tên
        self.name_display.config(text=self.current_name)
        # Ghi vào CSV
        save_to_csv(self.current_name)
        print(f"Check-in: {self.current_name}")

    def on_closing(self):
        self.video_stream.stop()
        self.sess.close()
        self.root.destroy()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Path of the video you want to test on.', default=0)
    args = parser.parse_args()

    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
