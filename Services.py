import requests

from PyQt5.QtCore import Qt, QRunnable, QMetaObject, Q_ARG


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