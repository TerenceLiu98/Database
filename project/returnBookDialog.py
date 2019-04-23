import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class returnBookDialog(QDialog):
    return_book_success_signal=pyqtSignal()
    def __init__(self,parent=None):#这里给入的是还书人的ID，然后还书，感觉并不科学。应该是给书号，然后去匹配还书人是谁
        super(returnBookDialog, self).__init__(parent)
        self.studentId =""#在还书的时候会用到这个
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("归还书籍")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        BookCategory = ["哲学", "社会科学", "政治", "法律", "军事", "经济", "文化", "教育", "体育", "语言文字", "艺术", "历史"
            , "地理", "天文学", "生物学", "医学卫生", "农业"]
        self.resize(300, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.returnStudentLabel = QLabel("还 书 人:")
        # self.returnStudentIdLabel = QLabel(self.studentId)
        self.titlelabel = QLabel("  归还书籍")
        self.bookNameLabel = QLabel("书    名:")
        self.bookIdLabel = QLabel("书    号:")
        self.authNameLabel = QLabel("作    者:")
        self.categoryLabel = QLabel("分    类:")
        self.publisherLabel = QLabel("出 版 社:")
        self.publishDateLabel = QLabel("出版日期:")

        # button控件
        self.returnBookButton = QPushButton("确认归还")

        # lineEdit控件
        self.returnStudentNameEdit=QLineEdit()#还书人名字
        self.bookNameEdit = QLineEdit()
        self.bookIdEdit = QLineEdit()
        self.authNameEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(BookCategory)
        self.publisherEdit = QLineEdit()
        self.publishTime = QLineEdit()

        self.bookNameEdit.setMaxLength(10)
        self.bookIdEdit.setMaxLength(20)
        self.authNameEdit.setMaxLength(10)
        self.publisherEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.returnStudentLabel, self.returnStudentNameEdit)#还书人名字，会有重复名字，但是id其实不用管了
        self.layout.addRow(self.bookNameLabel, self.bookNameEdit)
        self.layout.addRow(self.bookIdLabel, self.bookIdEdit)
        self.layout.addRow(self.authNameLabel, self.authNameEdit)
        self.layout.addRow(self.categoryLabel, self.categoryComboBox)
        self.layout.addRow(self.publisherLabel, self.publisherEdit)
        self.layout.addRow(self.publishDateLabel, self.publishTime)
        self.layout.addRow("", self.returnBookButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        # self.returnStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.returnStudentLabel.setFont(font)
        self.bookNameLabel.setFont(font)
        self.bookIdLabel.setFont(font)
        self.authNameLabel.setFont(font)
        self.categoryLabel.setFont(font)
        self.publisherLabel.setFont(font)
        self.publishDateLabel.setFont(font)

        #字体设置：文本框部分
        self. returnStudentNameEdit.setFont(font)#还书人名字
        self. returnStudentNameEdit.setReadOnly(True)
        self.returnStudentNameEdit.setStyleSheet("background-color:#363636")
        self.bookNameEdit.setFont(font)
        self.bookNameEdit.setReadOnly(True)
        self.bookNameEdit.setStyleSheet("background-color:#363636")
        self.bookIdEdit.setFont(font)
        self.authNameEdit.setFont(font)
        self.authNameEdit.setReadOnly(True)
        self.authNameEdit.setStyleSheet("background-color:#363636")
        self.publisherEdit.setFont(font)
        self.publisherEdit.setReadOnly(True)
        self.publisherEdit.setStyleSheet("background-color:#363636")
        self.publishTime.setFont(font)
        self.publishTime.setStyleSheet("background-color:#363636")
        self.categoryComboBox.setFont(font)
        self.categoryComboBox.setStyleSheet("background-color:#363636")

        # button设置
        font.setPixelSize(16)
        self.returnBookButton.setFont(font)
        self.returnBookButton.setFixedHeight(32)
        self.returnBookButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)
        self.returnBookButton.clicked.connect(self.returnButtonClicked)
        self.bookIdEdit.textChanged.connect(self.bookIdEditChanged)

    def returnButtonClicked(self):
        # 获取书号，书号为空或并未借阅，则弹出错误
        # 更新Book_User表User表以及Book表
        BookId = self.bookIdEdit.text()
        # studentID=self.studentID
        # BookId为空的处理
        if (BookId == ""):
            print(QMessageBox.warning(self, "警告", "你所要还的书不存在，请查看输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库
        db = db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()

        # 如果未借阅
        sql = "SELECT * FROM User_Book WHERE StudentId='%s' AND BookId='%s' AND BorrowState=1" %(self.studentId,BookId)
        query.exec_(sql)
        if (not query.next()):
            print(QMessageBox.information(self, "提示", "此书并未借阅，故无需归还", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 更新User表
        sql = "UPDATE User SET NumBorrowed=NumBorrowed-1 WHERE StudentId='%s'" % self.studentId
        # print(sql)
        query.exec_(sql)
        db.commit()

        # 更新Book表:变成可借
        sql = "UPDATE Book SET isBorrowed=0 WHERE BookId='%s'" % BookId
        # print(sql)
        query.exec_(sql)
        db.commit()

        # 更新User_Book表：给一个还书时间+改一个状态
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "UPDATE User_Book SET ReturnTime='%s',BorrowState=0 WHERE StudentId='%s' AND BookId='%s' AND BorrowState=1" % (timenow,self.studentId,BookId)
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "提示", "归还成功!", QMessageBox.Yes, QMessageBox.Yes))
        self.return_book_success_signal.emit()
        self.close()
        return

    def bookIdEditChanged(self):
        bookId = self.bookIdEdit.text()
        if (bookId == ""):
            self.returnStudentNameEdit.clear()
            self.bookNameEdit.clear()
            self.authNameEdit.clear()
            self.publisherEdit.clear()
            self.publishTime.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        # 在User_Book表中找借阅记录，如果存在借阅，则更新form内容
        sql = "SELECT * FROM User_Book WHERE BookId='%s' AND BorrowState=1" % (
            bookId)#找到书籍的借阅信息
        #print(sql)
        query.exec_(sql)
        if (query.next()):#如果是借阅信息存在
            # 更新form内容
            # sql = "SELECT * FROM Book WHERE BookId='%s'" % (bookId)
            sql="select User_Book.StudentId,Book.*,User.Name from User_Book left join User on User.StudentId=User_Book.StudentId left join Book on User_Book.BookId=Book.BookId where User_Book.BookId='%s' AND User_Book.ReturnTime is null" % (bookId)
            # print(sql)
            query.exec_(sql)
            # 查询对应书号，如果存在就更新form
            if (query.next()):
                # print(query.value())
                self.studentId=query.value(0)#studentID号，更新的时候用得到。
                self.returnStudentNameEdit.setText(query.value(10))
                self.bookNameEdit.setText(query.value(1))
                self.authNameEdit.setText(query.value(4))
                self.categoryComboBox.setCurrentText(query.value(5))
                self.publisherEdit.setText(query.value(6))
                self.publishTime.setText(query.value(7))
        return

#IS1027
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = returnBookDialog()#"PB15000135"
    mainMindow.show()
    sys.exit(app.exec_())
