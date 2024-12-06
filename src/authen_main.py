import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from authendes import Ui_MainWindow  # Import lớp giao diện từ authendes.py
import pymongo
import bcrypt
import subprocess
from PyQt6.QtWidgets import QMessageBox


class AuthendesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(AuthendesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Face Recognition App")
        # Kết nối đến MongoDB
        try:
            self.client = pymongo.MongoClient('mongodb://192.168.110.113:27017/')  # Thay đổi nếu cần
            self.db = self.client['user_authentication']  # Tên database
            self.users_collection = self.db['users']  # Tên collection
            print("Kết nối MongoDB thành công!")
        except Exception as e:
            print(f"Lỗi khi kết nối MongoDB: {e}")
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi kết nối MongoDB: {e}")
            sys.exit(1)

        # Tạo tài khoản admin mặc định nếu chưa tồn tại
        if not self.users_collection.find_one({'username': 'admin'}):
            hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
            self.users_collection.insert_one({
                'username': 'admin',
                'password': hashed_password,
                'role': 'admin'
            })

        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        # Kết nối các nút với chức năng
        self.pushButton.clicked.connect(self.login)  # Nút Đăng Nhập
        self.pushButton_2.clicked.connect(self.register)  # Nút Đăng Ký

    def login(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        user = self.users_collection.find_one({'username': username})

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            role = user['role']
            QMessageBox.information(self, "Thành công", f"Đăng nhập thành công với vai trò: {role}")
            if username == 'admin':
                self.open_admin_window()
            else:
                self.open_staff_window()
        else:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def open_admin_window(self):
        # Import và mở cửa sổ admin
        try:
            import admin_main
            self.admin_window = admin_main.AdminDesApp()
            self.admin_window.show()
            self.close()
        except ImportError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp admin_main.py.")

    def open_staff_window(self):
        # Import và mở cửa sổ staff
        try:
            import staff_main
            self.staff_window = staff_main.StaffDesApp()
            self.staff_window.show()
            self.close()
        except ImportError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp staff.py.")

    def register(self):
        # Thực hiện lệnh chạy file regisdes.py
        try:
            subprocess.run(["python", "src/regis_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi mở tệp regisdes.py: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp regisdes.py.")

    def closeEvent(self, event):
        self.client.close()
        event.accept()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AuthendesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
