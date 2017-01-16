from PyQt4 import QtCore, QtGui
from BluetoothDialog import Ui_BluetoothDialog

class BluetoothDialogBox(QtGui.QDialog, Ui_BluetoothDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_BluetoothDialog()
        self.ui.setupUi(self)

def FUNC_ERROR():
    print "Invalid code"
def TestBluetoothDialog():
    dialog = BluetoothDialogBox()
    if dialog.exec_():
        values = dialog.getValues()
    else:
        raise FUNC_ERROR()

TestBluetoothDialog()
