import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import pymongo
import bcrypt
import subprocess  # Import subprocess để chạy lệnh bên ngoài

class AuthenApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(AuthenApp, self).__init__()
        self.setWindowTitle("Đăng nhập")
        self.setGeometry(100, 100, 300, 200)

        # Kết nối đến MongoDB
        self.client = pymongo.MongoClient('localhost', 27017)  # Thay đổi nếu cần
        self.db = self.client['user_authentication']  # Tên database
        self.users_collection = self.db['users']  # Tên collection

        # Tạo tài khoản admin mặc định nếu chưa tồn tại
        if not self.users_collection.find_one({'username': 'admin'}):
            hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            self.users_collection.insert_one({
                'username': 'admin',
                'password': hashed_password,
                'role': 'admin'
            })

        # Tạo widget trung tâm
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Tạo layout và các widget
        self.layout = QtWidgets.QVBoxLayout()

        self.label_username = QtWidgets.QLabel("Tên đăng nhập:")
        self.input_username = QtWidgets.QLineEdit()

        self.label_password = QtWidgets.QLabel("Mật khẩu:")
        self.input_password = QtWidgets.QLineEdit()
        self.input_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.button_login = QtWidgets.QPushButton("Đăng nhập")
        self.button_register = QtWidgets.QPushButton("Đăng ký")

        self.layout.addWidget(self.label_username)
        self.layout.addWidget(self.input_username)
        self.layout.addWidget(self.label_password)
        self.layout.addWidget(self.input_password)
        self.layout.addWidget(self.button_login)
        self.layout.addWidget(self.button_register)

        self.central_widget.setLayout(self.layout)

        # Kết nối các nút với chức năng
        self.button_login.clicked.connect(self.login)
        self.button_register.clicked.connect(self.register)

    def login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        user = self.users_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            role = user['role']
            QtWidgets.QMessageBox.information(self, "Thành công", f"Đăng nhập thành công với vai trò: {role}")
            if username == 'admin':
                self.open_admin_window()
            else:
                self.open_staff_window()
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def open_admin_window(self):
        # Import tệp admin.py và mở cửa sổ admin
        import admin
        self.admin_window = admin.AdminApp()
        self.admin_window.show()
        self.close()

    def open_staff_window(self):
        # Import tệp staff.py và mở cửa sổ staff
        import staff
        self.staff_window = staff.StaffApp()
        self.staff_window.show()
        self.close()

    def register(self):
        # Thực hiện lệnh chạy file regis.py
        try:
            subprocess.run(["python", "src/regis.py"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở tệp regis.py: {e}")
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp regis.py trong thư mục src.")

    def closeEvent(self, event):
        self.client.close()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthenApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
