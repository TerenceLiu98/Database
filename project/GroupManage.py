import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
from PyQt5.QtSql import *
import time
import sip

class GroupManage(QDialog):
    def __init__(self,parent=None):
        super(GroupManage, self).__init__(parent)
        self.resize(400, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setWindowTitle("Group Management")
        # 用户数
        self.GroupCount = 0
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

        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.GroupCount)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Group Name', 'Group Id',"GroupSize"])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.deleteGroupButton = QPushButton("Remove Group")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.deleteGroupButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)
        font = QFont()
        font.setPixelSize(15)
        self.deleteGroupButton.setFixedHeight(36)
        self.deleteGroupButton.setFixedWidth(180)
        self.deleteGroupButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.deleteGroupButton.clicked.connect(self.deleteGroup)
        self.tableWidget.itemClicked.connect(self.getGroupInfo)

    def getResult(self):
        sql = "SELECT GroupName, GroupId, GroupSize FROM InterestGroup"
        self.query.exec_(sql)
        self.GroupCount = 0;
        while (self.query.next()):
            self.GroupCount += 1;
        sql = "SELECT GroupName, GroupId, GroupSize FROM InterestGroup"
        self.query.exec_(sql)

    def setRows(self):
        font = QFont()
        font.setPixelSize(14)
        for i in range(self.GroupCount):
            if (self.query.next()):
                GroupNameItem = QTableWidgetItem(self.query.value(0))
                GroupIdItem = QTableWidgetItem(self.query.value(1))
                GroupSizeItem = QTableWidgetItem(self.query.value(2))
                GroupIdItem.setFont(font)
                GroupNameItem.setFont(font)
                GroupSizeItem.setFont(font)
                GroupIdItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                GroupNameItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                GroupSizeItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, 0, GroupNameItem)
                self.tableWidget.setItem(i, 1, GroupIdItem)
                self.tableWidget.setItem(i, 2, GroupSizeItem)

        return

    def getGroupInfo(self, item):
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

    def deleteGroup(self):
        if (self.deleteId == "" and self.deleteName == ""):
            print(QMessageBox.warning(self, "ALERT!","Choose the Group you want to remove", QMessageBox.Yes, QMessageBox.Yes))
            return
        elif (self.deleteId == self.oldDeleteId and self.deleteName == self.oldDeleteName):
            print(QMessageBox.warning(self, "ALERT!","Choose the Group you want to remove", QMessageBox.Yes, QMessageBox.Yes))
            return
        if (QMessageBox.information(self, "ALERT!", "Rmoving:%s,%s\n Group's operation can not be undo, continue?" % (self.deleteId, self.deleteName),
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No) == QMessageBox.No):
            return
        # 从 User_Group表删除用户
        sql = "DELETE FROM InterestGroup WHERE GroupId='%s'" % (self.deleteName)
        self.query.exec_(sql)
        self.db.commit()
        print(QMessageBox.information(self,"Yes","Success",QMessageBox.Yes,QMessageBox.Yes))
        self.updateUI()
        return

    def updateUI(self):
        self.getResult()
        self.layout.removeWidget(self.widget)
        self.layout.removeWidget(self.tableWidget)
        sip.delete(self.widget)
        sip.delete(self.tableWidget)
        # 表格设置
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.GroupCount)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Group Name', 'Group ID', 'Group Size'])
        # 不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 标题可拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 整行选中
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.tableWidget)
        self.setRows()
        self.deleteGroupButton = QPushButton("Remove Group")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.deleteGroupButton, Qt.AlignHCenter)
        self.widget = QWidget()
        self.widget.setLayout(hlayout)
        self.widget.setFixedHeight(48)
        font = QFont()
        font.setPixelSize(15)
        self.deleteGroupButton.setFixedHeight(36)
        self.deleteGroupButton.setFixedWidth(180)
        self.deleteGroupButton.setFont(font)
        self.layout.addWidget(self.widget, Qt.AlignCenter)
        # 设置信号
        self.deleteGroupButton.clicked.connect(self.deleteGroup)
        self.tableWidget.itemClicked.connect(self.getGroupInfo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = GroupManage()
    mainMindow.show()
    sys.exit(app.exec_())
