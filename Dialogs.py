from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QLineEdit, QLabel, QFormLayout, QPushButton, \
    QWidget


class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super(AddBookDialog, self).__init__(parent)
        self.authors = []

        self.title = QLineEdit()
        self.publication_year = QLineEdit()
        self.label_authors = QLabel('Authors')
        self.button_add_author = QPushButton('Add author')

        self.title.setMinimumWidth(200)
        self.publication_year.setMinimumWidth(200)
        self.publication_year.setValidator(QIntValidator())

        self.inputs = QFormLayout()
        self.inputs.addRow('Title:', self.title)
        self.inputs.addRow('Year of publication:', self.publication_year)
        self.inputs.addWidget(self.label_authors)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal,
            self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(self.inputs)
        layout.addWidget(self.button_add_author)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.add_author()

        self.button_add_author.clicked.connect(self.add_author)

    def add_author(self):
        name = QLineEdit()
        surname = QLineEdit()
        name.setMinimumWidth(200)
        surname.setMinimumWidth(200)
        self.authors.append((name, surname))
        self.inputs.addRow('', QWidget())
        self.inputs.addRow('Name:', name)
        self.inputs.addRow('Surname:', surname)

    def get_values(self):
        return {'title': self.title.text(),
                'publishmentYear': self.publication_year.text(),
                'authors': [
                    {'name': name.text(), 'surname': surname.text()} for name, surname in self.authors
                ]}

    @staticmethod
    def get_result(parent=None):
        dialog = AddBookDialog(parent)
        result = dialog.exec_()
        book = dialog.get_values()
        return result, book


class AddUserDialog(QDialog):
    def __init__(self, parent=None):
        super(AddUserDialog, self).__init__(parent)

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.confirm_password = QLineEdit()

        self.username.setPlaceholderText('Username')
        self.passwd.setPlaceholderText('Password')
        self.confirm_passwd.setPlaceholderText('Confirm password')

        inputs = QFormLayout()
        inputs.addRow('Username:', self.username)
        inputs.addRow('Password:', self.password)
        inputs.addRow('Confirm password:', self.confirm_password)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal,
            self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        self.button_accept = buttons.buttons()

        layout = QVBoxLayout()
        layout.addLayout(inputs)
        layout.addWidget(buttons)

        self.setLayout(layout)

        self.username.clicked.connect(self.validate)
        self.password.clicked.connect(self.validate)
        self.confirm_password.clicked.connect(self.validate)

    def validate(self):
        print(self.button_accept)

    def get_values(self):
        return {'username': self.username.text(),
                'password': self.password.text()}

    @staticmethod
    def get_result(parent=None):
        dialog = AddUserDialog(parent)
        result = dialog.exec_()
        user = dialog.get_values()
        return result, user
