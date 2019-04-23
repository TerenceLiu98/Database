import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class addBookDialog(QDialog):
    add_book_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addBookDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Add Collections")

    def setUpUI(self):
        # Book Names, Book IDs, Authors, Classification, Quality, Press, Press_Date
        # Classification: "Philosophy", "Social Science", "Politics", "legislation", "Military", "Economics", "Culture", "Education",
        # "Linguistics", "Art", "History", "geography", "Astronomy",
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["Philosophy", "Social Science", "Politics", "legislation", "Military", "Economics", "Culture", "Education",
        "Linguistics", "Art", "History", "geography", "Astronomy"]
        self.resize(300,400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("Add Book")
        self.bookNameLabel = QLabel("Book Name:")
        self.bookIdLabel = QLabel("BookID:")
        self.ISSNLabel = QLabel("ISBN:")
        self.authNameLabel = QLabel("Author:")
        self.categoryLabel = QLabel("Classification:")
        self.publisherLabel = QLabel("Press:")
        self.publishDateLabel = QLabel("Press Date:")
        self.addNumLabel = QLabel("Place:")

        # button控件
        self.addBookButton = QPushButton("Add")

        # lineEdit控件
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.ISSNEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QDateTimeEdit()
        self.publishTime.setDisplayFormat("yyyy-MM-dd")
        # self.publishDateEdit = QLineEdit()
        self.addNumEdit = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(20)
        self.ISSNEdit.setMaxLength(20)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)
        self.addNumEdit.setMaxLength(50)
        # self.addNumEdit.setValidator(QIntValidator())

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.ISSNLabel, self.ISSNEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow(self.addNumLabel, self.addNumEdit)
        self.layout.addRow("", self.addBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.ISSNLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)
        self.addNumLabel.setFont(font)

        self.bookNameEdit.setFont(font)
        self.bookIdEdit.setFont(font)
        self.ISSNEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.publisherEdit.setFont(font)
        self.publishTime.setFont(font)
        self.categoryComboBox.setFont(font)
        self.addNumEdit.setFont(font)

        # button设置
        font.setPixelSize(16)
        self.addBookButton.setFont(font)
        self.addBookButton.setFixedHeight(50)
        self.addBookButton.setFixedWidth(200)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.addBookButton.clicked.connect(self.addBookButtonCicked)

    def addBookButtonCicked(self):
        bookName = self.bookNameEdit.text()
        bookId = self.bookIdEdit.text()
        ISSN=self.ISSNEdit.text()
        authName = self.authNameEdit.text()
        bookCategory = self.categoryComboBox.currentText()
        publisher = self.publisherEdit.text()
        publishTime = self.publishTime.text()
        location = self.addNumEdit.text()
        if (
                bookName == "" or bookId == "" or ISSN=="" or authName == "" or bookCategory == "" or publisher == "" or publishTime == "" or location == ""):
            print(QMessageBox.warning(self, "Warning", "Blank is not aollowed，operation Failed", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            # addBookNum = int(addBookNum)
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/LibraryManagement.db')
            db.open()
            query = QSqlQuery()
            # 如果bookID已存在:提示已经存在
            sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
            query.exec_(sql)
            if (query.next()):
                # sql = "UPDATE Book SET NumStorage=NumStorage+%d,NumCanBorrow=NumCanBorrow+%d WHERE BookId='%s'" % (
                #     addBookNum, addBookNum, bookId)
                self.isExist()
            else:#如果不存在，则update Book表，则insert Book表，同时insert buyordrop表
                sql = "INSERT INTO book VALUES ('%s','%s','%s','%s','%s','%s','%s',0,'%s')" % (
                    bookName, bookId,ISSN, authName, bookCategory, publisher, publishTime, location)
            # print(sql)
            query.exec_(sql)
            db.commit()

            # 插入droporinsert表
            timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            sql = "INSERT INTO buyordrop VALUES ('%s','%s',1)" % (bookId, timenow)
            query.exec_(sql)
            db.commit()
            print(QMessageBox.information(self, ":)", "Operation Success!", QMessageBox.Yes, QMessageBox.Yes))
            self.add_book_success_signal.emit()
            self.close()
            self.clearEdit()
        return

    def clearEdit(self):
        self.bookNameEdit.clear()
        self.bookIdEdit.clear()
        self.authNameEdit.clear()
        self.addNumEdit.clear()
        self.publisherEdit.clear()


    def isExist(self):
        QMessageBox.information(self, "Information",
                                self.tr("bookID is existed，rewrite the ID"))
        self.label.setText("Information MessageBox")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/library.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = addBookDialog()
    mainMindow.show()
    sys.exit(app.exec_())
