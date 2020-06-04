from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QGridLayout, QTreeWidget, QTreeWidgetItem, QLabel, QMainWindow

from Services import AuthorService, BookService


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

        self.button_login.clicked.connect(parent.request_login)


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
        self.list.addTopLevelItem(QTreeWidgetItem(['D' , 'E', 'F']))

        self.list.itemSelectionChanged.connect(self.details)

        self.parent = parent
        self.button_add_user.clicked.connect(parent.add_user)
        self.button_delete_user.clicked.connect(parent.delete_user)
        self.button_add_book.clicked.connect(parent.add_book)
        self.button_delete_book.clicked.connect(parent.delete_book)

        layout = QGridLayout()
        layout.addWidget(self.button_add_user, 0, 0)
        layout.addWidget(self.button_delete_user, 1, 0)
        layout.addWidget(self.button_add_book, 2, 0)
        layout.addWidget(self.button_delete_book, 3, 0)
        layout.addWidget(self.button_logout, 4, 0)
        layout.addWidget(self.list, 0, 1, 5, 1)

        self.setLayout(layout)

        self.button_logout.clicked.connect(parent.request_logout)

    def details(self):
        getSelected = self.list.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getAuthor = baseNode.text(0)
            getName = baseNode.text(1)

            self.parent.show_detail()


class BookDetails(QWidget):
    def __init__(self, parent = None):
        super(BookDetails, self).__init__(parent)

        # idk how to pass the details here
        self.author = QLabel('Author')
        self.name = QLabel('Title')
        self.place_order = QPushButton('Place order')
        self.button_back = QPushButton('Back')

        self.place_order.clicked.connect(parent.place_order)
        self.button_back.clicked.connect(parent.back)

        layout = QVBoxLayout()
        layout.addWidget(self.author)
        layout.addWidget(self.name)
        layout.addWidget(self.place_order)
        layout.addWidget(self.button_back)

        self.setLayout(layout)


class AddUser(QWidget):
    def __init__(self, parent = None):
        super(AddUser, self).__init__(parent)

        self.username = QLineEdit()
        self.passwd = QLineEdit()
        self.confirm_passwd = QLineEdit()

        self.username.setPlaceholderText('Username')
        self.passwd.setPlaceholderText('Password')
        self.confirm_passwd.setPlaceholderText('Confirm password')

        self.button_register = QPushButton('Register')
        self.button_back = QPushButton('Back')

        self.button_register.clicked.connect(parent.confirm_reg)
        self.button_back.clicked.connect(parent.back)

        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.passwd)
        layout.addWidget(self.confirm_passwd)
        layout.addWidget(self.button_register)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

class DeleteUser(QWidget):
    def __init__(self, parent = None):
        super(DeleteUser, self).__init__(parent)

        layout = QGridLayout()

        self.user_list = QTreeWidget()
        self.user_list.setHeaderLabels(['ID', 'Username'])

        self.button_back = QPushButton('Back')
        self.button_back.clicked.connect(parent.back)

        layout.addWidget(self.user_list)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

class AddBook(QWidget):
    def __init__(self, parent = None):
        super(AddBook, self).__init__(parent)

        self.title = QLineEdit()
        self.author = QLineEdit()

        self.title.setPlaceholderText('Book title')
        self.author.setPlaceholderText('Author name')

        self.button_book2db = QPushButton('Add book')
        self.button_back = QPushButton('Back')

        self.button_book2db.clicked.connect(parent.add_book_to_db)
        self.button_back.clicked.connect(parent.back)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.author)
        layout.addWidget(self.button_book2db)
        layout.addWidget(self.button_back)

        self.setLayout(layout)

class DeleteBook(QWidget):
    def __init__(self, parent = None):
        super(DeleteBook, self).__init__(parent)

        layout = QGridLayout()

        self.book_list = QTreeWidget()
        self.book_list.setHeaderLabels(['ID', 'Title', 'Author'])

        self.button_back = QPushButton('Back')
        self.button_back.clicked.connect(parent.back)

        layout.addWidget(self.book_list)
        layout.addWidget(self.button_back)

        self.setLayout(layout)




# class UserWidget(QWidget):
#     def __init__(self, parent = None):
#         super(AdminWidget, self).__init__(parent)
#         layout = QHBoxLayout()
#         self.buttonRent = QPushButton('Rent a book')
#         self.buttonReturn = QPushButton('Return a book')

#         layout.addWidget(self.buttonRent)
#         layout.addWidget(self.buttonReturn)
#         self.setLayout(layout)
