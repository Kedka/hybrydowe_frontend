from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QLineEdit, QVBoxLayout, QListWidget, QGridLayout

class LibraryApp(QMainWindow):
    def __init__(self, parent = None):
        super(LibraryApp, self).__init__(parent)
        self.centralWidget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle('Library app')

        loginWidget = LoginWidget(self)
        loginWidget.button.clicked.connect(self.login)
        self.centralWidget.addWidget(loginWidget)

    def login(self):
        print('Logged in')
        adminWidget = AdminWidget(self)
        self.centralWidget.addWidget(adminWidget)
        self.centralWidget.setCurrentWidget(adminWidget)

class LoginWidget(QWidget):
    def __init__(self, parent = None):
        super(LoginWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.userName = QLineEdit()
        self.userName.setPlaceholderText('User ID')
        self.userPasswd = QLineEdit()
        self.userPasswd.setPlaceholderText('Password')
        self.button = QPushButton('Login')

        layout.addWidget(self.userName)
        layout.addWidget(self.userPasswd)
        layout.addWidget(self.button)
        self.setLayout(layout)

class AdminWidget(QWidget):
    def __init__(self, parent = None):
        super(AdminWidget, self).__init__(parent)
        layout = QGridLayout()
        self.buttonAddUser = QPushButton('Add user')
        self.buttonDeleteUser = QPushButton('Delete User')
        self.buttonAddBook = QPushButton('Add book')
        self.buttonDeleteBook = QPushButton('Delete book')

        #layout2 = QVBoxLayout()
        self.list = QListWidget()
        self.list.setMinimumSize(300, 200)
        #self.list.setGeometry(QtCore.QRect(300, 300, 300, 300))

        layout.addWidget(self.buttonAddUser, 0, 0)
        layout.addWidget(self.buttonDeleteUser,1, 0)
        layout.addWidget(self.buttonAddBook, 2, 0)
        layout.addWidget(self.buttonDeleteBook, 3, 0)
        layout.addWidget(self.list, 4, 1)
        #layout.setSpacing(10)

        self.setLayout(layout)
        
        books = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
        self.list.addItems(books)



# Nie wiem czy nie latwiej bedzie zamiast takich przyciskow to po prostu 
# zrobic przy wylistowaniu jakies plusiki i minusiki

# class UserWidget(QWidget):
#     def __init__(self, parent = None):
#         super(AdminWidget, self).__init__(parent)
#         layout = QHBoxLayout()
#         self.buttonRent = QPushButton('Rent a book')
#         self.buttonReturn = QPushButton('Return a book')

#         layout.addWidget(self.buttonRent)
#         layout.addWidget(self.buttonReturn)
#         self.setLayout(layout)
