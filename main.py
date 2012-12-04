import sys
import re

from PySide import QtGui, QtCore

class Communicate(QtCore.QObject):
    status_msg = QtCore.Signal(str)

class Cipollini(QtGui.QMainWindow):
    def __init__(self):
        super(Cipollini, self).__init__()

        # intialise widgets
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        # intialise status bar
        self.status_bar = self.statusBar()
        self.main_widget.comms.status_msg.connect(self.status_bar.showMessage)

        # fix size and position
        self.setGeometry(300, 300, 250, 150)
        self.center()

        self.setWindowTitle('Cipollini')
        self.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2,
                (screen.height()-size.height())/2)

class MainWidget(QtGui.QWidget):
    def __init__(self, parent):
        self.comms = Communicate()
        self.tor_process = None
        self.tor_start = False

        super(MainWidget, self).__init__()
        self.initUI()

    def initUI(self):
        # initialise tool tips
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.pbar = QtGui.QProgressBar(self)
        self.pbar.resize(self.pbar.sizeHint())
        self.pbar.setTextVisible(True)

        # button to start/stop Tor
        main_btn = QtGui.QPushButton('Start Tor', self)
        main_btn.clicked.connect(self.main_btn_clicked)
        main_btn.resize(main_btn.sizeHint())

        # button to kill cipollini
        quit_btn = QtGui.QPushButton('Quit', self)
        quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quit_btn.resize(quit_btn.sizeHint())

        # initialise a horizontal box layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.pbar)
        hbox.addWidget(main_btn)
        hbox.addWidget(quit_btn)
        self.setLayout(hbox)

    def update_progressbar(self):
        msg = self.tor_process.readAll()
        bootstrap_line = re.compile("Bootstrapped ([0-9]+)%: ")
        bootstrap_match = bootstrap_line.search(msg)
        if bootstrap_match:
            progress = int(bootstrap_match.groups()[0])
            self.pbar.setValue(progress)

    def main_btn_clicked(self):
        main_btn = self.sender()
        if not self.tor_start:
            # start Tor
            self.tor_start = True
            main_btn.setText("Stop Tor")
            self.comms.status_msg.emit("Started Tor")
            self.tor_process = QtCore.QProcess()
            self.tor_process.start("tor")
            self.tor_process.readyReadStandardOutput.connect(self.update_progressbar)
        else:
            # stop Tor
            self.tor_process.kill()
            self.comms.status_msg.emit("Stopped Tor")
            self.tor_start = False
            self.pbar.setValue(0)
            main_btn.setText("Start Tor")

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Cipollini()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
