## Interface of the Library Management System

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from BookStorageViewer import BookStorageViewer
from UserManage import UserManage

from borrowBookDialog import borrowBookDialog
from returnBookDialog import returnBookDialog

class AdminHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(900, 600) # interface size
        self.setWindowTitle("Library Management System")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont() # interface font
        font.setPixelSize(16)
        self.userManageButton = QPushButton("User Management")
        self.addBookButton = QPushButton("Add Collection")
        self.dropBookButton = QPushButton("Delete Collection")
        self.borrowBookButton = QPushButton("Borrow Book")
        self.returnBookButton = QPushButton("Return Book")

        self.userManageButton.setFont(font)
        self.addBookButton.setFont(font)
        self.dropBookButton.setFont(font)
        self.borrowBookButton.setFont(font)
        self.returnBookButton.setFont(font)

        self.userManageButton.setFixedWidth(200)
        self.userManageButton.setFixedHeight(42)
        self.addBookButton.setFixedWidth(200)
        self.addBookButton.setFixedHeight(42)
        self.dropBookButton.setFixedWidth(200)
        self.dropBookButton.setFixedHeight(42)
        self.borrowBookButton.setFixedWidth(200)
        self.borrowBookButton.setFixedHeight(42)
        self.returnBookButton.setFixedWidth(200)
        self.returnBookButton.setFixedHeight(42)

        self.buttonlayout.addWidget(self.addBookButton)
        self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.userManageButton)
        self.buttonlayout.addWidget(self.borrowBookButton)
        self.buttonlayout.addWidget(self.returnBookButton)

        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.userManageButton.clicked.connect(self.userManage)
        self.borrowBookButton.clicked.connect(self.borrowBook)
        self.returnBookButton.clicked.connect(self.returnBook)

    def addBookButtonClicked(self):
        addDialog = addBookDialog(self)
        addDialog.add_book_success_signal.connect(self.storageView.searchButtonClicked)
        addDialog.show()
        addDialog.exec_()

    def dropBookButtonClicked(self):
        dropDialog = dropBookDialog(self)
        dropDialog.drop_book_successful_signal.connect(self.storageView.searchButtonClicked)
        dropDialog.show()
        dropDialog.exec_()

    def userManage(self):
        UserDelete=UserManage(self)
        UserDelete.show()
        UserDelete.exec_()
    def borrowBook(self):
        borrow_book=borrowBookDialog()
        borrow_book.borrow_book_success_signal.connect(self.storageView.searchButtonClicked)
        borrow_book.show()
        borrow_book.exec_()
    def returnBook(self):
        return_book=returnBookDialog()
        return_book.return_book_success_signal.connect(self.storageView.searchButtonClicked)
        return_book.show()
        return_book.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/library.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = AdminHome()
    mainMindow.show()
    sys.exit(app.exec_())
