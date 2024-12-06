import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from admindes import Ui_MainWindow  # Import lớp giao diện từ admindes.py
import subprocess
from PyQt6.QtWidgets import QMessageBox
from pymongo import MongoClient
from datetime import datetime, timedelta
import authen_main  # Import giao diện đăng nhập


class AdminDesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(AdminDesApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Quản lý")

        # Kết nối các nút với chức năng
        self.pushButton.clicked.connect(self.manage_staff)  # Nút "Quản Lý Nhân Viên"
        self.pushButton_2.clicked.connect(self.manage_attendance)  # Nút "Quản Lý Chấm Công"
        self.pushButton_3.clicked.connect(self.show_notifications)  # Nút "Thông báo"

        # Hiển thị tổng số đơn khi khởi động giao diện
        self.update_total_requests()

    def manage_staff(self):
        """Chức năng quản lý nhân viên."""
        try:
            subprocess.run(["python", "src/managestaff_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp managestaff.py trong thư mục src.")

    def manage_attendance(self):
        """Chức năng quản lý chấm công."""
        try:
            subprocess.run(["python", "src/checkimage_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp checkimage_main.py trong thư mục src.")

    def update_total_requests(self):
        """Cập nhật tổng số đơn nghỉ phép vào label."""
        try:
            # Kết nối tới MongoDB
            client = MongoClient("mongodb://localhost:27017/")
            db = client["leave_requests"]
            collection = db["requests"]

            # Lấy ngày hiện tại
            today = datetime.now()
            start_of_day = datetime(today.year, today.month, today.day)
            end_of_day = start_of_day + timedelta(days=1)

            # Đếm số đơn nghỉ của ngày hôm nay
            total_requests = collection.count_documents({
                "date": {"$gte": start_of_day, "$lt": end_of_day}
            })

            # Chỉ hiển thị label nếu có ít nhất 1 đơn
            if total_requests > 0:
                self.label.setText(f"{total_requests}")
                self.label.show()  # Hiển thị label
            else:
                self.label.hide()  # Ẩn label nếu không có đơn
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật tổng số đơn: {e}")

    def show_notifications(self):
        """Hiển thị tổng số đơn và chạy file noti.py."""
        try:
            # Chạy file noti.py
            subprocess.run(["python", "src/noti_main.py"], check=True)
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi chạy lệnh: {e}")
        except FileNotFoundError:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tệp noti.py trong thư mục src.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi: {e}")

    def closeEvent(self, event):
        self.authen_window = authen_main.AuthendesApp()
        self.authen_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AdminDesApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
