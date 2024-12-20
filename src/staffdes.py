# Form implementation generated from reading ui file 'staffdes.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(337, 339)
        MainWindow.setStyleSheet("\n"
"background-color:#e8e8e8;")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 291, 271))
        self.groupBox.setStyleSheet("QGroupBox {\n"
"    background: qlineargradient(\n"
"        spread:pad, \n"
"        x1:0, y1:0, x2:1, y2:1, \n"
"        stop:0 #3cacd0,   /*  (trái trên) */\n"
"        stop:0.5 #7ec8e0, /*  (giữa) */\n"
"        stop:1 #0083ab    /* (phải dưới) */\n"
"    );\n"
"    border: 1px solid #A9A9A9; /* Viền xám nhạt */\n"
"    border-radius: 10px; /* Góc bo tròn */\n"
"    color: #000; /* Màu chữ đen */\n"
"    font-weight: bold; /* Chữ in đậm */\n"
"    padding: 10px; /* Khoảng cách nội bộ */\n"
"}\n"
"")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(70, 70, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #d4ecf4, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #a6d9e9  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 130, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #cde9f3, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #a6d9e9  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 190, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #cde9f3, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #a6d9e9  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton_4.setGeometry(QtCore.QRect(80, 10, 141, 41))
        self.pushButton_4.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #cde9f3, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #a6d9e9  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton_4.setObjectName("pushButton_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 337, 22))
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
        self.pushButton.setText(_translate("MainWindow", "Chấm Công"))
        self.pushButton_2.setText(_translate("MainWindow", "Cập Nhật Thông Tin"))
        self.pushButton_3.setText(_translate("MainWindow", "Thêm Dữ Liệu Chấm Công"))
        self.pushButton_4.setText(_translate("MainWindow", "Xin Phép"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
