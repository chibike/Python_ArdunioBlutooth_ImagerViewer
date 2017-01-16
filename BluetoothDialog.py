from PyQt4 import QtCore, QtGui
import serial.tools.list_ports
import serial

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BluetoothDialog(object):
    def setupUi(self, BluetoothDialog, baudrate, timeout):
        BluetoothDialog.setObjectName(_fromUtf8("BluetoothDialog"))
        BluetoothDialog.resize(371, 112)
        BluetoothDialog.setMinimumSize(QtCore.QSize(371, 112))
        BluetoothDialog.setMaximumSize(QtCore.QSize(371, 112))
        self.windowReference = BluetoothDialog
        self.verticalLayoutWidget = QtGui.QWidget(BluetoothDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(70, 10, 231, 91))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.comPort_comboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comPort_comboBox.setObjectName(_fromUtf8("comPort_comboBox"))
        self.comPort_comboBox.currentIndexChanged.connect(self.portSelected)
        self.comPort_comboBox_index = -1
        #self.comPort_comboBox.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comPort_comboBox)
        self.connect_pushButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.connect_pushButton.setObjectName(_fromUtf8("connect_pushButton"))
        self.connect_pushButton.clicked.connect(self.connect)
        self.verticalLayout.addWidget(self.connect_pushButton)

        self.setupValues(baudrate, timeout) 
        self.retranslateUi(BluetoothDialog)
        QtCore.QMetaObject.connectSlotsByName(BluetoothDialog)

    def retranslateUi(self, BluetoothDialog):
        BluetoothDialog.setWindowTitle(_translate("BluetoothDialog", "Blink Bluetooth Dialog", None))
        self.ports = [i[0] for i in list(serial.tools.list_ports.comports())]
        for i in range(0, len(self.ports), 1):
            self.comPort_comboBox.addItem(_fromUtf8(""))
            self.comPort_comboBox.setItemText(i, _translate("BluetoothDialog", self.ports[i], None))
        if len(self.ports) > 0:
            self.comPort_comboBox.setCurrentIndex(0)
        self.connect_pushButton.setText(_translate("BluetoothDialog", "Connect", None))

    def setupValues(self, baudrate, timeout):
        self.port = "None"
        self.connected = False
        self.serialDevice = "None"
        self.baudrate = int(baudrate)
        self.timeout = int(timeout)
        
    def getValues(self):
        return [self.connected, self.port, self.serialDevice]
    
    def portSelected(self, index):
        self.comPort_comboBox_index = int(index)
        
    def connect(self):
        self.port = str(self.comPort_comboBox.currentText())
        try:
            self.serialDevice = serial.Serial(port=self.port,
                                              baudrate=self.baudrate,
                                              timeout=self.timeout)
            self.connected = True
        except:
            pass#print "Could not connect ="#,self.getValues()
        self.windowReference.close()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    BluetoothDialog = QtGui.QWidget()
    ui = Ui_BluetoothDialog()
    ui.setupUi(BluetoothDialog, 115200, 3)
    BluetoothDialog.show()
    sys.exit(app.exec_())

