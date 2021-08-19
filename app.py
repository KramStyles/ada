from functions import password
import sys, sqlite3, secrets  # To bring in the operating system
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QMainWindow, QWidget, QMessageBox, QInputDialog  # To introduce the Qapplication and QDialog
from PyQt5.uic import loadUi  # is used to run the UI designed
from PyQt5.QtCore import QTimer
from datetime import datetime

from functions import *
from requests import request, ConnectionError, Timeout

DB = sqlite3.connect('database.sql', check_same_thread=False)
cursor = DB.cursor()

USERNAME = ''


class studentEdit(QWidget):
    def __init__(self):
        super(studentEdit, self).__init__()
        loadUi('ui/studentEditProfile.ui', self)

        self.value = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.progressbar)

        self.buttonHandle()
        # self.show()

    def buttonHandle(self):
        self.showInfo()
        self.btnUpdate.clicked.connect(self.updateProfile)

    def progressbar(self):
        self.value = self.value + 5
        if self.value <= 100:
            self.progBar.setValue(self.value)
            self.lblMsg.setText('Updating...')
        else:
            self.timer.stop()
            self.lblMsg.setText('')
            self.progBar.setValue(0)
            self.value = 0
            self.close()

    def showInfo(self):
        sql = f"""SELECT * FROM users WHERE username = '{self.username}'"""
        result = cursor.execute(sql).fetchall()[0]
        self.txtFullname.setText(result[1])
        self.txtPhone.setText(result[7])
        self.txtEmail.setText(result[4])
        self.txtReg.setText(result[8])
        self.txtFac.setText(result[9])
        self.txtDept.setText(result[10])
        self.txtUsername.setText(result[2])

    def updateProfile(self):
        Fullname = self.txtFullname.text()
        Phone = self.txtPhone.text()
        Reg = self.txtReg.text()
        Fac = self.txtFac.text()
        Dept = self.txtDept.text()
        Username = self.txtUsername.text()
        arr = [Fullname, Phone, Reg, Fac, Dept]

        if checkEmpty(arr) is True:
            msg = 'Fill all fields'
        else:
            try:
                sql = f"""UPDATE users SET fullname = '{Fullname}', regnumber = '{Reg}', faculty = '{Fac}', department = '{Dept}', phone = '{Phone}' WHERE username = '{self.username}'"""
                cursor.execute(sql)
                DB.commit()
                msg = "Details Saved"
                self.timer.start(50)
                U = User()
                U.loadInfo(User)
            except Exception as err:
                print(err)
                msg = str(err)
        self.lblMsg.setText(msg)


class User(QMainWindow):
    def __init__(self):
        try:
            super(User, self).__init__()
            loadUi('ui/student.ui', self)
            print(self.username)
            self.w = None
            self.loadInfo()
            self.buttonHandle()
            self.show()
        except Exception as err:
            print(err)

    def buttonHandle(self):
        self.actionClose.triggered.connect(closeApp)
        self.btnEdit.clicked.connect(self.editProfile)

    def editProfile(self):
        print('hello')
        studentEdit.username = self.username
        self.w = studentEdit()
        # studentEdit.show()
        self.w.show()

    def loadInfo(self):
        print('Load info working now')
        sql = f"""SELECT * FROM users WHERE username = '{self.username}'"""
        result = cursor.execute(sql).fetchall()[0]
        self.lblName.setText(result[1])
        self.lblUser.setText(result[2])
        self.nnamdi = result[2]
        self.lblEmail.setText(result[4])
        self.lblRegDate.setText(result[6])
        print(result[6])
        self.lblPhone.setText(result[7])
        self.lblReg.setText(result[8])
        self.lblFalc.setText(result[9])
        self.lblDept.setText(result[10])


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
        self.btnForgot.clicked.connect(self.changePassword)

    def changePassword(self):
        try:
            # msgBox = QMessageBox()
            # msgBox.setText('Are you sure you want to change your Password?')
            # msgBox.setWindowTitle('Confirm Password Change')
            # msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            # msgBox.setIcon(QMessageBox.Information)  # Information , Question and warning

            value = myMsgBox('Are you sure you want to change your Password?', 'confirm password change', buttons=QMessageBox.Ok | QMessageBox.Cancel)
            if value == QMessageBox.Ok:
                try:
                    request('get', 'https://google.com')
                    # username = self.txtLoginUser.text()
                    username, Dialog = QInputDialog.getText(self,'Username: ', 'Enter Username associated with the Account!')
                    
                    if not Dialog:
                        msg = "Username is needed!"
                    else:
                        sql = f"""SELECT email from users WHERE username = '{username}'"""
                        result = cursor.execute(sql).fetchone()[0]
                        if not result:
                            msg = "Username not found"
                        else:
                            new_password = secrets.token_urlsafe(10)
                            enc = password(new_password)
                            sql = f""" UPDATE users SET password = '{enc}' WHERE username = '{username}'"""
                            cursor.execute(sql)
                            DB.commit()

                            if emailSender(result, "Password Recovery", f"Your new password is: {new_password}") == 'ok':
                            
                            #I.E SEND THE GENERATED OWN TO THE MAIL, AND SEND THE ENCRYPTED ONE TO DATABASE
                                msg = f"Your new password has been sent to your email address"
                            else:
                                msg = "Something is wrong"
                    myMsgBox(msg)
                except ConnectionError as err:
                    myMsgBox("No Internet Connection", title='Check Network', icon=QMessageBox.Warning)

        except Exception as err:
            print(err)
            myMsgBox('User not found!', icon=QMessageBox.Warning)

    def showPassword(self):
        if self.txtPassword.echoMode() == 0:
            self.txtPassword.setEchoMode(2)
        else:
            self.txtPassword.setEchoMode(0)

    def showUser(self):
        self.w = User()
        self.w.show()
        self.hide()
        # pass

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
        msg = ''

        if not username or not passwd:
            msg = "No empty fields allowed!"
        elif not result:
            msg = "Invalid Password"
        else:
            # if Sun.verify(passwd, result[0]):
            try:
                if passwd and username:
                    User.username = username
                    self.showUser()

                else:
                    msg = "Your password is incorrect"
            except Exception as err:
                print('Problem dey', err)

        self.lblLoginMsg.setText(msg)


def closeApp():
    print('hello')
    sys.exit()


def myMsgBox(text, title="Message Box Information", icon=QMessageBox.Information, buttons=QMessageBox.Ok):
    msgBox = QMessageBox()
    msgBox.setText(text)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(buttons)
    msgBox.setIcon(icon)  # Information , Question and warning

    return msgBox.exec_()


app = QApplication(sys.argv)
win = Login()  # First form to run
sys.exit(app.exec_())  # Prevents the app from closing after we run the python script
