import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip
from User_adduser import addUserDialog

class UserManage(QDialog):
    def __init__(self,parent=None):
        super(UserManage, self).__init__(parent)
        self.resize(700, 400)#窗体大小
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("管理用户")
        # 用户数
        self.userCount = 0
        self.oldDeleteId = ""
        self.oldDeleteName = ""
        self.deleteId = ""
        self.deleteName = ""
        self.setUpUI()

    def setUpUI(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.query = QSqlQuery()
        self.getResult()


        # 下面的和updateUI一样了，复制过去就行
        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(5)#table列数
        self.tableWidget.setHorizontalHeaderLabels(['账号', '姓名','性别','科室','借阅书籍本数'])

        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()#在table里面放数据

        self.addUserButton = QPushButton("添 加 用 户")
        # self.reviseUserButton = QPushButton("修 改 用 户")
        self.deleteUserButton = QPushButton("删 除 用 户")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.addUserButton, Qt.AlignHCenter)
        # hlayout.addWidget(self.reviseUserButton, Qt.AlignHCenter)
        hlayout.addWidget(self.deleteUserButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)

        font = QFont()
        font.setPixelSize(15)
        self.addUserButton.setFixedHeight(36)
        self.addUserButton.setFixedWidth(180)
        self.addUserButton.setFont(font)
        # self.reviseUserButton.setFixedHeight(36)
        # self.reviseUserButton.setFixedWidth(180)
        # self.reviseUserButton.setFont(font)
        self.deleteUserButton.setFixedHeight(36)
        self.deleteUserButton.setFixedWidth(180)
        self.deleteUserButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

        # 设置信号
        self.addUserButton.clicked.connect(self.addUser)
        self.deleteUserButton.clicked.connect(self.deleteUser)#删除用户信号
        self.tableWidget.itemClicked.connect(self.getStudentInfo)
        # self.reviseUserButton.clicked.connect(self.updateUI)

    def getResult(self):
        sql = "SELECT StudentId,Name,sex,keshi,Numborrowed FROM User WHERE IsAdmin=0 order by keshi, studentid"
        self.query.exec_(sql)
        self.userCount = 0;
        while (self.query.next()):
            self.userCount += 1;
        sql = "SELECT StudentId,Name,sex,keshi,Numborrowed FROM User WHERE IsAdmin=0 order by keshi, studentid"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.userCount):
            if (self.query.next()):
                #读取数据
                StudentIdItem = QTableWidgetItem(self.query.value(0))
                StudentNameItem = QTableWidgetItem(self.query.value(1))
                StudentSexItem = QTableWidgetItem(self.query.value(2))
                StudentKeshiItem = QTableWidgetItem(self.query.value(3))
                StudentNumBorrowedItem=QTableWidgetItem(str(self.query.value(4)))
                # print(self.query.value(4))

                #设置字体
                StudentIdItem.setFont(font)
                StudentNameItem.setFont(font)
                StudentSexItem.setFont(font)
                StudentKeshiItem.setFont(font)
                StudentNumBorrowedItem.setFont(font)

                #文字居中显示
                StudentIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentSexItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentKeshiItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                StudentNumBorrowedItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                #绑定到窗体
                self.tableWidget.setItem(i, 0, StudentIdItem)
                self.tableWidget.setItem(i, 1, StudentNameItem)
                self.tableWidget.setItem(i, 2, StudentSexItem)
                self.tableWidget.setItem(i, 3, StudentKeshiItem)
                self.tableWidget.setItem(i, 4, StudentNumBorrowedItem)
        return

    def getStudentInfo(self, item):
        row = self.tableWidget.currentIndex().row()
        self.tableWidget.verticalScrollBar().setSliderPosition(row)
        self.getResult()
        i = 0
        while (self.query.next() and i != row):
            i = i + 1
        self.oldDeleteId = self.deleteId
        self.oldDeleteName = self.deleteName
        self.deleteId = self.query.value(0)
        self.deleteName = self.query.value(1)

    def deleteUser(self):
        if (self.deleteId == "" and self.deleteName == ""):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif (self.deleteId == self.oldDeleteId and self.deleteName == self.oldDeleteName):
            print(QMessageBox.warning(self, "警告", "请选中要删除的用户", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "提醒", "删除用户:%s,%s\n用户一经删除将无法恢复，是否继续?" % (self.deleteId, self.deleteName),
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.No):
            return
        # 从User表删除用户
        sql = "DELETE FROM User WHERE StudentId='%s'" % (self.deleteId)
        # print(sql)
        self.query.exec_(sql)
        self.db.commit()



        # 归还所有书籍
        # 把所有的书籍变成可以借阅:isborrowed=0
        sql = "update book set isborrowed=0 where bookid in (SELECT BookId FROM User_Book where returnTime is null AND StudentId= '%s')" % self.deleteId
        self.query.exec_(sql)

        sql = "SELECT * FROM User_Book  WHERE StudentId='%s' AND BorrowState=1 order by keshi, name" % self.deleteId
        self.query.exec_(sql)
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # updateQuery=QSqlQuery()#老版本，增加书使用
        # while (self.query.next()):
        #     bookId=self.query.value(1)
        #     sql="UPDATE Book SET NumCanBorrow=NumCanBorrow+1 WHERE BookId='%s'"% bookId
        #     updateQuery.exec_(sql)
        #     self.db.commit()
        sql="UPDATE User_Book SET ReturnTime='%s',BorrowState=0 WHERE StudentId='%s' AND BorrowState=1"%(timenow,self.deleteId)
        print(sql)
        self.query.exec_(sql)

        self.db.commit()
        print(QMessageBox.information(self,"提醒","删除用户成功!",QMessageBox.Yes,QMessageBox.Yes))
        self.updateUI()#删除完成以后更新UI
        return
    def addUser(self):
        add_User1=addUserDialog(self)
        # add_User1.add_user_success_signal.connect(self.updateUI)  # 删除完成以后更新UI
        add_User1.show()
        add_User1.exec_()

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName('./db/LibraryManagement.db')
        self.db.open()
        self.query = QSqlQuery()
        self.db.open()
        self.updateUI()
        # print("执行完毕")
        return

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)
        sip.delete(self.widget)
        sip.delete(self.tableWidget)

        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.userCount)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(['账号', '姓名', '性别', '科室','借阅书籍本数'])

        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()

        self.addUserButton = QPushButton("添 加 用 户")
        # self.reviseUserButton = QPushButton("修 改 用 户")
        self.deleteUserButton = QPushButton("删 除 用 户")

        hlayout = QHBoxLayout()
        hlayout.addWidget(self.addUserButton, Qt.AlignHCenter)
        # hlayout.addWidget(self.reviseUserButton, Qt.AlignHCenter)
        hlayout.addWidget(self.deleteUserButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)

        font = QFont()
        font.setPixelSize(15)
        self.addUserButton.setFixedHeight(36)
        self.addUserButton.setFixedWidth(180)
        self.addUserButton.setFont(font)
        # self.reviseUserButton.setFixedHeight(36)
        # self.reviseUserButton.setFixedWidth(180)
        # self.reviseUserButton.setFont(font)
        self.deleteUserButton.setFixedHeight(36)
        self.deleteUserButton.setFixedWidth(180)
        self.deleteUserButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)

        # 设置信号
        self.addUserButton.clicked.connect(self.addUser)
        self.deleteUserButton.clicked.connect(self.deleteUser)  # 删除用户信号
        self.tableWidget.itemClicked.connect(self.getStudentInfo)
        # self.tableWidget.doubleClicked.connect(self.updateUI)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = UserManage()
    mainMindow.show()
    sys.exit(app.exec_())
