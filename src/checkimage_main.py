import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from checkimagedes import Ui_MainWindow
from PyQt6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QWidget, QScrollArea, QComboBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import pymongo
import gridfs
import numpy as np
import cv2
from datetime import datetime, timedelta

class ImageViewerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ImageViewerApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Cập nhật tiêu đề và các nhãn
        self.setWindowTitle("Xem Hình Ảnh Theo Ngày")
        self.ui.groupBox.setTitle("")
        self.ui.groupBox_2.setTitle("")
        self.ui.groupBox_3.setTitle("")

        self.ui.label.setText("Nhập ngày\n(YYYY-MM-DD):")
        self.ui.btn_view.setText("Xem")
        self.ui.label_3.setText("Chọn dữ liệu:")
        self.ui.label_4.setText("Nhập tên nhân viên:")
        self.ui.label_2.setText("Chọn dữ liệu:")

        # Thiết lập các giá trị mặc định cho ComboBox
        self.ui.collection_menu.clear()
        self.ui.collection_menu.addItems(["checkins", "checkouts"])
        self.ui.collection_var = self.ui.collection_menu.currentText()

        self.ui.option_menu.clear()
        self.ui.option_menu.addItems(["Toàn bộ", "Nhân Viên"])
        self.ui.option_var = self.ui.option_menu.currentText()

        # Kết nối đến MongoDB
        try:
            self.client = pymongo.MongoClient('mongodb://192.168.110.113:27017/')  # Thay đổi nếu cần
            self.db = self.client['face_recognition']              # Tên cơ sở dữ liệu
            self.collection_name = 'checkins'                      # Tên collection mặc định
            self.fs = gridfs.GridFS(self.db)                       # GridFS (nếu sử dụng)
            print("Kết nối đến MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối đến MongoDB: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi kết nối đến MongoDB: {e}")
            return

        # Kết nối các sự kiện
        self.ui.btn_view.clicked.connect(self.view_images)
        self.ui.option_menu.currentIndexChanged.connect(self.on_option_change)
        self.ui.collection_menu.currentIndexChanged.connect(self.on_collection_change)

        # Tạo ScrollArea để hiển thị hình ảnh
        self.scroll_area = self.ui.scrollArea
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setWidget(self.scroll_area_widget)

        # Gọi hàm để cập nhật giao diện theo lựa chọn ban đầu
        self.on_option_change()

    def on_option_change(self):
        option = self.ui.option_menu.currentText()
        if option == "Nhân Viên":
            # Hiển thị ô nhập tên
            self.ui.label_4.show()
            self.ui.entry_name.show()
        else:
            # Ẩn ô nhập tên
            self.ui.label_4.hide()
            self.ui.entry_name.hide()

    def on_collection_change(self):
        # Cập nhật tên collection khi thay đổi lựa chọn
        self.collection_name = self.ui.collection_menu.currentText()

    def view_images(self):
        # Xóa nội dung cũ
        for i in reversed(range(self.scroll_area_layout.count())):
            widget_to_remove = self.scroll_area_layout.itemAt(i).widget()
            self.scroll_area_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        date_str = self.ui.lineEdit.text().strip()
        if not date_str:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập ngày.")
            return

        # Kiểm tra định dạng ngày
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            # Tạo khoảng thời gian từ đầu ngày đến cuối ngày
            start_date = date
            end_date = date + timedelta(days=1)
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Định dạng ngày không hợp lệ. Vui lòng nhập theo định dạng YYYY-MM-DD.")
            return

        option = self.ui.option_menu.currentText()

        query = {
            'timestamp': {
                '$gte': start_date,
                '$lt': end_date
            }
        }

        if option == "Nhân Viên":
            name = self.ui.entry_name.text().strip()
            if not name:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập tên nhân viên.")
                return
            query['name'] = name

        # Lấy tên collection từ lựa chọn của người dùng
        self.collection_name = self.ui.collection_menu.currentText()
        collection = self.db[self.collection_name]

        # Truy vấn MongoDB để lấy các tài liệu phù hợp
        try:
            documents = collection.find(query).sort('timestamp', pymongo.ASCENDING)
            found = False
            for doc in documents:
                found = True
                # Kiểm tra và lấy hình ảnh từ GridFS hoặc từ trường 'image'
                if 'image' in doc:
                    # Lấy hình ảnh từ trường 'image' trong tài liệu
                    img_bytes = doc['image']
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                elif 'image_id' in doc:
                    # Lấy hình ảnh từ GridFS
                    image_id = doc['image_id']
                    grid_out = self.fs.get(image_id)
                    img_bytes = grid_out.read()
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                elif 'image_path' in doc:
                    # Lấy hình ảnh từ hệ thống tệp
                    image_path = doc['image_path']
                    img_cv = cv2.imread(image_path)
                else:
                    continue  # Nếu không có hình ảnh, bỏ qua tài liệu này

                # Chuyển đổi sang RGB cho QImage
                img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

                # Thay đổi kích thước hình ảnh nếu cần
                img_cv = cv2.resize(img_cv, (200, 200), interpolation=cv2.INTER_AREA)

                # Chuyển đổi OpenCV image thành QImage
                height, width, channel = img_cv.shape
                bytesPerLine = channel * width
                qImg = QImage(img_cv.data, width, height, bytesPerLine, QImage.Format.Format_RGB888)

                # Tạo QLabel để hiển thị hình ảnh
                img_label = QLabel()
                img_label.setPixmap(QPixmap.fromImage(qImg))
                img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Hiển thị tên và thời gian chụp
                timestamp = doc.get('timestamp', None)
                if timestamp:
                    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    timestamp_str = "Không rõ thời gian"

                name = doc.get('name', 'Không rõ tên')

                info_label = QLabel(f"{name}\n{timestamp_str}")
                info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # Tạo widget để chứa hình ảnh và thông tin
                container = QWidget()
                container_layout = QVBoxLayout()
                container_layout.addWidget(img_label)
                container_layout.addWidget(info_label)
                container.setLayout(container_layout)

                # Thêm container vào layout chính
                self.scroll_area_layout.addWidget(container)
            if not found:
                QMessageBox.information(self, "Thông báo", "Không tìm thấy hình ảnh phù hợp.")
        except Exception as e:
            print(f"Lỗi khi truy vấn MongoDB: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi truy vấn MongoDB: {e}")

    def closeEvent(self, event):
        self.client.close()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ImageViewerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
