from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QVBoxLayout, QTreeWidget, QTreeWidgetItem, \
    QComboBox, QHBoxLayout, QTabWidget, QListWidget

from Dialogs import AddBookDialog
from Services import BookService, UserService


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.button_login = QPushButton('Login')

        self.username.setPlaceholderText('Username')
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)

        layout = QVBoxLayout()
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.button_login)
        self.setLayout(layout)

        self.button_login.clicked.connect(lambda: parent.request_login(self.username.text(), self.password.text()))

    def blockSignals(self, bool):
        self.button_login.blockSignals(bool)

    def clear(self):
        self.username.clear()
        self.password.clear()


class UserWidget(QWidget):
    def __init__(self, parent=None):
        super(UserWidget, self).__init__(parent)
        self.__books = None

        self.book_service = BookService(self)
        self.user_id = UserService.user_id

        self.button_add_book = QPushButton('Add book')
        self.button_remove_book = QPushButton('Remove book')
        self.button_borrow_book = QPushButton('Borrow book')
        self.button_return_book = QPushButton('Return book')
        self.filter_choice = QComboBox()
        self.book_search_input = QLineEdit()
        self.book_list = QTreeWidget()
        self.button_logout = QPushButton('Logout')

        self.filter_choice.addItems(['All', 'Available', 'Borrowed'])
        self.button_remove_book.setEnabled(False)
        self.button_borrow_book.setEnabled(False)
        self.button_return_book.setEnabled(False)
        self.book_search_input.setPlaceholderText('Search books')
        self.book_list.setMinimumWidth(400)
        self.book_list.setHeaderLabels(['Author', 'Title', 'Publish year', 'Status'])
        self.book_list.setIndentation(0)

        left_column = QVBoxLayout()
        left_column.addWidget(self.filter_choice)
        left_column.addWidget(self.button_add_book)
        left_column.addWidget(self.button_remove_book)
        left_column.addWidget(self.button_borrow_book)
        left_column.addWidget(self.button_return_book)
        left_column.addStretch()
        left_column.addWidget(self.button_logout)

        right_column = QVBoxLayout()
        right_column.addWidget(self.book_search_input)
        right_column.addWidget(self.book_list)

        layout = QHBoxLayout()
        layout.addLayout(left_column)
        layout.addLayout(right_column)
        self.setLayout(layout)

        self.refresh()

        self.filter_choice.currentIndexChanged.connect(self.refresh)
        self.button_add_book.clicked.connect(self.add_book)
        self.button_remove_book.clicked.connect(
            lambda: self.book_service.delete_book(
                self.__books[self.book_list.currentIndex().row()]
            )
        )
        self.button_borrow_book.clicked.connect(
            lambda: self.book_service.borrow_book(
                self.__books[self.book_list.currentIndex().row()]
            )
        )
        self.button_return_book.clicked.connect(
            lambda: self.book_service.return_book(
                self.__books[self.book_list.currentIndex().row()]
            )
        )
        self.book_search_input.textChanged.connect(self.refresh)
        self.book_list.currentItemChanged.connect(self.book_choice)
        self.button_logout.clicked.connect(parent.request_logout)

    @pyqtSlot()
    def refresh(self):
        self.book_list.clear()
        self.apply_filters()
        for book in self.__books:
            item = QTreeWidgetItem([
                ', '.join([' '.join([author['name'], author['surname']]) for author in book['authors']]),
                book['title'],
                str(book['publishmentYear']),
                'Available' if book['assignUser'] is None else
                ('Unavailable' if book['assignUser']['id'] != self.user_id else 'Borrowed')
            ])
            self.book_list.addTopLevelItem(item)

    def apply_filters(self):
        self.__books = self.book_service.books
        search = self.book_search_input.text().lower()
        if search is not None:
            self.__books = filter(lambda x: True if x['title'].lower().find(search) > -1 else False, self.__books)
        if self.filter_choice.currentIndex() == 1:
            self.__books = filter(lambda x: True if x['assignUser'] is None else False, self.__books)
        if self.filter_choice.currentIndex() == 2:
            self.__books = filter(lambda x: True if x['assignUser'] == self.user_id else False, self.__books)
        self.__books = list(self.__books)

    def book_choice(self, index):
        selected = self.book_list.currentIndex().row()
        if selected == -1:
            self.button_remove_book.setEnabled(False)
            self.button_borrow_book.setEnabled(False)
            self.button_return_book.setEnabled(False)
            return
        book = self.__books[selected]
        self.button_remove_book.setEnabled(True)
        if book['assignUser'] is None:
            self.button_borrow_book.setEnabled(True)
        else:
            self.button_borrow_book.setEnabled(False)
            if book['assignUser']['id'] == self.user_id:
                self.button_return_book.setEnabled(True)
            else:
                self.button_return_book.setEnabled(False)

    def add_book(self):
        ok, book = AddBookDialog.get_result()
        if not ok:
            return
        self.book_service.add_book(book)


class AdminWidget(QTabWidget):
    def __init__(self, parent=None):
        self.__users = None

        self.user_service = UserService(self)

        super(AdminWidget, self).__init__(parent)
        self.button_add_user = QPushButton('Add user')
        self.button_remove_user = QPushButton('Remove user')
        self.user_search_input = QLineEdit()
        self.user_list = QListWidget()
        self.button_logout = QPushButton('Logout')

        self.user_search_input.setPlaceholderText('Search users')
        self.user_list.setMinimumWidth(400)

        left_column = QVBoxLayout()
        left_column.addWidget(self.button_add_user)
        left_column.addWidget(self.button_remove_user)
        left_column.addStretch()
        left_column.addWidget(self.button_logout)

        right_column = QVBoxLayout()
        right_column.addWidget(self.user_search_input)
        right_column.addWidget(self.user_list)

        layout = QHBoxLayout()
        layout.addLayout(left_column)
        layout.addLayout(right_column)

        widget = QWidget()
        widget.setLayout(layout)

        self.addTab(widget, 'Users manager')
        self.addTab(UserWidget(parent), 'Books manager')

        self.user_search_input.textChanged.connect(self.refresh)
        self.button_logout.clicked.connect(parent.request_logout)

    @pyqtSlot()
    def refresh(self):
        self.user_list.clear()
        self.search()
        self.user_list.addItems([user['username'] for user in self.__users])

    def search(self):
        self.__users = self.user_service.users
        search = self.user_search_input.text().lower()
        if search is not None:
            self.__users = filter(lambda x: True if x['username'].lower().find(search) > -1 else False, self.__users)
        self.__users = list(self.__users)


class AddUser(QWidget):
    def __init__(self, parent=None):
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

