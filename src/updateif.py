import sys
from PyQt6 import QtWidgets
from pymongo import MongoClient


class UpdateInfoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(UpdateInfoApp, self).__init__()
        self.setWindowTitle("Cập nhật thông tin")
        self.setGeometry(100, 100, 400, 400)

        # Tạo widget trung tâm
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout chính
        self.layout = QtWidgets.QVBoxLayout()

        # Các ô nhập liệu
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên")

        self.dob_input = QtWidgets.QLineEdit()
        self.dob_input.setPlaceholderText("Nhập ngày sinh (yyyy-mm-dd)")

        self.department_input = QtWidgets.QLineEdit()
        self.department_input.setPlaceholderText("Nhập phòng ban")

        self.position_input = QtWidgets.QLineEdit()
        self.position_input.setPlaceholderText("Nhập chức vụ")

        # Nút browse hình ảnh
        self.browse_button = QtWidgets.QPushButton("Chọn hình ảnh")
        self.browse_button.clicked.connect(self.browse_image)
        self.image_path = None

        # Nút cập nhật
        self.update_button = QtWidgets.QPushButton("Cập nhật thông tin")
        self.update_button.clicked.connect(self.update_info)

        # Thêm các widget vào layout
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.dob_input)
        self.layout.addWidget(self.department_input)
        self.layout.addWidget(self.position_input)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.update_button)

        self.central_widget.setLayout(self.layout)

    def browse_image(self):
        """Chọn hình ảnh để lưu"""
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Không chọn được hình ảnh.")

    def update_info(self):
        """Lưu thông tin và hình ảnh vào MongoDB"""
        name = self.name_input.text()
        dob = self.dob_input.text()
        department = self.department_input.text()
        position = self.position_input.text()

        if not name or not dob or not department or not position:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Đọc hình ảnh dưới dạng binary
        image_data = None
        if self.image_path:
            try:
                with open(self.image_path, "rb") as image_file:
                    image_data = image_file.read()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi đọc hình ảnh: {e}")
                return

        # Kết nối MongoDB
        try:
            client = MongoClient("mongodb://localhost:27017/")
            db = client["user_information"]
            collection = db[name]  # Tạo collection với tên là "name"

            # Lưu thông tin vào collection
            document = {
                "name": name,
                "dob": dob,
                "department": department,
                "position": position,
            }
            if image_data:
                document["image"] = image_data

            collection.insert_one(document)
            QtWidgets.QMessageBox.information(self, "Thành công", f"Thông tin đã lưu trong collection '{name}'!")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi kết nối MongoDB: {e}")
        finally:
            client.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UpdateInfoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
