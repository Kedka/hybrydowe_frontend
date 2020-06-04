import requests
from PyQt5.QtCore import QRunnable, QMetaObject, Qt, Q_ARG


class RequestRunnable(QRunnable):
    def __init__(self, parent, callback, url):
        QRunnable.__init__(self)
        self.url = 'https://library-app3.herokuapp.com/' + url
        self.parent = parent
        self.callback = callback


class RequestGetRunnable(RequestRunnable):
    def run(self):
        r = requests.get(self.url)
        getattr(self.parent, self.callback)(r)


class RequestPostRunnable(RequestRunnable):
    def __init__(self, parent, callback, url, data):
        super(RequestPostRunnable, self).__init__(parent, callback, url)
        self.data = data

    def run(self):
        r = requests.post(self.url, json=self.data)
        getattr(self.parent, self.callback)(self.data, r)


class RequestDeleteRunnable(RequestRunnable):
    def __init__(self, parent, callback, url, params):
        super(RequestDeleteRunnable, self).__init__(parent, callback, url)
        self.params = params

    def run(self):
        r = requests.post(self.url, params={'id': self.params.get('id')})
        getattr(self.parent, self.callback)(self.params, r)


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
