#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
from BluetoothDialog import Ui_BluetoothDialog
import json

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig,
                                            _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class BluetoothDialogBox(QtGui.QDialog, Ui_BluetoothDialog):
    def __init__(self, parent=None, baudrate=None, timeout=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_BluetoothDialog()
        self.ui.setupUi(self, baudrate, timeout)
    def getValues(self):
        return self.ui.getValues()

##class BluetoothDialogBox(Ui_BluetoothDialog):
##    def __init__(self, parent=None, baudrate=None, timeout=None):
##        #QtGui.QDialog.__init__(self, parent)
##        self.ui = Ui_BluetoothDialog()
##        self.ui.setupUi(parent, baudrate, timeout)
##        self.ui.show()
##    def getValues(self):
##        return self.ui.getValues()

def find(item, array):
    if item not in array:
        return -1
    else:
        for i in range(0, len(array), 1):
            if array[i] == item:
                return i

class ImageViewer(QtGui.QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.connectedDevice = False
        self.imageByteArrays = []
        self.imageBufferStart = False

        self.takePictureCommand = "TP"
        self.setCameraPositionCommand = "SP"
        
        self.printer = QtGui.QPrinter()
        self.scaleFactor = 0.0

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                    QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.centralwidget)

        self.verticalLayout.addWidget(self.scrollArea)
        
        self.createButtons()
        self.createToolbar()
        self.createActions()
        self.createMenus()

        self.setWindowTitle("Blink Image Viewer")
        self.resize(1000, 500)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start()

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                     QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Blink Image Viewer",
                                              "Cannot load %s." % fileName)
                return
            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()
    def saveas(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self, "Sava As File",
                                                     QtCore.QDir.currentPath())
        if fileName:
            with open(fileName, 'wb') as f:
                p = bytearray(self.imageByteArrays[-1])
                f.write(p)
                
    def connect(self):
        if self.connectedDevice == False:
            dlg = BluetoothDialogBox(baudrate=115200, timeout=3)
            dlg.exec_()
            val = dlg.getValues()
            if val[0] != True:
                QtGui.QMessageBox.information(self, "Blink Image Viewer",
                                              "Cannot connect to %s."%val[1])
                return
            self.serialDevice = val[2]
            self.connectedDevice = True
            self.sendMessageAct.setEnabled(True)
            self.snapshotButton.setEnabled(True)
            self.cameraPositionSlider.setEnabled(True)
            self.connectAct.setText("Disconnect")

            self.updateCameraPosition()
        else:
            self.serialDevice.close()
            self.connectedDevice = False
            self.sendMessageAct.setEnabled(False)
            self.snapshotButton.setEnabled(False)
            self.cameraPositionSlider.setEnabled(False)
            self.connectAct.setText("Connect")

    def sendMessage(self):
        text, ok = QtGui.QInputDialog.getText(self, "Send port message",
                "Message:", QtGui.QLineEdit.Normal,
                QtCore.QDir.home().dirName())
        if ok and text != '':
            self.sendMessage2ComPort(text)

    def sendMessage2ComPort(self, text):
        self.serialDevice.write(str(text))
    
    def saveDisplayImage(self):
        with open('Images.json', 'w') as f:
            json.dump(self.imageByteArrays, f)

        #with open('Images.json', 'r') as f:
        #    self.imageByteArrays = json.load(f)

        choice = QtGui.QMessageBox.question(self, "Blink Image Viewer",
                                            "An Image has been recieved.\nDo you want to view?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.No:
            return

        #with open('NewImage.txt', 'w') as f:
        #    for i in self.imageByteArrays[-1]:#bytearray(self.imageByteArrays[-1]):
        #        f.write(str(i))

        #return

        fileName = 'NewImage.jpg'
        
        if fileName:
            with open(fileName, 'wb') as f:
                p = bytearray(self.imageByteArrays[-1])
                f.write(p)
        image = QtGui.QImage(fileName)
        if image.isNull():
            print "Received invalid image"
            return

        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
        self.scaleFactor = 1.0

        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()

        #self.fitToWindowAct.setChecked(True)
        #self.fitToWindow()
            
    def close(self):
        if self.connectedDevice == True:
            self.serialDevice.close()
            self.connectedDevice = False
        with open('Images.json', 'w') as f:
            json.dump(self.imageByteArrays, f)
        super(ImageViewer, self).close()

    def print_(self):
        dialog = QtGui.QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QtGui.QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def requestPicture(self):
        self.sendMessage2ComPort(self.takePictureCommand)

    def updateCameraPosition(self):
        value = int(self.cameraPositionSlider.value())
        self.sendMessage2ComPort(self.setCameraPositionCommand+";"+str(value))
    
    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def about(self):
        QtGui.QMessageBox.about(self, "About Image Viewer",
                "<p>The <b>Image Viewer</b> example shows how to combine "
                "QLabel and QScrollArea to display an image. QLabel is "
                "typically used for displaying text, but it can also display "
                "an image. QScrollArea provides a scrolling view around "
                "another widget. If the child widget exceeds the size of the "
                "frame, QScrollArea automatically provides scroll bars.</p>"
                "<p>The example demonstrates how QLabel's ability to scale "
                "its contents (QLabel.scaledContents), and QScrollArea's "
                "ability to automatically resize its contents "
                "(QScrollArea.widgetResizable), can be used to implement "
                "zooming and scaling features.</p>"
                "<p>In addition the example shows how to use QPainter to "
                "print an image.</p>")
    
    def createButtons(self):
        self.snapshotButton = QtGui.QPushButton(QtGui.QIcon("snapshotButton_01.jpg"), "Snapshot")
        self.snapshotButton.setObjectName(_fromUtf8("snapshotButton"))
        self.snapshotButton.setEnabled(False)
        self.snapshotButton.clicked.connect(self.requestPicture)

        self.cameraPositionSlider = QtGui.QSlider()
        self.cameraPositionSlider.setEnabled(False)
        self.cameraPositionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.cameraPositionSlider.setObjectName(_fromUtf8("cameraPositionSlider"))
        self.cameraPositionSlider.setTickInterval(1)
        self.cameraPositionSlider.setTickPosition(self.cameraPositionSlider.TicksAbove)
        self.cameraPositionSlider.setMinimum(0)
        self.cameraPositionSlider.setMaximum(1024)
        self.cameraPositionSlider.setMaximumWidth(150)
        self.cameraPositionSlider.sliderReleased.connect(self.updateCameraPosition)

    def createToolbar(self):
        self.toolbar = QtGui.QToolBar(self)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        self.toolbar.toolButtonStyle()
        self.toolbar.addWidget(self.snapshotButton)
        self.toolbar.addWidget(self.cameraPositionSlider)

        self.verticalLayout.addWidget(self.toolbar)

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.saveasAct = QtGui.QAction("&Save As...", self, shortcut="Shift+Ctrl+S",
                triggered=self.saveas)
        
        self.connectAct = QtGui.QAction("&Connect...", self, shortcut="Shift+Ctrl+C",
                triggered=self.connect)

        self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
                enabled=False, triggered=self.print_)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitToWindow)

        self.sendMessageAct = QtGui.QAction("Send &message", self, shortcut="Ctrl+M",
                                            enabled=False, triggered=self.sendMessage)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveasAct)
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.cameraMenu = QtGui.QMenu("&Camera", self)
        self.cameraMenu.addAction(self.connectAct)
        self.cameraMenu.addAction(self.sendMessageAct)
        
        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.cameraMenu)
        self.menuBar().addMenu(self.helpMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                                + ((factor - 1) * scrollBar.pageStep()/2)))

    def timerEvent(self):
        if self.connectedDevice == True:
            if int(self.serialDevice.inWaiting()) <= 0:
                return
            
            cmd = self.serialDevice.readall()
            cmd = cmd.split(",")
            #print "cmd =",cmd
            
            image_start_index = find("JPG_S", cmd)
            image_end_index = find("JPG_E", cmd)
            displayImage = False
            
            if image_start_index < 0:
                if self.imageBufferStart == True:
                    #image started in previous data
                    if image_end_index >= 0:#with end
                        image = [int(f) for f in cmd[0:image_end_index]]
                        self.imageByteArrays[-1].append(image)
                        self.imageBufferStart = False
                        displayImage = True
                    else: #without end
                        image = [int(f) for f in cmd[0:]]
                        self.imageByteArrays[-1].append(image)
                else:
                    self.excuteCommand(cmd)#image not started
            else:
                if self.imageBufferStart == True:
                    print "Error #Over-writing previously written image buffer because no JPEG_E Received"
                    if image_end_index < 0:#with start but no end
                        image = [int(f) for f in cmd[image_start_index+1:]]
                        self.imageByteArrays[-1].append(image)
                    else:                  #with start and end
                        image = [int(f) for f in cmd[image_start_index+1:image_end_index]]
                        self.imageByteArrays[-1].append(image)
                        self.imageBufferStart = False
                        displayImage = True
                else:
                    if image_end_index < 0:#with start but no end
                        image = [int(f) for f in cmd[image_start_index+1:]]
                        self.imageByteArrays.append(image)
                    else:                  #with start and end
                        image = [int(f) for f in cmd[image_start_index+1:image_end_index]]
                        self.imageByteArrays.append(image)
                        self.imageBufferStart = False
                        displayImage = True
            if displayImage == True:
                self.saveDisplayImage()
        else:
            pass
            
    def excuteCommand(self, array):
        if len(array) <= 0:
            return
        else:
            print "Function =",array

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())
