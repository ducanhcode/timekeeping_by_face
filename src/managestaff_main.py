import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from managestaffdes import Ui_MainWindow  # Import lớp giao diện từ managestaffdes.py
from pymongo import MongoClient
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QPixmap
from io import BytesIO
from PIL import Image
from PIL.ImageQt import ImageQt

class ManageStaffDesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ManageStaffDesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Thông tin nhân viên")
        # Kết nối MongoDB
        try:
            self.client = MongoClient('mongodb://192.168.110.113:27017/')
            self.db = self.client["user_information"]
            print("Kết nối MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi kết nối MongoDB: {e}")
            sys.exit(1)

        # Kết nối các nút với chức năng
        self.pushButton.clicked.connect(self.view_data)  # Nút "Xem"

        # Kết nối combobox để xử lý sự thay đổi lựa chọn
        self.comboBox.currentIndexChanged.connect(self.toggle_name_input)

        # Ô nhập tên nhân viên
        self.name_input = self.lineEdit  # lineEdit tương ứng với "Nhập tên nhân viên"
        self.name_input.setPlaceholderText("Nhập Tên Nhân Viên:")
        self.name_input.setVisible(False)  # Ẩn theo mặc định

    def toggle_name_input(self):
        """Hiển thị hoặc ẩn ô nhập tên nhân viên dựa trên lựa chọn của combobox."""
        if self.comboBox.currentText() == "Nhân Viên":
            self.name_input.setVisible(True)
        else:
            self.name_input.setVisible(False)

    def view_data(self):
        """Hiển thị dữ liệu từ MongoDB dựa trên lựa chọn."""
        self.clear_display_area()

        if self.comboBox.currentText() == "Toàn Bộ":
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
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên nhân viên.")
                return

            collection = self.db[name]
            latest_record = collection.find_one(sort=[("_id", -1)])
            if latest_record:
                self.display_record(latest_record)
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy dữ liệu cho nhân viên.")

    def clear_display_area(self):
        """Xóa tất cả widget trong khu vực hiển thị."""
        scroll_widget = self.scrollAreaWidgetContents
        for child in scroll_widget.findChildren(QtWidgets.QWidget):
            child.deleteLater()

    def display_record(self, record, collection_name=None):
        """Hiển thị một bản ghi trong khu vực hiển thị."""
        # Container để chứa ảnh và thông tin
        record_container = QtWidgets.QWidget(scroll_widget := self.scrollAreaWidgetContents)
        record_layout = QtWidgets.QVBoxLayout()
        record_container.setLayout(record_layout)

        # Hiển thị ảnh (nếu có)
        image_label = QtWidgets.QLabel()
        if "image" in record and record["image"]:
            pixmap = self.get_image_from_binary(record["image"])
            if pixmap:
                image_label.setPixmap(pixmap)
        else:
            image_label.setText("Không có hình ảnh")

        # Hiển thị thông tin
        info_label = QtWidgets.QLabel()
        info_text = self.format_record(record, collection_name)
        info_label.setText(info_text)
        info_label.setWordWrap(True)

        # Thêm ảnh và thông tin vào container
        record_layout.addWidget(image_label)
        record_layout.addWidget(info_label)

        # Thêm container vào scroll widget
        layout = scroll_widget.layout()
        if not layout:
            layout = QtWidgets.QHBoxLayout(scroll_widget)
            scroll_widget.setLayout(layout)
        layout.addWidget(record_container)

    def format_record(self, record, collection_name=None):
        """Định dạng thông tin bản ghi để hiển thị."""
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

        return formatted_text

    def get_image_from_binary(self, binary_data):
        """Chuyển đổi dữ liệu binary thành QPixmap."""
        try:
            image = Image.open(BytesIO(binary_data))
            image = image.convert("RGBA")
            qt_image = QPixmap.fromImage(ImageQt(image))
            return qt_image.scaled(200, 200, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        except Exception as e:
            print(f"Lỗi khi xử lý hình ảnh: {e}")
            return None

    def closeEvent(self, event):
        self.client.close()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ManageStaffDesApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
