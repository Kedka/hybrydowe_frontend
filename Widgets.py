from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QGridLayout, QTreeWidget, QTreeWidgetItem


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.username = QLineEdit()
        self.username.setPlaceholderText('User ID')
        self.user_password = QLineEdit()
        self.user_password.setPlaceholderText('Password')
        self.button_login = QPushButton('Login')

        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.user_password)
        layout.addWidget(self.button_login)
        self.setLayout(layout)

        self.button_login.clicked.connect(parent.login)


class AdminWidget(QWidget):
    def __init__(self, parent=None):
        super(AdminWidget, self).__init__(parent)
        self.button_add_user = QPushButton('Add user')
        self.button_delete_user = QPushButton('Delete User')
        self.button_add_book = QPushButton('Add book')
        self.button_delete_book = QPushButton('Delete book')
        self.button_logout = QPushButton('Log out')

        self.list = QTreeWidget()
        self.list.setHeaderLabels(['Author', 'Title'])
        self.list.setIndentation(0)

        self.list.addTopLevelItem(QTreeWidgetItem(['A', 'B', 'C']))

        layout = QGridLayout()
        layout.addWidget(self.button_add_user, 0, 0)
        layout.addWidget(self.button_delete_user, 1, 0)
        layout.addWidget(self.button_add_book, 2, 0)
        layout.addWidget(self.button_delete_book, 3, 0)
        layout.addWidget(self.button_logout, 4, 0)
        layout.addWidget(self.list, 0, 1, 5, 1)

        self.setLayout(layout)

        self.button_logout.clicked.connect(parent.logout)


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
