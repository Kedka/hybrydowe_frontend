import requests
from PyQt5.QtCore import QThreadPool

from Runnable import RequestGetRunnable, RequestPostRunnable, RequestDeleteRunnable


class Service:
    session = None
    # TODO: change to None
    user_id = 1

    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def check_response(response):
        if response.status_code != requests.codes.ok:
            raise ConnectionError()


class AuthorizationService(Service):
    def __init__(self, parent):
        super(AuthorizationService, self).__init__(parent)
        self.user_type = None
        self.username = None

    def login(self, login, password):
        Service.session = requests.Session()
        runnable = RequestPostRunnable(
            self,
            'handle_login',
            'user/login',
            {'username': login, 'password': password}
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_login(self, data, response):
        self.check_response(response)
        response = response.json()
        self.user_id = response.get('id')
        self.user_type = response.get('type')
        self.username = response.get('username')
        self.parent.login(self.user_type)

    def logout(self):
        runnable = RequestPostRunnable(
            self,
            'handle_login',
            'user/logout',
            None
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_logout(self, data, response):
        self.check_response(response)
        self.session = None
        self.parent.logout()


class BookService(Service):
    def __init__(self, parent):
        super(BookService, self).__init__(parent)
        self.books = []
        self.get_books()

    def get_books(self):
        runnable = RequestGetRunnable(
            self,
            'handle_get_books',
            'books'
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_get_books(self, response):
        self.check_response(response)
        self.books = response.json()
        self.notify_parent()

    def add_book(self, book):
        runnable = RequestPostRunnable(
            self,
            'handle_add_book',
            'book/add',
            book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_add_book(self, data, response):
        self.check_response(response)
        db_id = response.json().get('message')[20:]
        data.update({'id': db_id, 'assignUser': None})
        self.books.append(data)
        self.notify_parent()

    def delete_book(self, book):
        runnable = RequestDeleteRunnable(
            self,
            'handle_delete_book',
            'book/delete',
            book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_delete_book(self, data, response):
        self.check_response(response)
        self.books.remove(data)
        self.notify_parent()

    def borrow_book(self, book):
        # TODO: pass only id or change request type
        runnable = RequestPostRunnable(
            self,
            'handle_borrow_book',
            'book/borrow',
            book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_borrow_book(self, data, response):
        self.check_response(response)
        self.books[self.books.index(data)].update({'assignUser': self.user_id})
        self.notify_parent()

    def return_book(self, book):
        runnable = RequestPostRunnable(
            self,
            'handle_return_book',
            'book/return',
            book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_return_book(self, data, response):
        self.check_response(response)
        self.books[self.books.index(data)].update({'assignUser': None})
        self.notify_parent()

    def notify_parent(self):
        self.parent.refresh()


class UserService(Service):
    def __init__(self, parent):
        super(UserService, self).__init__(parent)
        self.users = []
        self.get_users()

    def get_users(self):
        runnable = RequestGetRunnable(self,
                                      'handle_get_users',
                                      'users')
        QThreadPool.globalInstance().start(runnable)

    def handle_get_users(self, response):
        self.check_response(response)
        self.users = response.json()
        self.notify_parent()

    def notify_parent(self):
        self.parent().refresh()
