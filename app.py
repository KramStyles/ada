import sys, sqlite3  # To bring in the operating system
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow  # To introduce the Qapplication and QDialog
from PyQt5.uic import loadUi  # is used to run the UI designed
from datetime import datetime

from functions import *

DB = sqlite3.connect('database.sql', check_same_thread=False)
cursor = DB.cursor()


class User(QMainWindow):
    def __init__(self):
        try:
            super(User, self).__init__()
            loadUi('ui/student.ui', self)

            self.show()
        except Exception as err:
            print(err)

class Login(QDialog):  # Login inherits every form element from the QDialog import
    def __init__(self):  # A function that runs immediately the code is ran
        super(Login, self).__init__()
        loadUi('ui/login.ui', self)

        self.w = None
        self.buttonHandle()
        self.setWindowTitle('My new window title')
        self.show()

    def buttonHandle(self):
        self.btnShowPass.clicked.connect(self.showPassword)
        self.btnRegister.clicked.connect(self.register)
        self.btnLogin.clicked.connect(self.login)

    def showPassword(self):
        if self.txtPassword.echoMode() == 0:
            self.txtPassword.setEchoMode(2)
        else:
            self.txtPassword.setEchoMode(0)

    def showUser(self):
        self.w = User()
        self.w.show()
        self.hide()

    def register(self):
        # from PyQt5.QtWidgets import QComboBox
        # h = QComboBox()
        # h.item
        try:
            fullname = self.txtFullname.text()
            username = self.txtUser.text()
            passwd = self.txtPassword.text()
            confirm = self.txtConfirm.text()
            email = self.txtEmail.text()
            usertype = self.cmbUserType.currentText()
            noww = datetime.now()

            if not fullname or not username or not passwd or not email:
                msg = "You need to fill all the fields"
            elif len(passwd) < 5:
                msg = "Your password is too short"
            elif passwd != confirm:
                msg = "Password Mismatch"
            else:
                passwd = Sun.encrypt(passwd)
                sql = f"""INSERT INTO users (fullname, username, password, email, usertype, regdate) 
                VALUES ('{fullname}','{username}', "{passwd}", '{email}', '{usertype}', '{noww}')"""
                cursor.execute(sql)
                DB.commit()
                msg = "You have registered"
                self.lblMsg.setStyleSheet('color: green')
        except Exception as err:
            msg = str(err)
            self.lblMsg.setStyleSheet("color: red")

        self.lblMsg.setText(msg)

    def login(self):
        username = self.txtLoginUser.text()
        passwd = self.txtLoginPass.text()
        sql = f"""SELECT password from users WHERE username = '{username}'"""
        result = cursor.execute(sql).fetchone()

        try:
            if not username or not passwd:
                msg = "No empty fields allowed!"
            elif not result:
                msg = "Invalid Password"
            else:
                if Sun.verify(passwd, result[0]):
                    # msg = "You are logged in"
                    print('logged')
                    self.showUser()
                    print('after logged')
                else:
                    msg = "Your password is incorrect"
        except Exception as err:
            print(err)
            msg = str(err)

        self.lblLoginMsg.setText(msg)


def closeApp():
    sys.exit()


app = QApplication(sys.argv)
win = Login()  # First form to run
sys.exit(app.exec_())  # Prevents the app from closing after we run the python script
