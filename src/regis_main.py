import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from regisdes import Ui_MainWindow  # Import lớp giao diện từ regisdes.py
import pymongo
import bcrypt
from PyQt6.QtWidgets import QMessageBox

class RegisdesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RegisdesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Đăng ký nếu chưa có tài khoản")
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

        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # Kết nối nút đăng ký với chức năng
        self.pushButton_2.clicked.connect(self.register_user)

    def register_user(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        if self.users_collection.find_one({'username': username}):
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Thêm tài khoản mới vào MongoDB
        self.users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'role': 'staff'  # Mặc định là 'staff'
        })

        QMessageBox.information(self, "Thành công", "Đăng ký tài khoản thành công!")
        self.close()

    def closeEvent(self, event):
        self.client.close()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = RegisdesApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
