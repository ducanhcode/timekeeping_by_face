# Form implementation generated from reading ui file 'managestaffdes.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(566, 510)
        MainWindow.setStyleSheet("background-color: #eef7fb;")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 521, 431))
        self.groupBox.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:1, y2:1, \n"
"    stop:0 #85cbe1, /* Màu hồng nhạt góc trên trái */\n"
"    stop:1 #406f93  /* Màu xanh dương nhạt góc dưới phải */\n"
");\n"
"border: 1px solid #151515; /* Viền xanh nhạt */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setGeometry(QtCore.QRect(16, 29, 111, 31))
        self.label.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:1, y2:1, \n"
"    stop:0 #b8cedf, /* Màu xanh dương đậm */\n"
"    stop:1 #ffffff /* Màu xanh dương nhạt */\n"
");\n"
"border: 1px solid #357ABD; /* Viền xanh đậm */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: black; /* Chữ màu trắng */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(parent=self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(20, 110, 481, 301))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 479, 299))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.comboBox = QtWidgets.QComboBox(parent=self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(140, 30, 91, 31))
        self.comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid #357ABD; /* Viền xanh đậm */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: black; /* Chữ màu trắng */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(20, 70, 211, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid #357ABD; /* Viền xanh đậm */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: black; /* Chữ màu trắng */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(420, 70, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #f3f8fb, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #bee0f5  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 566, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Xem Thông Tin"))
        self.label.setText(_translate("MainWindow", "Lựa chọn dữ liệu:"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Toàn Bộ"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Nhân Viên"))
        self.pushButton.setText(_translate("MainWindow", "Xem"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
