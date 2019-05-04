# -*- coding: utf-8 -*-
'''
登录窗口，然后进入查询
'''

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import qdarkstyle
from PyQt5.QtSql import *


class BookStorageViewer(QWidget):
    def __init__(self):
        super(BookStorageViewer, self).__init__()
        self.resize(700, 500)
        self.setWindowTitle("Library Management System")
        # 查询模型
        self.queryModel = None
        # 数据表
        self.tableView = None
        # 当前页
        self.currentPage = 0
        # 总页数
        self.totalPage = 0
        # 总记录数
        self.totalRecord = 0
        # 每页数据数
        self.pageRecord = 10
        self.setUpUI()

    def setUpUI(self):
        self.layout = QVBoxLayout()
        self.Hlayout1 = QHBoxLayout()
        self.Hlayout2 = QHBoxLayout()

        # Hlayout1控件的初始化
        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(50)
        font = QFont()
        font.setPixelSize(15)
        self.searchEdit.setFont(font)

        self.searchButton = QPushButton("Search")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(font)
        self.searchButton.setIcon(QIcon(QPixmap("./images/search.png")))

        self.condisionComboBox = QComboBox()
        searchCondision = ['by name', 'by bookID','by ISSN', 'by Author', 'by classification', 'by Press']
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(font)
        self.condisionComboBox.addItems(searchCondision)

        self.Hlayout1.addWidget(self.searchEdit)
        self.Hlayout1.addWidget(self.searchButton)
        self.Hlayout1.addWidget(self.condisionComboBox)

        # Hlayout2初始化
        self.jumpToLabel = QLabel("Jump to")
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(100)
        s = "/" + str(self.totalPage) + "page"
        self.pageLabel = QLabel(s)
        self.jumpToButton = QPushButton("Go!")
        self.prevButton = QPushButton("up")
        self.prevButton.setFixedWidth(40)
        self.backButton = QPushButton("down")
        self.backButton.setFixedWidth(40)

        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.jumpToLabel)
        Hlayout.addWidget(self.pageEdit)
        Hlayout.addWidget(self.pageLabel)
        Hlayout.addWidget(self.jumpToButton)
        Hlayout.addWidget(self.prevButton)
        Hlayout.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(Hlayout)
        widget.setFixedWidth(300)
        self.Hlayout2.addWidget(widget)

        # tableView
        # id, bookName, bookId, ISSN, Auther, Classification, Press
        # Press_date, reserve, reminder
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.tableView = QTableView()

        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queryModel = QSqlQueryModel()
        self.searchButtonClicked()
        self.tableView.setModel(self.queryModel)#tableView控件

        self.queryModel.setHeaderData(0, Qt.Horizontal, "BookName")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "BookId")
        self.queryModel.setHeaderData(2, Qt.Horizontal, "ISSN")
        self.queryModel.setHeaderData(3, Qt.Horizontal, "Author")
        self.queryModel.setHeaderData(4, Qt.Horizontal, "Classification")
        self.queryModel.setHeaderData(5, Qt.Horizontal, "Press")
        self.queryModel.setHeaderData(6, Qt.Horizontal, "Press_date")
        self.queryModel.setHeaderData(7, Qt.Horizontal, "Brorrowed")
        self.queryModel.setHeaderData(8, Qt.Horizontal, "Borrower's Name")#借书人名字
        self.queryModel.setHeaderData(9, Qt.Horizontal, "programme of Borrower")#借书人科室
        self.queryModel.setHeaderData(10, Qt.Horizontal, "Time")# 总借阅次数"
        self.layout.addLayout(self.Hlayout1)
        self.layout.addWidget(self.tableView)

        self.layout.addLayout(self.Hlayout2)
        self.setLayout(self.layout)
        self.searchButton.clicked.connect(self.searchButtonClicked)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchEdit.returnPressed.connect(self.searchButtonClicked)

    def setButtonStatus(self):
        if(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        if(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        if(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    # 得到记录数
    def getTotalRecordCount(self):
        self.queryModel.setQuery("select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId")#("SELECT * FROM Book")
        self.totalRecord = self.queryModel.rowCount()
        return

    # 得到总页数
    def getPageCount(self):
        self.getTotalRecordCount()#获取所有数据
        # 上取整
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        return

    # 分页记录查询
    # 'by name', 'by bookID','by ISSN', 'by Author', 'by classification', 'by Press'
    def recordQuery(self, index):
        queryCondition = ""
        conditionChoice = self.condisionComboBox.currentText()
        if (conditionChoice == "by name"):
            conditionChoice = 'BookName'
        elif (conditionChoice == "by bookID"):
            conditionChoice = 'BookId'
        elif (conditionChoice == "by ISSN"):
            conditionChoice = 'ISSN'
        elif (conditionChoice == "by Author"):
            conditionChoice = 'Auth'
        elif (conditionChoice == 'by classification'):
            conditionChoice = 'Category'
        else:
            conditionChoice = 'Publisher'

        if (self.searchEdit.text() == ""):
            queryCondition = "select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId"#"select * from Book"
            self.queryModel.setQuery(queryCondition)
            self.totalRecord = self.queryModel.rowCount()
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage))
            self.pageLabel.setText(label)
            queryCondition = ("select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId ORDER BY %s  limit %d,%d " % (conditionChoice,index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            self.setButtonStatus()
            return

        # 得到模糊查询条件
        temp = self.searchEdit.text()
        s = '%'
        for i in range(0, len(temp)):
            s = s + temp[i] + "%"
        queryCondition = ("select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId WHERE %s LIKE '%s' ORDER BY %s " % (
            conditionChoice, s,conditionChoice))
        self.queryModel.setQuery(queryCondition)
        self.totalRecord = self.queryModel.rowCount()
        # 当查询无记录时的操作
        if(self.totalRecord==0):
            print(QMessageBox.information(self,"Attention!", "No record.",QMessageBox.Yes,QMessageBox.Yes))
            queryCondition = "select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId"
            self.queryModel.setQuery(queryCondition)
            self.totalRecord = self.queryModel.rowCount()
            self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
            label = "/" + str(int(self.totalPage)) + "pages"
            self.pageLabel.setText(label)
            queryCondition = ("select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId ORDER BY %s  limit %d,%d " % (conditionChoice,index, self.pageRecord))
            self.queryModel.setQuery(queryCondition)
            self.setButtonStatus()
            return
        self.totalPage = int((self.totalRecord + self.pageRecord - 1) / self.pageRecord)
        label = "/" + str(int(self.totalPage)) + "pages"
        self.pageLabel.setText(label)
        queryCondition = ("select Book.BookName, Book.BookId, Book.ISSN, Book.Auth,Book.Category,Book.Publisher,Book.PublishTime,Book.isBorrowed,Book.location,b.Name,b.keshi, b.BorrowTime from Book left join  (select User_Book.StudentId,User_Book.BookId,User_Book.BorrowTime,User.Name,User.keshi from User_Book left join User on User.StudentId=User_Book.StudentId where User_Book.ReturnTime is null) b on Book.BookId=b.BookId WHERE %s LIKE '%s' ORDER BY %s LIMIT %d,%d " % (
            conditionChoice, s, conditionChoice,index, self.pageRecord))
        self.queryModel.setQuery(queryCondition)
        self.setButtonStatus()
        return

    # 点击查询
    def searchButtonClicked(self):
        self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        self.getPageCount()
        s = "/" + str(int(self.totalPage)) + "pages"
        self.pageLabel.setText(s)
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向前翻页
    def prevButtonClicked(self):
        self.currentPage -= 1
        if (self.currentPage <= 1):
            self.currentPage = 1
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 向后翻页
    def backButtonClicked(self):
        self.currentPage += 1
        if (self.currentPage >= int(self.totalPage)):
            self.currentPage = int(self.totalPage)
        self.pageEdit.setText(str(self.currentPage))
        index = (self.currentPage - 1) * self.pageRecord
        self.recordQuery(index)
        return

    # 点击跳转
    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        index = (self.currentPage - 1) * self.pageRecord
        self.pageEdit.setText(str(self.currentPage))
        self.recordQuery(index)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = BookStorageViewer()
    mainMindow.show()
    sys.exit(app.exec_())
