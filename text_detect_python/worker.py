# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject

from safa_yardim import process_receipt, ocr_image


class WorkerSignal(QObject):
    signal = pyqtSignal(str, str, list)


class FinishSignal(QObject):
    signal = pyqtSignal()


class Worker(QObject):
    result_signal = WorkerSignal()
    finish_signal = FinishSignal()

    def __init__(self, file_path, use_gpu):
        super().__init__()
        self.file_path = file_path
        self.use_gpu = use_gpu

    def run(self):
        date_str, store, products = process_receipt(ocr_image(self.file_path, self.use_gpu))
        self.result_signal.signal.emit(date_str, store, products)
        self.finish_signal.signal.emit()
