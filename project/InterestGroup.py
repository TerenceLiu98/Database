import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *


class InterestGroup(QDialog):
    group_success_signal=pyqtSignal()

    def __init__(self, StudentId, parent=None):
        super(InterestGroup, self).__init__(parent)
        self.studentId = StudentId
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("Interest Group Application")

    def setUpUI(self):
        # 书名，书号，作者，分类，添加数量.出版社,出版日期
        # 书籍分类：哲学类、社会科学类、政治类、法律类、军事类、经济类、文化类、教育类、体育类、语言文字类、艺术类、历史类、地理类、天文学类、生物学类、医学卫生类、农业类
        GroupCategory = ["Philosophy", "Social Science", "Politics", "Legislation", "Military", "Economics", "Culture", "Education",
"Linguistics", "Art", "History", "geography", "Astronomy"]
        self.resize(600, 400)
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("Interest Group Application")
        self.applyStudentLabel = QLabel("Applicant:")
        self.applyStudentIdLabel = QLabel(self.studentId)
        self.GroupNameLabel = QLabel("Group Name:")
        self.GroupIdLabel = QLabel("Group ID:")
        self.GroupSizeLabel = QLabel("Group Size:")

        # Button控件
        self.InterestGroupButton = QPushButton("Apply!")

        # lineEdit控件
        self.GroupNameEdit = QLineEdit()
        self.GroupIdEdit = QLineEdit()
        self.GroupSizeEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(GroupCategory)
        self.GroupSizeEdit = QLineEdit()

        self.GroupNameEdit.setMaxLength(10)
        self.GroupIdEdit.setMaxLength(10)

        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.applyStudentLabel, self.applyStudentIdLabel)
        self.layout.addRow(self.GroupNameLabel, self.GroupNameEdit)
        self.layout.addRow(self.GroupIdLabel, self.GroupIdEdit)
        self.layout.addRow(self.GroupSizeLabel, self.GroupSizeEdit)
        self.layout.addRow("", self.InterestGroupButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(16)
        self.applyStudentIdLabel.setFont(font)
        font.setPixelSize(14)
        self.applyStudentLabel.setFont(font)
        self.GroupNameLabel.setFont(font)
        self.GroupIdLabel.setFont(font)

        self.GroupNameEdit.setFont(font)
        self.GroupNameEdit.setReadOnly(True)
        self.GroupNameEdit.setStyleSheet("background-color:#363636")
        self.GroupIdEdit.setFont(font)
        self.GroupSizeEdit.setReadOnly(True)
        self.GroupSizeEdit.setFont(font)
        self.GroupSizeEdit.setStyleSheet("background-color:#363636")

        # Button设置
        font.setPixelSize(16)
        self.InterestGroupButton.setFont(font)
        self.InterestGroupButton.setFixedHeight(32)
        self.InterestGroupButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.InterestGroupButton.clicked.connect(self.InterestGroupButtonclicked)
        self.GroupIdEdit.textChanged.connect(self.GroupIdEditChanged)
        self.GroupIdEdit.returnPressed.connect(self.InterestGroupButtonclicked)

    def InterestGroupButtonclicked(self):
        # 获取组号，组号为空或不存在库中，则弹出错误
        GroupId = self.GroupIdEdit.text()
        # GroupId 为空的处理
        if (GroupId == ""):
            print(QMessageBox.warning(self, "Group does not exist", QMessageBox.Yes, QMessageBox.Yes))
            return
        # 打开数据库
        db = db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        # 如果 GroupId 不存在
        sql = "SELECT * FROM InterestGroup WHERE GroupId='%s'" % GroupId
        query.exec_(sql)
        if (not query.next()):
            print(QMessageBox.warning(self, "Alert!", "Group does not exist", QMessageBox.Yes, QMessageBox.Yes))
            return


        # 不允许重复加入
        sql = "SELECT StudentId FROM User_Group WHERE  StudentId='%s' AND GroupId='%s' AND BorrowState=1" % (
        self.studentId, GroupId)
        query.exec_(sql)
        if (query.next() and query.value(0)):
            QMessageBox.warning(self, "Alert!", "You are in the group already", QMessageBox.Yes, QMessageBox.Yes)
            return
        # 更新 User 表
        sql = "UPDATE User SET Group_quantity=Group_quantity+1 WHERE StudentId='%s'" % self.studentId
        query.exec_(sql)
        db.commit()
        # 更新 Interest_Group 表
        sql = "UPDATE InterestGroup SET GroupSize=GroupSize+1 WHERE GroupId='%s'" % GroupId
        query.exec_(sql)
        db.commit()
        timenow = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        sql = "INSERT INTO User_Group VALUES ('%s','%s',1)" % (self.studentId, GroupId)
        print(sql)
        query.exec_(sql)
        db.commit()
        print(QMessageBox.information(self, "Yes!","Apply Seccuessful", QMessageBox.Yes, QMessageBox.Yes))
        self.group_success_signal.emit()
        self.close()
        return


    def GroupIdEditChanged(self):
        GroupId = self.GroupIdEdit.text()
        if (GroupId == ""):
            self.GroupNameEdit.clear()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName('./db/LibraryManagement.db')
        db.open()
        query = QSqlQuery()
        sql = "SELECT * FROM InterestGroup WHERE GroupId='%s'" % (GroupId)
        query.exec_(sql)
        # 查询对应书号，如果存在就更新form
        if (query.next()):
            self.GroupNameEdit.setText(query.value(0))
            self.GroupSizeEdit.setText(query.value(2))
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = InterestGroup("PB15000135")
    mainMindow.show()
    sys.exit(app.exec_())
