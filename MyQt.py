__author__ = 'ludek'

import sys
import serial
from PyQt4 import QtGui, QtCore


class Priklad(QtGui.QWidget):

    def __init__(self):
        super(Priklad, self).__init__()

        self.initUI()

        self.dev = False

        # self.conectDevice()

    def initUI(self):

        connectButton = QtGui.QPushButton('Connect')
        exitButton = QtGui.QPushButton('Exit')
        lostatButton = QtGui.QPushButton('Load status')
        dumpButton = QtGui.QPushButton('Dump data')

        connectButton.connect(connectButton, QtCore.SIGNAL('clicked()'), self.connectClicked)
        exitButton.connect(exitButton, QtCore.SIGNAL('clicked()'), self.exitClicked)
        lostatButton.connect(lostatButton, QtCore.SIGNAL('clicked()'), self.lostatClicked)
        dumpButton.connect(dumpButton, QtCore.SIGNAL('clicked()'), self.dumpClicked)

        hbox01 = QtGui.QHBoxLayout()
        hbox01.addWidget(connectButton)
        hbox01.addWidget(lostatButton)
        hbox01.addStretch(1)

        hbox02 = QtGui.QHBoxLayout()
        hbox02.addWidget(dumpButton)
        hbox02.addStretch(1)

        hbox03 = QtGui.QHBoxLayout()
        hbox03.addStretch(1)
        hbox03.addWidget(exitButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox01)
        vbox.addLayout(hbox02)
        vbox.addStretch(1)
        vbox.addLayout(hbox03)

        self.setLayout(vbox)

        # self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('StatusBar')
        self.show()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self.close()

    def connectClicked(self):
        try:
            self.dev = serial.Serial('/dev/ttyUSB0', baudrate=19200, timeout=3.0)
            print 'UART opened'
        except:
            print 'Could not open device!'
        #self.close()

    def lostatClicked(self):
        self.dev.write('s')
        rx = self.dev.read(10)
        print 'Chars loaded: ',
        print len(rx)
        for char in rx:
            print str(char),

    def dumpClicked(self):
        self.dev.write('d')
        rx = self.dev.read(10000)
        print 'Chars loaded: ',
        print len(rx)
        print 'numbers: '
        for char in rx:
            print '{:02x} '.format(ord(char)),

    def exitClicked(self):
        if self.dev:
            print 'UART dev has been opened, close it'
            self.dev.close()

        self.close()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ex = Priklad()
    sys.exit(app.exec_())
