# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/annademidova/PycharmProjects/HAR_Parser/Code/design.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 197)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 791, 201))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 141, 181))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(False)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(140, 177, 231);\n"
"color: rgb(255, 255, 255);")
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setGeometry(QtCore.QRect(160, 10, 611, 181))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.chooseFile = QtWidgets.QPushButton(self.frame)
        self.chooseFile.setGeometry(QtCore.QRect(490, 10, 113, 41))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.chooseFile.setFont(font)
        self.chooseFile.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.chooseFile.setObjectName("chooseFile")
        self.chooseDirectory = QtWidgets.QPushButton(self.frame)
        self.chooseDirectory.setGeometry(QtCore.QRect(490, 60, 113, 41))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.chooseDirectory.setFont(font)
        self.chooseDirectory.setStyleSheet("background-color: rgb(230, 230, 230);")
        self.chooseDirectory.setObjectName("chooseDirectory")
        self.labelFile = QtWidgets.QLabel(self.frame)
        self.labelFile.setGeometry(QtCore.QRect(19, 20, 81, 21))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.labelFile.setFont(font)
        self.labelFile.setObjectName("labelFile")
        self.labelFolder = QtWidgets.QLabel(self.frame)
        self.labelFolder.setGeometry(QtCore.QRect(19, 70, 81, 20))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.labelFolder.setFont(font)
        self.labelFolder.setObjectName("labelFolder")
        self.lineEditFile = QtWidgets.QLineEdit(self.frame)
        self.lineEditFile.setGeometry(QtCore.QRect(110, 20, 371, 21))
        self.lineEditFile.setReadOnly(True)
        self.lineEditFile.setObjectName("lineEditFile")
        self.lineEditFolder = QtWidgets.QLineEdit(self.frame)
        self.lineEditFolder.setGeometry(QtCore.QRect(110, 70, 371, 21))
        self.lineEditFolder.setReadOnly(True)
        self.lineEditFolder.setObjectName("lineEditFolder")
        self.processFile = QtWidgets.QPushButton(self.frame)
        self.processFile.setGeometry(QtCore.QRect(210, 100, 151, 41))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.processFile.setFont(font)
        self.processFile.setObjectName("processFile")
        self.readyLabel = QtWidgets.QLabel(self.frame)
        self.readyLabel.setGeometry(QtCore.QRect(190, 150, 181, 21))
        font = QtGui.QFont()
        font.setFamily(".Aqua Kana")
        self.readyLabel.setFont(font)
        self.readyLabel.setText("")
        self.readyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.readyLabel.setObjectName("readyLabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HARalyzer"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; color:#ffffff;\">Analyze </span></p><p align=\"center\"><span style=\" font-size:24pt; color:#ffffff;\">HAR file</span></p></body></html>"))
        self.chooseFile.setText(_translate("MainWindow", "Browse"))
        self.chooseDirectory.setText(_translate("MainWindow", "Browse"))
        self.labelFile.setText(_translate("MainWindow", "Choose HAR"))
        self.labelFolder.setText(_translate("MainWindow", "Save .ppt to"))
        self.processFile.setText(_translate("MainWindow", "Analyze"))