import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from updateifdes import Ui_MainWindow  # Import lớp giao diện từ updateifdes.py
from pymongo import MongoClient
from PyQt6.QtWidgets import QMessageBox


class UpdateIfDesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UpdateIfDesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow

        # Kết nối MongoDB
        try:
            self.client = MongoClient('mongodb://192.168.110.113:27017/')
            self.db = self.client["user_information"]
            self.users_collection = self.db["users"]  # Bạn có thể thay đổi collection nếu cần
            print("Kết nối MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi kết nối MongoDB: {e}")
            sys.exit(1)

        # Khởi tạo biến để lưu đường dẫn hình ảnh
        self.image_path = None

        # Đặt placeholder text cho các ô nhập liệu
        self.lineEdit.setPlaceholderText("Nhập tên:")
        self.lineEdit_2.setPlaceholderText("Nhập ngày sinh (yyyy-mm-dd):")
        self.lineEdit_3.setPlaceholderText("Nhập phòng ban:")
        self.lineEdit_4.setPlaceholderText("Nhập chức vụ:")

        # Kết nối nút với chức năng
        self.pushButton.clicked.connect(self.browse_image)        # Nút "Chọn Hình Ảnh"
        self.pushButton_2.clicked.connect(self.update_info)       # Nút "Cập nhật thông tin"

    def browse_image(self):
        """Chọn hình ảnh để lưu."""
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
            QMessageBox.information(self, "Thành công", f"Đã chọn hình ảnh: {file_path}")
        else:
            QMessageBox.warning(self, "Lỗi", "Không chọn được hình ảnh.")

    def update_info(self):
        """Lưu thông tin và hình ảnh vào MongoDB."""
        name = self.lineEdit.text().strip()
        dob = self.lineEdit_2.text().strip()
        department = self.lineEdit_3.text().strip()
        position = self.lineEdit_4.text().strip()

        if not name or not dob or not department or not position:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Đọc hình ảnh dưới dạng binary
        image_data = None
        if self.image_path:
            try:
                with open(self.image_path, "rb") as image_file:
                    image_data = image_file.read()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi đọc hình ảnh: {e}")
                return

        # Lưu thông tin vào MongoDB
        try:
            collection = self.db["user_info"]  # Bạn có thể thay đổi collection nếu cần

            document = {
                "name": name,
                "dob": dob,
                "department": department,
                "position": position,
            }
            if image_data:
                document["image"] = image_data

            collection.insert_one(document)
            QMessageBox.information(self, "Thành công", f"Thông tin đã lưu trong collection 'user_info'!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lưu thông tin vào MongoDB: {e}")
        finally:
            self.client.close()

    def closeEvent(self, event):
        """Đóng kết nối MongoDB khi cửa sổ đóng."""
        try:
            self.client.close()
        except:
            pass
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateIfDesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
