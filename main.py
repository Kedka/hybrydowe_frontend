import sys
from PyQt5.QtWidgets import QApplication
from GUI import LibraryApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
