import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import subprocess

class StaffApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(StaffApp, self).__init__()
        self.setWindowTitle("Nhân viên")
        self.setGeometry(100, 100, 400, 200)

        # Tạo widget trung tâm
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Tạo layout và các widget
        self.layout = QtWidgets.QVBoxLayout()

        self.button_attendance = QtWidgets.QPushButton("Chấm công")
        self.button_update_info = QtWidgets.QPushButton("Cập nhật thông tin")  # Nút mới

        self.layout.addWidget(self.button_attendance)
        self.layout.addWidget(self.button_update_info)  # Thêm nút mới vào layout

        self.central_widget.setLayout(self.layout)

        # Kết nối các nút với chức năng
        self.button_attendance.clicked.connect(self.attendance)
        self.button_update_info.clicked.connect(self.update_info)  # Kết nối nút mới

    def attendance(self):
        # Thực thi lệnh python src/testmongo.py
        try:
            subprocess.run(["python", "src/testmongo.py"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")

    def update_info(self):
        # Thực thi lệnh python src/updateif.py
        try:
            subprocess.run(["python", "src/updateif.py"], check=True)
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
    window = StaffApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
