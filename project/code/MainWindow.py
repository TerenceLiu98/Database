#  _*_ coding: utf-8 _*_
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import qdarkstyle
from SignIn import SignInWidget
from SignUp import SignUpWidget
import sip
from AdminHome import AdminHome
from StudentHome import StudentHome
from changePasswordDialog import changePasswordDialog
from AddGroup import AddGroupWidget

class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()
        self.resize(900, 600)
        self.setWindowTitle("Online Public Access Catalogue")
        self.setCentralWidget(self.widget)
        bar = self.menuBar()
        self.Menu = bar.addMenu("Menu")
        self.signUpAction = QAction("Sign Up", self)
        self.GroupAction = QAction("Add Group", self)
        self.changePasswordAction =QAction("Change Password",self)
        self.signInAction = QAction("Sign In", self)
        self.quitSignInAction = QAction("Sign Out", self)
        self.quitAction = QAction("Exit", self)
        self.Menu.addAction(self.signUpAction)
        self.Menu.addAction(self.GroupAction)
        self.Menu.addAction(self.changePasswordAction)
        self.Menu.addAction(self.signInAction)
        self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        self.signUpAction.setEnabled(True)
        self.GroupAction.setEnabled(True)
        self.changePasswordAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)
        self.widget.is_admin_signal.connect(self.adminSignIn)
        self.widget.is_student_signal[str].connect(self.studentSignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)

    def adminSignIn(self):
        sip.delete(self.widget)
        self.widget = AdminHome()
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.GroupAction.setEnabled(True)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)

    def studentSignIn(self, studentId):
        sip.delete(self.widget)
        self.widget = StudentHome(studentId)
        self.setCentralWidget(self.widget)
        self.changePasswordAction.setEnabled(False)
        self.signUpAction.setEnabled(True)
        self.GroupAction.setEnabled(False)
        self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)

    def menuTriggered(self, q):
        if(q.text()=="Change Password"):
            changePsdDialog=changePasswordDialog(self)
            changePsdDialog.show()
            changePsdDialog.exec_()
        if (q.text() == "Sign Up"):
            sip.delete(self.widget)
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.widget.student_signup_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "Add Group"):
            sip.delete(self.widget)
            self.widget = AddGroupWidget()
            self.setCentralWidget(self.widget)
            self.widget.Group_AddGroup_success_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "Sign Out"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "Sign In"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "Exit"):
            qApp = QApplication.instance()
            qApp.quit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainMindow = Main()
    mainMindow.show()
    sys.exit(app.exec_())
