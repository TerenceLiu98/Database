import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import hashlib


class AddGroupWidget(QDialog):
    Group_AddGroup_success_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        self.resize(300, 400)
        self.setWindowTitle("OPAC")
        self.AddGroupLabel = QLabel("Add Group")
        self.AddGroupLabel.setAlignment(Qt.AlignCenter)
        # self.AddGroupLabel.setFixedWidth(300)
        self.AddGroupLabel.setFixedHeight(100)
        font = QFont()
        font.setPixelSize(36)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.AddGroupLabel.setFont(font)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.AddGroupLabel, Qt.AlignHCenter)
        self.setLayout(self.layout)
        # 表单，包括学号，姓名，密码，确认密码
        self.formlayout = QFormLayout()
        font.setPixelSize(15)
        # Row1
        self.GroupIdLabel = QLabel("Group ID: ")
        self.GroupIdLabel.setFont(font)
        self.GroupIdLineEdit = QLineEdit()
        self.GroupIdLineEdit.setFixedWidth(180)
        self.GroupIdLineEdit.setFixedHeight(32)
        self.GroupIdLineEdit.setFont(lineEditFont)
        self.GroupIdLineEdit.setMaxLength(100)
        self.formlayout.addRow(self.GroupIdLabel, self.GroupIdLineEdit)

        # Row2
        self.GroupNameLabel = QLabel("Group Name: ")
        self.GroupNameLabel.setFont(font)
        self.GroupNameLineEdit = QLineEdit()
        self.GroupNameLineEdit.setFixedHeight(32)
        self.GroupNameLineEdit.setFixedWidth(180)
        self.GroupNameLineEdit.setFont(lineEditFont)
        self.GroupNameLineEdit.setMaxLength(100)
        self.formlayout.addRow(self.GroupNameLabel, self.GroupNameLineEdit)

        lineEditFont.setPixelSize(10)

        #Row 3
        self.GroupSizeLabel = QLabel("Group Size: ")
        self.GroupSizeLabel.setFont(font)
        self.GroupSizeLineEdit = QLineEdit()
        self.GroupSizeLineEdit.setFixedHeight(32)
        self.GroupSizeLineEdit.setFixedWidth(180)
        self.GroupSizeLineEdit.setFont(lineEditFont)
        self.GroupSizeLineEdit.setMaxLength(100)
        self.formlayout.addRow(self.GroupSizeLabel, self.GroupSizeLineEdit)

        lineEditFont.setPixelSize(10)

        # Row4
        self.AddGroupButton = QPushButton("Add!")
        self.AddGroupButton.setFixedWidth(120)
        self.AddGroupButton.setFixedHeight(30)
        self.AddGroupButton.setFont(font)
        self.formlayout.addRow("", self.AddGroupButton)
        widget = QWidget()
        widget.setLayout(self.formlayout)
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(self.Hlayout)
        self.layout.addWidget(widget, Qt.AlignHCenter)

        self.AddGroupButton.clicked.connect(self.AddGroupButtonClicked)

    def AddGroupButtonClicked(self):
        GroupId = self.GroupIdLineEdit.text()
        GroupName = self.GroupNameLineEdit.text()
        GroupSize = self.GroupSizeLineEdit.text()
        if (GroupId == "" or GroupName == "" or GroupSize == ""):
            print(QMessageBox.warning(self, "No blank is allowed", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName('./db/LibraryManagement.db')
            db.open()
            query = QSqlQuery()
            sql = "SELECT COUNT(GroupId) FROM InterestGroup WHERE  GroupId='%s' OR GroupName='%s'" % (
            GroupId, GroupName)
            query.exec_(sql)
            if (query.next() and query.value(0)):
                QMessageBox.warning(self, "Alert","Group exists", QMessageBox.Yes, QMessageBox.Yes)
                return
            sql = "INSERT INTO InterestGroup VALUES ('%s','%s','%s')" % (
                GroupName, GroupId, GroupSize)
            db.exec_(sql)
            db.commit()
            db.rollback()
            sql = "SELECT * FROM InterestGroup ORDER BY GroupId ASC"
            db.exec_(sql)
            db.commit()
            print(QMessageBox.information(self, "Yes", "Add seccuessfully!", QMessageBox.Yes, QMessageBox.Yes))
            self.Group_AddGroup_success_signal.emit()
            db.close()
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = AddGroupWidget()
    mainMindow.show()
    sys.exit(app.exec_())
