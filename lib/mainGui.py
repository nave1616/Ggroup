
import sys
import re
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication,QListWidgetItem, QMenu, QMessageBox, QSystemTrayIcon,QWidget
from pathlib import Path
from gitRepo import gitRepo

Project_path = gitRepo.path()
cookies_path = Path(gitRepo.path()/'data/cookies/cookie.pkl')
navegiMsg ='הייתה בעיה בניסיון לעדכן נסה שוב או דבר עם הנווגי הקרוב לביתך'
class login_window(QWidget):
    def __init__(self):
        super().__init__(None)
        
        #Properties
        path = gitRepo.path()/'Icons'
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
        #self.User_name.textChanged[str].connect(self.login_approve)

        self.Password = QtWidgets.QLineEdit(self)
        self.Password.setGeometry(QtCore.QRect(10, 60, 165, 25))
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        #self.Password.textChanged[str].connect(self.login_approve)
        
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
        self.connect_btn.setText( "התחבר")
        self.user_approved = False
        self.pass_approved = False
        
        self.show_btn = QtWidgets.QPushButton(self)
        self.show_btn.setGeometry(QtCore.QRect(144, 60, 30, 25))
        self.show_btn.setStyleSheet("border: 0;\nbackground: transparent;")
        self.show_btn.setIcon(self.showIcon)
        self.show_btn.setCheckable(True)
        self.show_btn.clicked.connect(self.show_hide)
    
    def login_approve(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, self.User_name.text()):
            self.user_approved = True
            self.uname_error.setText("")
        else:
            self.user_approved = False
            self.uname_error.setText("מייל לא תקין")
        if 0 <= len(self.Password.text()) < 5:
            self.pass_approved = False
            self.pass_error.setText("שגיאה: 5 תווים לפחות")
        else:
            self.pass_approved = True
            self.pass_error.setText("")
        return self.pass_approved and self.user_approved
             
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
        
        checkIcon = gitRepo.path()/'Icons/check.png'
        icon = gitRepo.path()/'Icons/Gicon.png'
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
        self.updater = Updater(self,self.tray)
        self.tray.updateAction.triggered.connect(self.updater.checkUpdate)
        
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
        if self.login.login_approve():
            self.user.create(self.login.User_name.text(),self.login.Password.text())
            self.login.hide()
            self.show()
            self.tray.showMessage('','התחברות בוצעה בהצלחה',self.icon)
            cookies_path.unlink(missing_ok=True)
          
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
    
    def set_labels(self,last,next,repeat):
        self.jump_lbl.setText("Today jump: "+repeat)
        self.last_lbl.setText("Last: "+last)
        self.next_lbl.setText("Next: "+next) 
    
    def update_checked(self):
        item = self.listWidget.selectedItems()
        try:
            item[0].setIcon(self.checkIcon)
            self.selected.setIcon(QtGui.QIcon())
            self.selected = item[0]
        except:
            None
        
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
        self.main_win = parent
        menu = QMenu(parent)
        self.icon = icon
        self.userAction = menu.addAction("Change User/Pass",self.changeUser)
        self.updateAction = menu.addAction('check for updates')            
        self.exitAction = menu.addAction("Exit",QApplication.exit)
        self.setIcon(icon)
        self.activated.connect(self.mousePressEvent)
        self.setContextMenu(menu)

    def mousePressEvent(self,reason):
        if reason == QSystemTrayIcon.Trigger:
            self.main_win.show()
            
    def changeUser(self):
        self.main_win.show(False)

class Updater():
    def __init__(self,window,tray):
        self.repository = gitRepo()
        self.tray = tray
        self.window = window
        
    def checkUpdate(self):
        try:
            flag = self.repository.hasUpdate()
        except:
            QMessageBox.warning(self.window,'Error: update faild',navegiMsg)
            return
        if flag == self.repository.FAST_FORWARD:
            self.updateAvailable()
        elif flag == self.repository.HEAD_UPTODATE:
            self.tray.showMessage('Everything up to date','',self.tray.icon)
            self.tray.updateAction.setText('Everything up to date')
        elif flag == self.repository.ERROR:
            self.tray.updateAction.setText("Error occurred")
            self.tray.updateAction.disconnect()
    
    def updateAvailable(self):
        msg = self.tray.showMessage('New update available','you can click to update',self.tray.icon)
        msg.clicked.connect(self.update)
        self.tray.updateAction.setText('Update now')
        self.tray.updateAction.disconnect()
        self.tray.updateAction.triggered.connect(self.update)
    
    def update(self):
        try:
            self.repository.pull()
            QMessageBox.information(self.window,'Updater','Update succsesfull\nclosing the app')
            QApplication.exit()
        except:
            QMessageBox.warning(self.window,'Error: update faild','הייתה בעיה בניסיון לעדכן נסה שוב או דבר עם הנווגי הקרוב לביתך')
            self.tray.updateAction.setText("Error occurred")
            self.tray.updateAction.triggered.disconnect()
            return False
        return True                
class Menu(QMenu):
    def __init__(self,parent,tray):
        super().__init__(parent)
        self.addAction("Change User/Pass",tray.changeUser)
        self.updateAction = self.addAction('check for updates',tray.checkUpdate)            
        self.addAction("Exit",QApplication.exit)
    def exec_(self):
        super().show()
               
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    w = QWidget()
    icon = gitRepo.path()/'Icons/Gicon.png'
    icon = QtGui.QIcon(str(icon))
    tray = QSystemTrayIcon(icon,w)
    main = Menu(w,tray)

    main.show()
    sys.exit(app.exec_())