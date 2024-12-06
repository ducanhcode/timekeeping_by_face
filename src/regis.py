import sys
from PyQt6 import QtWidgets
import pymongo
import bcrypt

class RegisterApp(QtWidgets.QWidget):
    def __init__(self):
        super(RegisterApp, self).__init__()
        self.setWindowTitle("Đăng ký")
        self.setGeometry(100, 100, 300, 200)

        # Kết nối đến MongoDB
        try:
            self.client = pymongo.MongoClient('localhost', 27017)  # Thay đổi nếu cần
            self.db = self.client['user_authentication']  # Tên database
            self.users_collection = self.db['users']  # Tên collection
            print("Kết nối MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")
            sys.exit(1)

        # Tạo layout và các widget
        self.layout = QtWidgets.QVBoxLayout()

        self.label_username = QtWidgets.QLabel("Tên đăng nhập:")
        self.input_username = QtWidgets.QLineEdit()

        self.label_password = QtWidgets.QLabel("Mật khẩu:")
        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.button_register = QtWidgets.QPushButton("Đăng ký")

        # Thêm các widget vào layout
        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.input_username)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)
        self.layout.addWidget(self.button_register)

        self.setLayout(self.layout)

        # Kết nối nút đăng ký với chức năng
        self.button_register.clicked.connect(self.register_user)

    def register_user(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        if self.users_collection.find_one({'username': username}):
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Thêm tài khoản mới vào MongoDB
        self.users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'role': 'staff'  # Mặc định là 'staff'
        })

        QtWidgets.QMessageBox.information(self, "Thành công", "Đăng ký tài khoản thành công!")
        self.close()

    def closeEvent(self, event):
        # Đóng kết nối MongoDB khi cửa sổ đóng
        self.client.close()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RegisterApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
