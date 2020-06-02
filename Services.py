import requests
from PyQt5.QtCore import QThreadPool

from Model import Book
from Runnable import RequestGetRunnable, RequestPostRunnable


class Service:
    def __init__(self, parent):
        self.parent = parent

    def check_response(self, response):
        if response.status_code != requests.codes.ok:
            raise ConnectionError()
        self.notify_parent()


class BookService(Service):
    def __init__(self, parent):
        super(BookService, self).__init__(parent)
        self.books = []

    def get_books(self):
        runnable = RequestGetRunnable(self, 'parse_books', 'books')
        QThreadPool.globalInstance().start(runnable)

    def add_book(self, book):
        runnable = RequestPostRunnable(self, 'check_response', 'book/add', vars(book))
        QThreadPool.globalInstance().start(runnable)

    def delete_book(self, book):
        runnable = RequestPostRunnable(self, 'check_response', 'book/remove', vars(book))
        QThreadPool.globalInstance().start(runnable)

    def borrow_book(self, book):
        runnable = RequestPostRunnable(self, 'check_response', 'book/borrow', vars(book))
        QThreadPool.globalInstance().start(runnable)

    def return_book(self, book):
        runnable = RequestPostRunnable(self, 'check_response', 'book/borrow', vars(book))
        QThreadPool.globalInstance().start(runnable)

    def parse_books(self, books_json):
        self.notify_parent()

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
