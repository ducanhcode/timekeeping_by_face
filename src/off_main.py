import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from offdes import Ui_MainWindow  # Import giao diện từ offdes.py
from pymongo import MongoClient
from datetime import datetime

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["leave_requests"]
collection = db["requests"]

class OffApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(OffApp, self).__init__()
        self.setupUi(self)  # Thiết lập giao diện từ Ui_MainWindow
        self.setWindowTitle("Đăng Ký Nghỉ Phép")

        # Gắn sự kiện cho nút "Gửi"
        self.pushButton.clicked.connect(self.submit_data)

        # Thêm placeholder cho ô nhập ngày tháng
        self.lineEdit_2.setPlaceholderText("YYYY-MM-DD")  # Hiển thị "YYYY-MM-DD" ở ô nhập ngày

    def submit_data(self):
        """Hàm xử lý gửi dữ liệu đến MongoDB."""
        name = self.lineEdit.text()  # Nhập Họ Tên
        leave_type = self.comboBox.currentText()  # Chọn loại nghỉ phép
        date = self.lineEdit_2.text()  # Nhập Ngày
        reason = self.textEdit.toPlainText()  # Lấy nội dung từ QTextEdit (thay vì lineEdit_3)

        # Kiểm tra dữ liệu nhập vào
        if not name or not leave_type or not date or not reason:
            QMessageBox.critical(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return

        # Kiểm tra định dạng ngày tháng
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Ngày không hợp lệ! Định dạng: YYYY-MM-DD")
            return

        # Chuẩn bị dữ liệu để lưu
        data = {
            "name": name,
            "leave_type": leave_type,
            "date": parsed_date,  # Lưu dưới dạng datetime
            "reason": reason
        }

        # Lưu dữ liệu vào MongoDB
        try:
            collection.insert_one(data)
            QMessageBox.information(self, "Thành công", "Đã gửi thông tin nghỉ phép!")
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu dữ liệu: {e}")

    def clear_fields(self):
        """Xóa nội dung các ô nhập sau khi gửi dữ liệu."""
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.textEdit.clear()  # Xóa nội dung QTextEdit
        self.comboBox.setCurrentIndex(0)  # Đặt ComboBox về lựa chọn đầu tiên

def main():
    app = QApplication(sys.argv)
    window = OffApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
