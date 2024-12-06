import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QScrollArea, QHBoxLayout
from PyQt6.QtGui import QPixmap
from pymongo import MongoClient
from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt


class ManageStaffApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(ManageStaffApp, self).__init__()
        self.setWindowTitle("Quản lý nhân viên")
        self.setGeometry(100, 100, 1200, 600)  # Tăng chiều rộng để phù hợp với hiển thị ngang

        # Kết nối MongoDB
        try:
            self.client = MongoClient('localhost', 27017)
            self.db = self.client["user_information"]
            print("Kết nối MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")

        # Tạo widget chính
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout chính
        self.layout = QVBoxLayout()

        # Tạo combobox để lựa chọn giữa toàn bộ hoặc nhân viên cụ thể
        self.combobox = QComboBox()
        self.combobox.addItems(["Toàn bộ", "Nhân viên"])
        self.combobox.currentIndexChanged.connect(self.toggle_name_input)

        # Ô nhập tên nhân viên (ẩn theo mặc định)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên nhân viên")
        self.name_input.setVisible(False)

        # Nút xem dữ liệu
        self.view_button = QPushButton("Xem")
        self.view_button.clicked.connect(self.view_data)

        # Khu vực hiển thị dữ liệu
        self.scroll_area = QScrollArea()
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QHBoxLayout()  # Thay đổi sang QHBoxLayout để hiển thị ngang
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Thêm các widget vào layout
        self.layout.addWidget(QLabel("Chọn kiểu dữ liệu:"))
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.view_button)
        self.layout.addWidget(self.scroll_area)

        self.central_widget.setLayout(self.layout)

    def toggle_name_input(self):
        if self.combobox.currentText() == "Nhân viên":
            self.name_input.setVisible(True)
        else:
            self.name_input.setVisible(False)

    def view_data(self):
        self.clear_display_area()

        if self.combobox.currentText() == "Toàn bộ":
            # Lấy tất cả collection và hiển thị dữ liệu mới nhất
            collection_names = self.db.list_collection_names()
            for collection_name in collection_names:
                collection = self.db[collection_name]
                latest_record = collection.find_one(sort=[("_id", -1)])
                if latest_record:
                    self.display_record(latest_record, collection_name)
        else:
            name = self.name_input.text().strip()
            if not name:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên nhân viên.")
                return

            collection = self.db[name]
            latest_record = collection.find_one(sort=[("_id", -1)])
            if latest_record:
                self.display_record(latest_record)
            else:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Không tìm thấy dữ liệu cho nhân viên.")

    def clear_display_area(self):
        # Xóa tất cả widget trong khu vực hiển thị
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_record(self, record, collection_name=None):
        # Container để chứa ảnh và thông tin
        record_container = QtWidgets.QWidget()
        record_layout = QVBoxLayout()
        record_container.setLayout(record_layout)

        # Hiển thị ảnh (nếu có)
        image_label = QLabel()
        if "image" in record and record["image"]:
            pixmap = self.get_image_from_binary(record["image"])
            if pixmap:
                image_label.setPixmap(pixmap)
        else:
            image_label.setText("Không có hình ảnh")

        # Hiển thị thông tin
        info_label = QLabel()
        info_text = self.format_record(record, collection_name)
        info_label.setText(info_text)
        info_label.setWordWrap(True)

        # Thêm ảnh và thông tin vào container
        record_layout.addWidget(image_label)
        record_layout.addWidget(info_label)

        # Thêm container vào scroll layout
        self.scroll_layout.addWidget(record_container)

    def format_record(self, record, collection_name=None):
        name = record.get("name", "N/A")
        dob = record.get("dob", "N/A")
        department = record.get("department", "N/A")
        position = record.get("position", "N/A")
        formatted_text = (
            f"<b>Name:</b> {name}<br>"
            f"<b>DOB:</b> {dob}<br>"
            f"<b>Department:</b> {department}<br>"
            f"<b>Position:</b> {position}"
        )
        if collection_name:
            formatted_text = f"<b>Collection:</b> {collection_name}<br>" + formatted_text
        return formatted_text

    def get_image_from_binary(self, binary_data):
        try:
            image = Image.open(BytesIO(binary_data))
            image = image.convert("RGBA")
            qt_image = QPixmap.fromImage(ImageQt(image))
            return qt_image.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        except Exception as e:
            print(f"Lỗi khi xử lý hình ảnh: {e}")
            return None


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ManageStaffApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
