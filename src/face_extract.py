# CÁCH DÙNG LỆNH
# python face_extract.py --input videos/real.mp4 --output dataset/real

import numpy as np
import argparse
import cv2
import os

# Các tham số đầu vào
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, required=True,
    help="path to input video")
ap.add_argument("-o", "--output", type=str, required=True,
    help="path to output directory of cropped faces")
ap.add_argument("-d", "--detector", type=str, default='face_detector',
    help="path to OpenCV's deep learning face detector")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
ap.add_argument("-s", "--skip", type=int, default=1,
    help="# of frames to skip before applying face detection")
args = vars(ap.parse_args())

# Load model ssd nhận diện mặt
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
    "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# Đọc file video input
vs = cv2.VideoCapture(args["input"])
read = 0
saved = 0

# Lặp qua các frame của video
while True:

    (grabbed, frame) = vs.read()
    # Nếu không đọc được frame thì thoát
    if not grabbed:
        break

    read += 1
    if read % args["skip"] != 0:
        continue

    # Chuyển từ frame thành blob
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))

    # Phát hiện các khuôn mặt trong frame
    net.setInput(blob)
    detections = net.forward()

    # Nếu tìm thấy ít nhất 1 khuôn mặt
    if len(detections) > 0:
        # Tìm khuôn mặt có độ tin cậy cao nhất
        i = np.argmax(detections[0, 0, :, 2])
        confidence = detections[0, 0, i, 2]

        # Nếu độ tin cậy > threshold
        if confidence > args["confidence"]:
            # Tách khuôn mặt và ghi ra file
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            face = frame[startY:endY, startX:endX]

            # Lấy tên file từ đường dẫn input
            filename = os.path.basename(args["input"])
            # Loại bỏ phần mở rộng để lấy tên file
            filename = os.path.splitext(filename)[0]
            # Tạo đường dẫn lưu ảnh
            p = os.path.sep.join([args["output"],
                f"{filename}_{saved}.png"])
            # Ghi ảnh khuôn mặt vào file
            cv2.imwrite(p, face)
            saved += 1
            print(f"[INFO] saved {p} to disk")

vs.release()
cv2.destroyAllWindows()
