import requests
from PyQt5.QtCore import QThreadPool

from Runnable import RequestGetRunnable, RequestPostRunnable, RequestDeleteRunnable


def check_response(response):
    if response.status_code != requests.codes.ok:
        raise ConnectionError()


class Service:
    def __init__(self, parent):
        self.parent = parent


class BookService(Service):
    def __init__(self, parent):
        super(BookService, self).__init__(parent)
        self.books = []

    def get_books(self):
        runnable = RequestGetRunnable(self, 'handle_get_books', 'books')
        QThreadPool.globalInstance().start(runnable)

    def handle_get_books(self, response):
        check_response(response)
        self.books = response.json()
        self.notify_parent()

    def add_book(self, book):
        runnable = RequestPostRunnable(self, 'check_response', 'book/add', book)
        QThreadPool.globalInstance().start(runnable)

    def handle_add_book(self, data, response):
        check_response(response)
        db_id = response.json().get('message')[20:]
        data.update({'id': db_id, 'assignUser': None})
        self.books.append(data)

    def delete_book(self, book):
        runnable = RequestDeleteRunnable(self, 'check_response', 'book/delete', book)
        QThreadPool.globalInstance().start(runnable)

    def handle_delete_book(self, data, response):
        check_response(response)
        self.books.remove(data)
        self.notify_parent()

    # def borrow_book(self, book):
    #     runnable = RequestPostRunnable(self, 'check_response', 'book/borrow', vars(book))
    #     QThreadPool.globalInstance().start(runnable)
    #
    # def return_book(self, book):
    #     runnable = RequestPostRunnable(self, 'check_response', 'book/borrow', vars(book))
    #     QThreadPool.globalInstance().start(runnable)

    def notify_parent(self):
        # self.parent.some_method
        pass


class AuthorService(Service):
    def __init__(self, parent):
        super(AuthorService, self).__init__(parent)
        self.authors = []

    def get_authors(self):
        runnable = RequestGetRunnable(self, 'parse_authors', 'authors')
        QThreadPool.globalInstance().start(runnable)

    def parse_authors(self, authors_json):
        print(authors_json)
