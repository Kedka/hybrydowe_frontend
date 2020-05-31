from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from Widgets import LoginWidget, AdminWidget


class LibraryApp(QMainWindow):
    def __init__(self, parent=None):
        super(LibraryApp, self).__init__(parent, flags=Qt.Window)
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Library app')

        login_widget = LoginWidget(self)
        login_widget.button.clicked.connect(self.login)
        self.centralWidget.addWidget(login_widget)

    def login(self):
        print('Logged in')
        admin_widget = AdminWidget(self)
        self.centralWidget.addWidget(admin_widget)
        self.centralWidget.setCurrentWidget(admin_widget)
