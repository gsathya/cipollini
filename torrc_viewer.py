import tools

from PySide import QtGui, QtCore

class TorrcViewer(QtGui.QWidget):
    def __init__(self, torrc_path=None):
        """
        :param str torrc: path to the torrc file
        """
        self.torrc = None
        self.torrc_path = torrc_path

        super(TorrcViewer, self).__init__()
        self.init()

    def init(self):
        if self.torrc_path:
            self.torrc = tools.parse_torrc(self.torrc_path)

        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setFixedPitch(True)
        font.setPointSize(12)

        self.viewer = QtGui.QPlainTextEdit()
        self.viewer.setFont(font)
        if self.torrc:
            self.viewer.setPlainText(self.stringify_torrc())
        self.viewer.setReadOnly(True)

        self.key_edit = QtGui.QLineEdit()
        self.key_edit.setPlaceholderText('Option')
        self.val_edit = QtGui.QLineEdit()
        self.val_edit.setPlaceholderText('Value')

        grid = QtGui.QGridLayout()
        grid.addWidget(self.key_edit, 0, 0)
        grid.addWidget(self.val_edit, 0, 1)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addWidget(self.viewer)

        #self.setCentralWidget(self.viewer)
        self.setLayout(vbox)
        self.setWindowTitle('Torrc')
        self.setGeometry(100, 300, 700, 500)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def stringify_torrc(self):
        output_string = []

        for (key, val) in self.torrc.items():
            output_string.append('%s %s' % (key, val))

        return '\n'.join(output_string)
