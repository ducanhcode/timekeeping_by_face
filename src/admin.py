import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import subprocess

class AdminApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(AdminApp, self).__init__()
        self.setWindowTitle("Quản trị viên")
        self.setGeometry(100, 100, 400, 300)

        # Tạo widget trung tâm
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Tạo layout và các widget
        self.layout = QtWidgets.QVBoxLayout()

        self.button_manage_staff = QtWidgets.QPushButton("Quản lý nhân viên")
        self.button_manage_attendance = QtWidgets.QPushButton("Quản lý chấm công")
        self.button_add_data = QtWidgets.QPushButton("Thêm dữ liệu")

        self.layout.addWidget(self.button_manage_staff)
        self.layout.addWidget(self.button_manage_attendance)
        self.layout.addWidget(self.button_add_data)

        self.central_widget.setLayout(self.layout)

        # Kết nối các nút với chức năng
        self.button_manage_staff.clicked.connect(self.manage_staff)
        self.button_manage_attendance.clicked.connect(self.manage_attendance)
        self.button_add_data.clicked.connect(self.add_data)

    def manage_staff(self):
        try:
            subprocess.run(["python", "src/managestaff.py"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")

    def manage_attendance(self):
        # Thực thi lệnh python src/checkimage.py
        try:
            subprocess.run(["python", "src/checkimage_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")

    def add_data(self):
        # Thực thi lệnh python src/makedata.py
        try:
            subprocess.run(["python", "src/makedata.py"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")

    def closeEvent(self, event):
        # Quay lại màn hình đăng nhập khi đóng cửa sổ
        from authen import AuthenApp
        self.login_window = AuthenApp()
        self.login_window.show()
        event.accept()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
