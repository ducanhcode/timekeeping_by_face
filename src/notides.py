# Form implementation generated from reading ui file 'notides.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(628, 447)
        MainWindow.setStyleSheet("\n"
"background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 40, 541, 321))
        self.groupBox.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:1, y2:1, \n"
"    stop:0 #6989c4, /* Màu hồng nhạt góc trên trái */\n"
"    stop:1 #a8ceef  /* Màu xanh dương nhạt góc dưới phải */\n"
");\n"
"border: 1px solid #151515; /* Viền xanh nhạt */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.treeView = QtWidgets.QTreeView(parent=self.groupBox)
        self.treeView.setGeometry(QtCore.QRect(20, 70, 500, 231))
        self.treeView.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid #357ABD; /* Viền xanh đậm */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: black; /* Chữ màu trắng */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.treeView.setObjectName("treeView")
        self.pushButton = QtWidgets.QPushButton(parent=self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(450, 20, 71, 31))
        self.pushButton.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"   stop:0 #d7f5ff, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #8ad5e9  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(120, 20, 151, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid #357ABD; /* Viền xanh đậm */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: black; /* Chữ màu trắng */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(parent=self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 31))
        self.label.setStyleSheet("background: qlineargradient(\n"
"    spread:pad, \n"
"    x1:0, y1:0, x2:0, y2:1, \n"
"    stop:0 #e4eaf4, /* Trắng mờ hơn ở trên */\n"
"    stop:1 #86a0cf  /* Trắng mờ hơn ở dưới */\n"
");\n"
"border: 1px solid rgba(200, 200, 200, 0.6); /* Viền xám mờ */\n"
"border-radius: 5px; /* Góc bo tròn */\n"
"color: #000; /* Chữ màu đen */\n"
"font-weight: bold; /* Chữ in đậm */\n"
"padding: 5px; /* Khoảng cách nội bộ */\n"
"")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 628, 22))
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
        self.pushButton.setText(_translate("MainWindow", "Xem"))
        self.label.setText(_translate("MainWindow", "Nhập ngày:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())