import requests
from PyQt5.QtCore import QRunnable, QMetaObject, Qt, Q_ARG


class RequestGetRunnable(QRunnable):
    def __init__(self, parent, callback, url):
        QRunnable.__init__(self)
        self.url = 'https://library-app3.herokuapp.com/' + url
        self.parent = parent
        self.callback = callback

    def run(self):
        r = requests.get(self.url)
        print(type(r.text))
        getattr(self.parent, self.callback)(r.text)


class RequestPostRunnable(QRunnable):
    def __init__(self, parent, callback, url, data):
        QRunnable.__init__(self)
        self.url = 'https://library-app3.herokuapp.com/' + url
        self.parent = parent
        self.callback = callback
        self.data = data

    def run(self):
        r = requests.post(self.url, json=self.data)
        getattr(self.parent, self.callback)(r.text)


class RequestLoginRunnable(QRunnable):
    def __init__(self, target):
        QRunnable.__init__(self)
        self.url = 'https://api.github.com/events'
        self.target = target

    def run(self):
        r = requests.get(self.url)
        QMetaObject.invokeMethod(self.target, "login",
                                 Qt.QueuedConnection,
                                 Q_ARG(str, r.text))


class RequestLogoutRunnable(QRunnable):
    def __init__(self, target):
        QRunnable.__init__(self)
        self.target = target
        self.url = 'https://api.github.com/events'

    def run(self):
        r = requests.get(self.url)
        QMetaObject.invokeMethod(self.target, "logout",
                                 Qt.QueuedConnection)