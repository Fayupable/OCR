import torch.cuda
import json
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog

from settings_auto import Ui_Dialog


class GpuTrigger(QObject):
    trigger = pyqtSignal(bool)

class Settings(QDialog, Ui_Dialog):
    gpu_trigger = GpuTrigger()

    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)
        if not torch.cuda.is_available():
            self.gpuCheckBox.setEnabled(False)
        else:
            with open("assets/settings.json") as json_file:
                json_obj = json.load(json_file)
                setting = json_obj["use_gpu"]
                if setting:
                    self.gpuCheckBox.setChecked(True)
                else:
                    self.gpuCheckBox.setChecked(False)
            self.gpuCheckBox.stateChanged.connect(self.onGpuChanged)

    def onGpuChanged(self):
        if self.gpuCheckBox.isChecked():
            self.gpu_trigger.trigger.emit(True)
        else:
            self.gpu_trigger.trigger.emit(False)