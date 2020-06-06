from PyQt5.QtCore import QRunnable


class RequestRunnable(QRunnable):
    def __init__(self, parent, session, callback, url, params=None, package=None):
        QRunnable.__init__(self)
        self.url = 'https://library-app3.herokuapp.com/' + url
        self.parent = parent
        self.callback = callback
        self.session = session
        self.params = params
        self.package = package


class RequestGetRunnable(RequestRunnable):
    def run(self):
        r = self.session.get(self.url, params=self.params)
        getattr(self.parent, self.callback)(r)


class RequestDeleteRunnable(RequestRunnable):
    def run(self):
        r = self.session.delete(self.url, params=self.params)
        getattr(self.parent, self.callback)(self.package, r)


class RequestPostRunnable(RequestRunnable):
    def __init__(self, parent, session, callback, url, params=None, data=None, package=None):
        super(RequestPostRunnable, self).__init__(parent, session, callback, url, params, package)
        self.data = data

    def run(self):
        r = self.session.post(self.url, json=self.data, params=self.params)
        getattr(self.parent, self.callback)(self.package, r)
