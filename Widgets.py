from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QListWidget, QGridLayout


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText('User ID')
        self.user_password = QLineEdit()
        self.user_password.setPlaceholderText('Password')
        self.button = QPushButton('Login')

        layout.addWidget(self.username)
        layout.addWidget(self.user_password)
        layout.addWidget(self.button)
        self.setLayout(layout)


class AdminWidget(QWidget):
    def __init__(self, parent=None):
        super(AdminWidget, self).__init__(parent)
        layout = QGridLayout()
        self.button_add_user = QPushButton('Add user')
        self.button_delete_user = QPushButton('Delete User')
        self.button_add_book = QPushButton('Add book')
        self.button_delete_book = QPushButton('Delete book')

        # layout2 = QVBoxLayout()
        self.list = QListWidget()
        self.list.setMinimumSize(300, 200)
        # self.list.setGeometry(QtCore.QRect(300, 300, 300, 300))

        layout.addWidget(self.button_add_user, 0, 0)
        layout.addWidget(self.button_delete_user, 1, 0)
        layout.addWidget(self.button_add_book, 2, 0)
        layout.addWidget(self.button_delete_book, 3, 0)
        layout.addWidget(self.list, 0, 1, 4, 1)
        # layout.setSpacing(10)

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
