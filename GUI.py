from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget, QStatusBar
from PyQt5.QtCore import Qt, QRect, pyqtSlot

from Widgets import *
from Services import AuthorizationService


class LibraryApp(QMainWindow):
    def __init__(self, parent=None):
        super(LibraryApp, self).__init__(parent, flags=Qt.Window)
        self.authorization_service = None

        self.setWindowTitle('Library app')
        self.setCentralWidget(QStackedWidget())
        self.centralWidget().addWidget(LoginWidget(self))

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        desktop = QDesktopWidget()
        screen_center = desktop.screenGeometry().center()
        self.adjust_geometry(screen_center)

    def request_login(self, username, password):
        self.status_bar.showMessage('Logging in')
        self.centralWidget().widget(0).blockSignals(True)
        self.authorization_service = AuthorizationService(self)
        self.authorization_service.login(username, password)

    @pyqtSlot(str)
    def login(self, user_type):
        self.centralWidget().widget(0).blockSignals(True)
        self.centralWidget().widget(0).clear()
        center = self.geometry().center()
        if user_type == 'A':
            self.centralWidget().addWidget(AdminWidget(self))
        else:
            self.centralWidget().addWidget(UserWidget(self))
        self.centralWidget().setCurrentIndex(1)
        self.adjust_geometry(center)
        self.status_bar.clearMessage()

    def request_logout(self):
        self.status_bar.showMessage('Logging out')
        self.authorization_service.logout()

    @pyqtSlot()
    def logout(self):
        center = self.geometry().center()
        self.centralWidget().widget(0).blockSignals(False)
        self.centralWidget().removeWidget(self.centralWidget().widget(1))
        self.adjust_geometry(center)
        self.authorization_service = None
        self.status_bar.clearMessage()

    def adjust_geometry(self, center):
        self.adjustSize()
        width = self.geometry().width()
        height = self.geometry().height()
        geometry = QRect(center.x() - width/2,
                         center.y() - height/2,
                         width, height)
        self.setGeometry(geometry)
