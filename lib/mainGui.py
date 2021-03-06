from logging import error
import os
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication,QListWidgetItem,QListWidget,QMainWindow, QMessageBox,QWidget,QPushButton
from pathlib import Path
import git
from gitRepo import gitRepo as Grepo
from git.repo.base import Repo
Project_path = Grepo.path()

class login_window(QWidget):
    def __init__(self):
        super().__init__(None)
        
        #Properties
        path = Grepo.path()/'Icons'
        showIcon = str(path/'visible.png')
        hideIcon = str(path/'hidden.png')
        iconPath = str(path/'Gicon.png')

        #self
        self.setWindowTitle('login')
        self.setGeometry(700,400,205, 150)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconPath))
        self.setWindowIcon(icon)
        
        
        #Icons
        self.showIcon,self.hideIcon = QtGui.QIcon(showIcon),QtGui.QIcon(hideIcon)
        self.toogle_icons = [self.showIcon,self.hideIcon]
        self.echoMode = [QtWidgets.QLineEdit.Password,QtWidgets.QLineEdit.Normal]
        
        #enteries
        self.User_name = QtWidgets.QLineEdit(self)
        self.User_name.setGeometry(QtCore.QRect(10, 10, 165, 25))
        self.User_name.setText("")
        self.User_name.textChanged[str].connect(self.login_approve)

        self.Password = QtWidgets.QLineEdit(self)
        self.Password.setGeometry(QtCore.QRect(10, 60, 165, 25))
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password.setText("")
        self.Password.textChanged[str].connect(self.login_approve)
        
        #labels
        self.uname_error = QtWidgets.QLabel(self)
        self.uname_error.setGeometry(QtCore.QRect(10, 38, 165, 17))
        self.uname_error.setStyleSheet('color: red')
        
        self.pass_error = QtWidgets.QLabel(self)
        self.pass_error.setGeometry(QtCore.QRect(10, 88, 165, 17))
        self.pass_error.setStyleSheet('color: red')
        
        #Buttons
        self.connect_btn = QtWidgets.QPushButton(self)
        self.connect_btn.setGeometry(QtCore.QRect(62, 110, 89, 30))
        self.connect_btn.setText( "??????????")
        self.user_approved = False
        self.pass_approved = False
        
        self.show_btn = QtWidgets.QPushButton(self)
        self.show_btn.setGeometry(QtCore.QRect(144, 60, 30, 25))
        self.show_btn.setStyleSheet("border: 0;\nbackground: transparent;")
        self.show_btn.setIcon(self.showIcon)
        self.show_btn.setCheckable(True)
        self.show_btn.clicked.connect(self.show_hide)

    def login_approve(self):
        mail_list = ['@gmail,@walla,@hotmail']
        if any(self.User_name.text() in string for string in mail_list)\
            or ('.com' not in self.User_name.text()\
            and '.co.il' not in self.User_name.text())\
            or 0 < len(self.User_name.text()) < 5:
            self.uname_error.setText("???????? ???? ????????")
            self.user_approved = False
        else:
            self.user_approved = True
            self.uname_error.setText("")
        if 0 < len(self.Password.text()) < 5:
            self.pass_error.setText("??????????: 5 ?????????? ??????????")
            self.user_approved = False
        else:
            self.pass_approved = True
            self.pass_error.setText("")

    def closeEvent(self,event):
        event.ignore()
        self.hide()
                
    def show_hide(self):
        i=0
        if self.Password.echoMode():
            i=1
        self.Password.setEchoMode(self.echoMode[i])
        self.show_btn.setIcon(self.toogle_icons[i])
 
 
        
class main_window(QWidget):
    def __init__(self,session,items,user):
        super().__init__(None)
        
        #Properties
        
        checkIcon = Grepo.path()/'Icons/check.png'
        icon = Grepo.path()/'Icons/Gicon.png'
        self.checkIcon = QtGui.QIcon(str(checkIcon))
        self.icon = QtGui.QIcon(str(icon))
        self.session = session
        self.items = items
        self.user = user
  
        #self
        self.setGeometry(700,400,266,222)
        self.setWindowTitle("Ggroup")
        self.setWindowIcon(self.icon)
        
        #Listwidget
        self.listWidget = QtWidgets.QListWidget(self)
        self.listWidget.setGeometry(QtCore.QRect(5, 5, 260, 145))
        self.listWidget.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        
        #Login
        self.login = login_window()
        self.login.connect_btn.clicked.connect(self.connect_clicked)
        self.login.Password.returnPressed.connect(self.connect_clicked)
        self.login.User_name.returnPressed.connect(self.connect_clicked)
        
        #Systray
        self.tray = SystemTrayIcon(self.icon,self)     
        
        #Lables
        self.jump_lbl = QtWidgets.QLabel(self)
        self.jump_lbl.setGeometry(QtCore.QRect(10, 200, 101, 17))

        self.last_lbl = QtWidgets.QLabel(self)
        self.last_lbl.setGeometry(QtCore.QRect(10, 160, 160, 17))

        self.next_lbl = QtWidgets.QLabel(self)
        self.next_lbl.setGeometry(QtCore.QRect(10, 180, 160, 17))

        #Buttons
        self.update_btn = QtWidgets.QPushButton(self)
        self.update_btn.setText('update')
        self.update_btn.setGeometry(QtCore.QRect(165, 160, 81, 30))
        self.update_btn.clicked.connect(self.update_checked)
        
    def connect_clicked(self):
        if self.login.pass_approved and self.login.user_approved:
            try:
                self.user.create(self.login.User_name.text(),self.login.Password.text())
                self.login.hide()
                self.show()
                self.trayNotify('?????????????? ?????????? ????????????')
            except:
                QMessageBox.warning(self,'Error: login faild','?????????? ???????? ???????????????? ?????? ?????? ???? ?????? ???? ???????????? ?????????? ??????????')
                sys.exit()
            if os.path.isfile(Grepo.path()/'data/cookies/cookie.pkl'):
                os.remove(Grepo.path()/'data/cookies/cookie.pkl')

          
    def show(self,state=True):
        if state:
            self.login.setVisible(False)
            self.setVisible(True)
            self.tray.setVisible(True)
        else:
            self.setVisible(False)
            self.login.setVisible(True)

    def closeEvent(self,event):
        event.ignore()
        self.hide()
    
    def trayNotify(self,msg):
        self.tray.showMessage('?????????? ??????????',msg,msecs=10)
        
    def set_labels(self,last,next,repeat):
        self.jump_lbl.setText("Today jump: "+repeat)
        self.last_lbl.setText("Last: "+last)
        self.next_lbl.setText("Next: "+next) 
    
    def update_checked(self):
        item = self.listWidget.selectedItems()
        if not item:
            return
        item[0].setIcon(self.checkIcon)
        self.selected.setIcon(QtGui.QIcon())
        self.selected = item[0]
        
    def update_items(self,items):
        if not items:
            return
        self.listWidget.clear()
        self.selected = None
        self.itemList = []
        for item in items:
            Item = QListWidgetItem(self.listWidget)
            Item.setText(item["name"])
            if item["state"] == 2:
                Item.setIcon(self.checkIcon)
                self.selected = Item
            self.itemList.append(Item)
            

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self,icon, parent):
        super().__init__(icon,parent)
        #Git repository
        self.repository = Grepo()
        
        self.main_win = parent
        #Main widget
        menu = QtWidgets.QMenu()
        usrAction = menu.addAction("Change User/Pass")
        usrAction.triggered.connect(self.changeUser)
        self.updateAction = menu.addAction('check for updates')
        self.updateAction.triggered.connect(self.checkUpdate)
        #self.updateAction.installEventFilter()
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)
        self.setIcon(icon)
        self.activated.connect(self.DoubleClick)
        self.setContextMenu(menu)

        
    def DoubleClick(self,reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.main_win.show(True)
    
    def checkUpdate(self):
        self.contextMenu().exec_(self.contextMenu().pos())
        try:
            flag = self.repository.hasUpdate()
        except:
            QMessageBox.warning(self.main_win,'Error: update faild','?????????? ???????? ?????????????? ?????????? ?????? ?????? ???? ?????? ???? ???????????? ?????????? ??????????')
            return
        if flag == self.repository.FAST_FORWARD:
            self.updateAction.setText('New update available')
            self.updateAction.disconnect()
            self.updateAction.triggered.connect(self.update)
        elif flag == self.repository.HEAD_UPTODATE:
            self.updateAction.setText('Everything up to date')
            self.updateAction.disconnect()
            self.updateAction.triggered.connect(self.checkUpdate)
        elif flag == self.repository.ERROR:
            self.updateAction.setText("Error occurred")
            self.updateAction.disconnect()

    def update(self):
        try:
            self.repository.pull()
            QMessageBox.information(self.main_win,'Updater','Update succsesfull\nclosing the app')
            QApplication.exit()
        except:
            QMessageBox.warning(self.main_win,'Error: update faild','?????????? ???????? ?????????????? ?????????? ?????? ?????? ???? ?????? ???? ???????????? ?????????? ??????????')
            self.updateAction.setText("Error occurred")
            self.updateAction.triggered.disconnect()
            return False
        return True
        
    def changeUser(self):
        self.main_win.show(False)
                 
    def exit(self):
      QApplication.exit()
      
if __name__ == '__Main__':
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    main = main_window()
    #main.set_labels('14','22','15')

    main.show()
    sys.exit(app.exec_())