from PySide import QtGui, QtCore

class LogViewer(QtGui.QMainWindow):
    def __init__(self, parent):
        super(LogViewer, self).__init__()
        self.init()

    def init(self):
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.viewer = QtGui.QPlainTextEdit()
        self.viewer.setFont(font)
        self.viewer.setReadOnly(True)
        self.viewer.show()

        self.setCentralWidget(self.viewer)
        self.setWindowTitle('Logs')
        self.setGeometry(100, 300, 700, 500)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        elif event.key() == QtCore.Qt.Key_F and \
            (event.modifiers() & QtCore.Qt.ControlModifier):
            # search
            pass

    @QtCore.Slot(str)
    def update_log(self, log):
        self.viewer.appendPlainText(log)
