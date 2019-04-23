import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import time
from PyQt5.QtSql import *
import hashlib

class addUserDialog(QDialog):
    add_user_success_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(addUserDialog, self).__init__(parent)
        self.setUpUI()
        self.setWindowModality(Qt.WindowModal)
        self.setWindowTitle("增加借阅人")

    def setUpUI(self):
        # 借阅人姓名，性别，科室（密码自动给一个）
        sexCategory = ["男", "女"]

        self.resize(300, 350)#窗口大小
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        # Label控件
        self.titlelabel = QLabel("  添加借阅人")
        self.studentIdLabel = QLabel("借 阅 人ID:")
        self.nameLabel=QLabel("姓    名:")
        self.sexLabel = QLabel("性    别:")
        self.keshiLabel = QLabel("科    室:")


        # button控件
        self.addUserButton = QPushButton("添 加")

        # lineEdit控件
        self.studentIDEdit = QLineEdit()
        self.nameEdit=QLineEdit()
        self.sexComboBox = QComboBox()
        self.sexComboBox.addItems(sexCategory)
        # self.sexEdit = QLineEdit()
        self.keshiEdit = QLineEdit()


        self.studentIDEdit.setMaxLength(10)
        self.nameEdit.setMaxLength(20)
        self.keshiEdit.setMaxLength(20)


        # 添加进formlayout
        self.layout.addRow("", self.titlelabel)
        self.layout.addRow(self.studentIdLabel, self.studentIDEdit)
        self.layout.addRow(self.nameLabel, self.nameEdit)
        self.layout.addRow(self.sexLabel, self.sexComboBox)
        self.layout.addRow(self.keshiLabel, self.keshiEdit)

        self.layout.addRow("", self.addUserButton)

        # 设置字体
        font = QFont()
        font.setPixelSize(20)
        self.titlelabel.setFont(font)
        font.setPixelSize(14)
        self.studentIdLabel.setFont(font)
        self.nameLabel.setFont(font)
        self.sexLabel.setFont(font)
        self.keshiLabel.setFont(font)


        self.studentIDEdit.setFont(font)
        self.nameEdit.setFont(font)
        self.sexComboBox.setFont(font)
        self.keshiEdit.setFont(font)


        # button设置
        font.setPixelSize(16)
        self.addUserButton.setFont(font)
        self.addUserButton.setFixedHeight(32)
        self.addUserButton.setFixedWidth(140)

        # 设置间距
        self.titlelabel.setMargin(8)
        self.layout.setVerticalSpacing(10)

        self.addUserButton.clicked.connect(self.addUserButtonCicked)

    def addUserButtonCicked(self):
        # print("点击成功")
        # studentId="123"
        studentId = self.studentIDEdit.text()
        # print(studentId)
        studentName = self.nameEdit.text()
        password = "123456"
        confirmPassword = "123456"
        sex=self.sexComboBox.currentText()
        keshi=self.keshiEdit.text()
        # print(studentId,studentName,sex,keshi)

        if (studentId == "" or studentName == "" or password == "" or confirmPassword == "" or keshi==""):
            print(QMessageBox.warning(self, "警告", "表单不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:  # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/LibraryManagement.db')
            db.open()
            # print("成功打开数据库")
            query = QSqlQuery()
            if (confirmPassword != password):
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif (confirmPassword == password):
                # md5编码
                hl = hashlib.md5()
                hl.update(password.encode(encoding='utf-8'))
                md5password = hl.hexdigest()
                sql = "SELECT * FROM user WHERE StudentId='%s'" % (studentId)
                query.exec_(sql)
                if (query.next()):
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    sql = "INSERT INTO user VALUES ('%s','%s','%s','%s','%s',0,0)" % (
                        studentId, studentName, md5password,sex,keshi)
                    # print(sql)
                    db.exec_(sql)
                    db.commit()
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    self.add_user_success_signal.emit()
                    # print(self.add_user_success_signal)
                    # print("信号释放")
                    self.close()
                    self.clearEdit()
                    # print("到这里结束")
                db.close()
                return

    def clearEdit(self):
        # print("开始清除")
        self.studentIDEdit.clear()
        self.nameEdit.clear()
        # self.sexEdit.clear()
        self.keshiEdit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = addUserDialog()
    mainMindow.show()
    sys.exit(app.exec_())
