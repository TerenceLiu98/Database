import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from addBookDialog import addBookDialog
from dropBookDialog import dropBookDialog
from BookStorageViewer import BookStorageViewer
from UserManage import UserManage

class AdminHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(900, 600)
        self.setWindowTitle("Online Public Access Catalogue")
        self.layout = QHBoxLayout()
        self.buttonlayout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont()
        font.setPixelSize(16)
        self.userManageButton = QPushButton("User Management")
        self.addBookButton = QPushButton("Add Books")
        self.dropBookButton = QPushButton("Remove Books")
        self.userManageButton.setFont(font)
        self.addBookButton.setFont(font)
        self.dropBookButton.setFont(font)
        self.userManageButton.setFixedWidth(200)
        self.userManageButton.setFixedHeight(42)
        self.addBookButton.setFixedWidth(200)
        self.addBookButton.setFixedHeight(42)
        self.dropBookButton.setFixedWidth(200)
        self.dropBookButton.setFixedHeight(42)
        self.buttonlayout.addWidget(self.addBookButton)
        self.buttonlayout.addWidget(self.dropBookButton)
        self.buttonlayout.addWidget(self.userManageButton)
        self.layout.addLayout(self.buttonlayout)
        self.storageView = BookStorageViewer()
        self.layout.addWidget(self.storageView)

        self.addBookButton.clicked.connect(self.addBookButtonClicked)
        self.dropBookButton.clicked.connect(self.dropBookButtonClicked)
        self.userManageButton.clicked.connect(self.userManage)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = AdminHome()
    mainMindow.show()
    sys.exit(app.exec_())
