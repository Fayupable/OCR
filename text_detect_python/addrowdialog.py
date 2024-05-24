from PyQt5.QtCore import QObject, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QDialog, QMessageBox

from addrowdialog_auto import Ui_Dialog


class AddRowTrigger(QObject):
    row_trigger = pyqtSignal(list)


class AddRowDialog(QDialog, Ui_Dialog):
    trigger = AddRowTrigger()

    def __init__(self):
        super(AddRowDialog, self).__init__()
        self.setupUi(self)
        price_validator = QRegExpValidator(QRegExp(r"\d+(\,\d+)?"))
        self.priceLE.setValidator(price_validator)
        self.pushButton.clicked.connect(self.transmitRow)

    def transmitRow(self):
        name = self.nameLE.text().strip()
        price = self.priceLE.text().strip()
        if name == "" or price == "":
            QMessageBox.warning(self, "Hata!", "Alanlar boş bırakılmamalı.")
        elif price[-1] == ",":
            QMessageBox.warning(self, "Hatalı Fiyat!",
                                "Fiyat tam sayı veya ondalıklı sayı olarak girilmelidir!")
        else:
            fields = [name, price]
            self.trigger.row_trigger.emit(fields)
            self.accept()
