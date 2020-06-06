import requests
from PyQt5.QtCore import QThreadPool, QMetaObject, Qt, Q_ARG

from Runnable import RequestGetRunnable, RequestPostRunnable, RequestDeleteRunnable


class Service:
    session = None
    user_id = None
    username = None

    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def check_response(response):
        if response.status_code != requests.codes.ok:
            print(response.text)
            raise ConnectionError(response.status_code)


class AuthorizationService(Service):
    def __init__(self, parent):
        super(AuthorizationService, self).__init__(parent)
        self.user_type = None

    def login(self, login, password):
        Service.session = requests.Session()
        runnable = RequestPostRunnable(
            self,
            self.session,
            'handle_login',
            'user/login',
            data={'username': login, 'password': password}
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_login(self, data, response):
        print(response.status_code, type(response.status_code))
        if response.status_code == 403:
            print('elo')
            QMetaObject.invokeMethod(
                self.parent,
                "login",
                Qt.QueuedConnection,
                Q_ARG(str, None)
            )
            return
        self.check_response(response)
        response = response.json()
        Service.user_id = response.get('id')
        Service.username = response.get('username')
        self.user_type = response.get('type')
        QMetaObject.invokeMethod(
            self.parent,
            "login",
            Qt.QueuedConnection,
            Q_ARG(str, self.user_type)
        )

    def logout(self):
        runnable = RequestGetRunnable(
            self,
            self.session,
            'handle_logout',
            'user/logout'
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_logout(self, response):
        self.check_response(response)
        Service.session = None
        Service.user_id = None
        Service.username = None
        QMetaObject.invokeMethod(
            self.parent,
            "logout",
            Qt.QueuedConnection
        )


class BookService(Service):
    def __init__(self, parent):
        super(BookService, self).__init__(parent)
        self.books = []
        self.get_books()

    def get_books(self):
        runnable = RequestGetRunnable(
            self,
            self.session,
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
            self.session,
            'handle_add_book',
            'book/add',
            data=book,
            package=book
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
            self.session,
            'handle_delete_book',
            'book/delete',
            params={'id': book['id']},
            package=book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_delete_book(self, data, response):
        self.check_response(response)
        self.books.remove(data)
        self.notify_parent()

    def borrow_book(self, book):
        runnable = RequestPostRunnable(
            self,
            self.session,
            'handle_borrow_book',
            'book/borrow',
            params={'id': book['id']},
            package=book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_borrow_book(self, data, response):
        self.check_response(response)
        self.books[self.books.index(data)].update({'assignUser': {'id': self.user_id}})
        self.notify_parent()

    def return_book(self, book):
        runnable = RequestPostRunnable(
            self,
            self.session,
            'handle_return_book',
            'book/return',
            params={'id': book['id']},
            package=book
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_return_book(self, data, response):
        self.check_response(response)
        self.books[self.books.index(data)].update({'assignUser': None})
        self.notify_parent()

    def notify_parent(self):
        QMetaObject.invokeMethod(
            self.parent,
            "refresh",
            Qt.QueuedConnection
        )


class UserService(Service):
    def __init__(self, parent):
        super(UserService, self).__init__(parent)
        self.users = []
        self.get_users()

    def get_users(self):
        runnable = RequestGetRunnable(
            self,
            self.session,
            'handle_get_users',
            'admin/users'
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_get_users(self, response):
        self.check_response(response)
        self.users = response.json()
        self.notify_parent()

    def add_user(self, user):
        runnable = RequestPostRunnable(
            self,
            self.session,
            'handle_add_user',
            'admin/user/add',
            data=user,
            package=user
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_add_user(self, data, response):
        self.check_response(response)
        self.users.append(data)
        self.notify_parent()

    def delete_user(self, user):
        runnable = RequestDeleteRunnable(
            self,
            self.session,
            'handle_delete_user',
            'admin/user/delete',
            params={'username': user['username']},
            package=user
        )
        QThreadPool.globalInstance().start(runnable)

    def handle_delete_user(self, data, response):
        self.check_response(response)
        self.users.remove(data)
        self.notify_parent()

    def notify_parent(self):
        QMetaObject.invokeMethod(
            self.parent,
            "refresh",
            Qt.QueuedConnection
        )
