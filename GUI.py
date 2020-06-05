from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QDesktopWidget, QStatusBar
from PyQt5.QtCore import Qt, QRect

from Widgets import *
from Services import AuthorizationService


class LibraryApp(QMainWindow):
    def __init__(self, parent=None):
        super(LibraryApp, self).__init__(parent, flags=Qt.Window)
        self.authorization_service = AuthorizationService(self)

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
        self.login('user')
        # self.authorization_service.login(username, password)

    def login(self, user_type):
        # print(user_type)
        self.centralWidget().widget(0).blockSignals(False)
        center = self.geometry().center()
        if user_type == 'admin':
            self.centralWidget().addWidget(AdminWidget(self))
        else:
            self.centralWidget().addWidget(UserWidget(self))
        self.centralWidget().setCurrentIndex(1)
        self.adjust_geometry(center)
        self.status_bar.clearMessage()

    def request_logout(self):
        # runnable = RequestLogoutRunnable(self)
        # QThreadPool.globalInstance().start(runnable)
        self.logout()

    def logout(self):
        center = self.geometry().center()
        self.centralWidget().removeWidget(self.centralWidget().widget(1))
        self.adjust_geometry(center)

    def add_user(self):
        center = self.geometry().center()
        add_user = AddUser(self)
        self.centralWidget.addWidget(add_user)
        self.centralWidget.setCurrentWidget(add_user)
        self.adjust_geometry(center)
        print('Add user')

    def confirm_reg(self):
        print('Confirmed')
        self.back()

    def delete_user(self):
        center = self.geometry().center()
        delete_user = DeleteUser(self)
        self.centralWidget.addWidget(delete_user)
        self.centralWidget.setCurrentWidget(delete_user)
        self.adjust_geometry(center)
        print('Delete user')

    def add_book(self):
        center = self.geometry().center()
        add_book = AddBook(self)
        self.centralWidget.addWidget(add_book)
        self.centralWidget.setCurrentWidget(add_book)
        self.adjust_geometry(center)

    def add_book_to_db(self):
        print('Book added')
        self.back()

    def delete_book(self):
        center = self.geometry().center()
        delete_book = DeleteBook(self)
        self.centralWidget.addWidget(delete_book)
        self.centralWidget.setCurrentWidget(delete_book)
        self.adjust_geometry(center)
        print('Delete book')

    def back(self):
        center = self.geometry().center()
        self.centralWidget.removeWidget(self.centralWidget.currentWidget())
        self.adjust_geometry(center)

    def show_detail(self):
        center = self.geometry().center()
        book_detail = BookDetails(self)
        self.centralWidget.addWidget(book_detail)
        self.centralWidget.setCurrentWidget(book_detail)
        self.adjust_geometry(center)
        print('Details')

    def place_order(self):
        print('Order')
        self.back()

    def adjust_geometry(self, center):
        self.adjustSize()
        width = self.geometry().width()
        height = self.geometry().height()
        geometry = QRect(center.x() - width/2,
                         center.y() - height/2,
                         width, height)
        self.setGeometry(geometry)
