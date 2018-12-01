from sys import argv, exit

from PySide2.QtWidgets import QApplication, QDialog

class window (QDialog):
    def __init__(self):
        super().__init__() #UI Instantiation
        self.show()

if __name__ == '__main__':
    app = QApplication(argv)
    w = window()
    exit(app.exec_())
