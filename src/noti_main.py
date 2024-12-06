from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from pymongo import MongoClient
from datetime import datetime, timedelta
from notides import Ui_MainWindow  # Import giao diện từ notides.py

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client["leave_requests"]
collection = db["requests"]


class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối sự kiện nút bấm
        self.ui.pushButton.clicked.connect(self.fetch_data)

        # Cài đặt model cho treeView
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Họ Tên", "Loại", "Lý do"])
        self.ui.treeView.setModel(self.model)

        # Chỉnh kích thước cột
        self.ui.treeView.header().setStretchLastSection(False)
        self.ui.treeView.header().setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive)  # Cho phép thay đổi kích thước cột
        self.ui.treeView.setColumnWidth(0, 150)  # Đặt độ rộng cho cột 1
        self.ui.treeView.setColumnWidth(1, 100)  # Đặt độ rộng cho cột 2
        self.ui.treeView.setColumnWidth(2, 1000)  # Đặt độ rộng cho cột 3
        self.ui.treeView.header().setMinimumSectionSize(100)  # Kích thước tối thiểu mỗi cột

        self.ui.treeView.setStyleSheet("""
                QTreeView {
                    background-color: white;  /* Màu nền của TreeView */
                    border: 1px solid #357ABD;  /* Viền xanh đậm */
                    color: black;  /* Màu chữ */
                    font-weight: bold;  /* Chữ in đậm */
                }
                   QHeaderView::section {
                       background-color: #cbdae3;  /* Màu nền header */
                       color: black;  /* Màu chữ */
                       font-size: 14px;  /* Kích thước chữ */
                       font-weight: bold;  /* Chữ in đậm */
                       padding: 5px;  /* Khoảng cách giữa chữ và cạnh */
                       border: 1px solid #151515;  /* Viền */
                   }
               """)

        # Lấy ngày hiện tại
        today_date = datetime.now().strftime("%Y-%m-%d")
        self.ui.lineEdit.setText(today_date)  # Hiển thị ngày hiện tại trong ô nhập
        self.fetch_data(today_date)  # Hiển thị dữ liệu cho ngày hiện tại

    def fetch_data(self, date_input=None):
        if not date_input:
            date_input = self.ui.lineEdit.text()

        try:
            # Chuyển đổi ngày từ chuỗi sang datetime
            query_date = datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Lỗi", "Ngày không hợp lệ! Định dạng: YYYY-MM-DD")
            return

        # Xác định khoảng thời gian trong ngày
        start_of_day = datetime(query_date.year, query_date.month, query_date.day)
        end_of_day = start_of_day + timedelta(days=1)

        # Truy vấn dữ liệu từ MongoDB
        records = list(collection.find({"date": {"$gte": start_of_day, "$lt": end_of_day}}))
        self.model.removeRows(0, self.model.rowCount())  # Xóa dữ liệu cũ trong treeView

        # Thêm dữ liệu vào treeView
        for record in records:
            items = [
                QStandardItem(record.get("name", "")),
                QStandardItem(record.get("leave_type", "")),
                QStandardItem(record.get("reason", ""))
            ]
            self.model.appendRow(items)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    mainWindow = MainApp()
    mainWindow.show()
    sys.exit(app.exec())
