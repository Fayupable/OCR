# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'records.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.searchLE = QtWidgets.QLineEdit(self.centralwidget)
        self.searchLE.setObjectName("searchLE")
        self.gridLayout.addWidget(self.searchLE, 0, 1, 1, 1)
        self.productRecordsTable = QtWidgets.QTableView(self.centralwidget)
        self.productRecordsTable.setObjectName("productRecordsTable")
        self.gridLayout.addWidget(self.productRecordsTable, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        self.mainMenu = QtWidgets.QMenu(self.menubar)
        self.mainMenu.setObjectName("mainMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionUpload = QtWidgets.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.mainMenu.addAction(self.actionUpload)
        self.menubar.addAction(self.mainMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Arama:"))
        self.mainMenu.setTitle(_translate("MainWindow", "Menü"))
        self.actionUpload.setText(_translate("MainWindow", "Kayıt Yükleme"))