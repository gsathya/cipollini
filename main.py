import sys
import re

import tools
from log import LogViewer

from PySide import QtGui, QtCore

class Communicate(QtCore.QObject):
    # msg displayed in the status bar
    status_msg = QtCore.Signal(str)
    # output from tor process
    bootstrap_msg = QtCore.Signal(str)

class Cipollini(QtGui.QMainWindow):
    def __init__(self):
        super(Cipollini, self).__init__()

        # intialise widgets
        self.main_widget = MainWidget(self)
        self.setCentralWidget(self.main_widget)

        # intialise status bar
        self.status_bar = self.statusBar()
        self.main_widget.btn_frame.comms.status_msg.connect(self.status_bar.showMessage)

        # fix size and position
        self.setGeometry(500, 500, 350, 250)
        self.center()

        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('CDE'))
        self.setWindowTitle('Cipollini')
        self.draw_bg()
        self.show()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size =  self.geometry()
        self.move((screen.width()-size.width())/2,
                (screen.height()-size.height())/2)

    def draw_bg(self):
        bg = QtGui.QImage('./images/bg.png')
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, bg)
        self.setPalette(palette)

class MainWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(MainWidget, self).__init__()
        self.init()

    def init(self):
        # initialise tool tips
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.status_frame = StatusFrame(self)
        self.btn_frame = BtnFrame(self)
        self.btn_frame.comms.bootstrap_msg.connect(self.status_frame.update_progressbar)
        self.btn_frame.comms.bootstrap_msg.connect(self.btn_frame.log_viewer.update_log)

        # place them all vertically
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.status_frame)
        vbox.addWidget(self.btn_frame)

        self.setLayout(vbox)

class StatusFrame(QtGui.QFrame):
    def __init__(self, parent):
        super(StatusFrame, self).__init__()
        self.init()

    def init(self):
        # progress bar
        self.pbar = QtGui.QProgressBar(self)
        self.pbar.resize(self.pbar.sizeHint())
        self.pbar.setValue(0)
        self.pbar.setTextVisible(True)

        self.setFrameStyle(QtGui.QFrame.StyledPanel)

        # place them all vertically
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.pbar)

        self.setLayout(vbox)

    @QtCore.Slot(str)
    def update_progressbar(self, msg):
        if msg == "Stopped Tor":
            self.pbar.setValue(0)
        else:
            progress = tools.parse_bootstrap_msg(msg)
            if progress:
                self.pbar.setValue(progress)

class BtnFrame(QtGui.QFrame):
    def __init__(self, parent):
        self.tor_process = None
        self.tor_start = False
        self.log_viewer = LogViewer(self)
        self.comms = Communicate()

        super(BtnFrame, self).__init__()
        self.init()

    def init(self):
        # button to start/stop Tor
        main_btn = QtGui.QPushButton('Start Tor', self)
        main_btn.clicked.connect(self.main_btn_clicked)
        main_btn.resize(main_btn.sizeHint())

        # show logs
        log_btn = QtGui.QPushButton('Show Logs', self)
        log_btn.clicked.connect(self.show_logs)
        log_btn.resize(log_btn.sizeHint())

        # button to kill cipollini
        quit_btn = QtGui.QPushButton('Quit', self)
        quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        quit_btn.resize(quit_btn.sizeHint())

        # initialise a horizontal box layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(main_btn)
        hbox.addWidget(log_btn)
        hbox.addWidget(quit_btn)

        self.setLayout(hbox)
        self.setFrameStyle(QtGui.QFrame.StyledPanel)

    def read_tor_msg(self):
        msg = str(self.tor_process.readAll())
        self.comms.bootstrap_msg.emit(msg.strip())
        if "100%" in msg:
            self.comms.status_msg.emit("Started Tor")

    def start_tor(self, main_btn):
        self.tor_start = True
        self.tor_process = tools.launch_tor()
        self.tor_process.readyReadStandardOutput.connect(self.read_tor_msg)
        main_btn.setText("Stop Tor")
        self.comms.status_msg.emit("Bootstrapping Tor")

    def stop_tor(self, main_btn):
        # stop Tor
        self.tor_process.kill()
        self.tor_start = False
        self.comms.status_msg.emit("Stopped Tor")
        self.comms.bootstrap_msg.emit("Stopped Tor")
        main_btn.setText("Start Tor")

    def main_btn_clicked(self):
        main_btn = self.sender()
        if not self.tor_start:
            self.start_tor(main_btn)
        else:
            self.stop_tor(main_btn)

    def show_logs(self):
        if self.log_viewer:
            self.log_viewer.show()
        else:
            # raise Exception
            pass

def main():
    app = QtGui.QApplication(sys.argv)
    cipollini = Cipollini()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
