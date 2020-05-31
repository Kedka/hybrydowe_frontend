from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from Widgets import LoginWidget, AdminWidget


class LibraryApp(QMainWindow):
    def __init__(self, parent=None):
        super(LibraryApp, self).__init__(parent, flags=Qt.Window)
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)

        login_widget = LoginWidget(self)
        self.centralWidget.addWidget(login_widget)

        desktop = QDesktopWidget()
        screen_center = desktop.screenGeometry().center()
        self.adjust_geometry(screen_center)

    def login(self):
        center = self.geometry().center()
        admin_widget = AdminWidget(self)
        self.centralWidget.addWidget(admin_widget)
        self.centralWidget.setCurrentWidget(admin_widget)
        self.adjust_geometry(center)
        print('Logged in')

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
