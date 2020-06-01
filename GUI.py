from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget, QStatusBar, QLabel
from PyQt5.QtCore import Qt, QRect, pyqtSlot, QThreadPool

from Widgets import LoginWidget, AdminWidget
from Services import RequestLoginRunnable, RequestLogoutRunnable


class LibraryApp(QMainWindow):
    def __init__(self, parent=None):
        super(LibraryApp, self).__init__(parent, flags=Qt.Window)
        self.setWindowTitle('Library app')
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        login_widget = LoginWidget(self)
        self.centralWidget.addWidget(login_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        desktop = QDesktopWidget()
        screen_center = desktop.screenGeometry().center()
        self.adjust_geometry(screen_center)

    def request_login(self):
        self.status_bar.showMessage('Logging in')
        runnable = RequestLoginRunnable(self)
        QThreadPool.globalInstance().start(runnable)

    @pyqtSlot(str)
    def login(self, data):
        print(data)
        center = self.geometry().center()
        admin_widget = AdminWidget(self)
        self.centralWidget.addWidget(admin_widget)
        self.centralWidget.setCurrentWidget(admin_widget)
        self.adjust_geometry(center)
        self.status_bar.clearMessage()
        print('Logged in')

    def request_logout(self):
        runnable = RequestLogoutRunnable(self)
        QThreadPool.globalInstance().start(runnable)

    @pyqtSlot()
    def logout(self):
        center = self.geometry().center()
        self.centralWidget.removeWidget(self.centralWidget.currentWidget())
        self.adjust_geometry(center)
        print('Logged out')

    def adjust_geometry(self, center):
        self.adjustSize()
        width = self.geometry().width()
        height = self.geometry().height()
        geometry = QRect(center.x() - width/2,
                         center.y() - height/2,
                         width, height)
        self.setGeometry(geometry)
