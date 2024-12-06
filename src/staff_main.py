import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from staffdes import Ui_MainWindow  # Import lớp giao diện từ staffdes.py
import subprocess
from PyQt6.QtWidgets import QMessageBox
import authen_main  # Import giao diện đăng nhập

class StaffDesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(StaffDesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Nhân Viên")
        # Kết nối các nút với chức năng
        self.pushButton.clicked.connect(self.attendance)         # Nút "Chấm Công"
        self.pushButton_2.clicked.connect(self.update_info)      # Nút "Cập Nhật Thông Tin"
        self.pushButton_3.clicked.connect(self.add_data)
        self.pushButton_4.clicked.connect(self.off)
    def attendance(self):
        """Chức năng chấm công."""
        try:
            subprocess.run(["python", "src/testmongo_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp testmongo.py trong thư mục src.")

    def update_info(self):
        """Chức năng cập nhật thông tin."""
        try:
            subprocess.run(["python", "src/updateif_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp updateif.py trong thư mục src.")

    def add_data(self):
        """Chức năng thêm dữ liệu chấm công."""
        try:
            subprocess.run(["python", "src/makedata_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp makedata.py trong thư mục src.")

    def off(self):
        """Chức năng xin nghỉ phép."""
        try:
            subprocess.run(["python", "src/off_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp testmongo.py trong thư mục src.")
    def closeEvent(self, event):
        self.authen_window = authen_main.AuthendesApp()
        self.authen_window.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = StaffDesApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
