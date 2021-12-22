import sys
from pathlib import Path
path = Path(__file__).resolve().parent
sys.path.append(str(path/'lib'))
from gitRepo import gitRepo
from Data import *
from mainGui import *
from datetime import datetime
import threading
from time import sleep


with open(gitRepo.path()/'Style.qss','r') as styleFile:
    qss = styleFile.read()

if __name__ == '__main__':
    show = True
    data = Data()
    user = User()
    if not user.usr_exists:
        show = False
    session,items = data.session,data.items
    last,next,repeat = session.toprint()
   
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qss)  
    
    main = main_window(session,items,user)
    main.set_labels(last,next,repeat)
    main.update_items(items.list)
    main.show(show)
    sys.exit(app.exec_())
    