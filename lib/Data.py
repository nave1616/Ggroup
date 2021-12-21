
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from datetime import datetime,timedelta
from pathlib import Path
from Grepo import Grepo


     
class Singleton(object):
    _instance = None
    def __new__(cls, *args):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class Data:
    def __init__(self):
        path = Grepo.path()
        self.session = Session(path/'data/session.yml')
        self.items = Item(path/'data/items.yml')
        
    def update(self):
        self.session.update()
        self.items.update()
    
    def load(self):
        self.session.load()
        self.items.load()
    
    def __str__(self) -> str:
        return f'{self.session} , {self.items}'
    
    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(
        self.__module__, type(self).__name__, hex(id(self)))

class Item:
    def __init__(self,path):
        self.path = Path(path)
        self.list = self.load()
        self.len = len(self.list) if self.list else 0
    
    def add_items(self,items):
        self.list = items
        self.update()
        
    def update(self):
        output = dump(self.list, Dumper=Dumper,allow_unicode=True)        
        with open(self.path, 'w') as stream:
            stream.write(output)
    
    def load(self):
        try:
            with open(self.path, 'r') as stream:
                self.list = load(stream, Loader=Loader)
        except:
            self.path.touch(exist_ok=True)
            self.list = []
        return self.list
    
    @property
    def checked(self):
        for index in range(self.len):
            if self.list[index].get("state") == 2:
                return index+1
        return -1
    
    def __str__(self) -> str:
        if not self.list:
            return 'Items: Empty'
        return f'{self.list}'
    
    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(
        self.__module__, type(self).__name__, hex(id(self)))
        
class Session:
    def __init__(self,path):
        self.path = Path(path)
        self.date = datetime.now().date().strftime("%d-%m-%y")
        if not self.path.exists():
            self.create()
        self.__session = self.load()
    
    def update(self):
        data = {"last":self.last,"next":self.next,"repeat":self.repeat}
        output = dump(data, Dumper=Dumper)
        with open(self.path, 'w') as stream:
            stream.write(output)

    def load(self):
        with open(self.path, 'r') as stream:
            self.__session = load(stream, Loader=Loader)
        return self.__session
     
    def create(self):
        last = datetime.now().replace(second=0,microsecond=0)
        next = (last + timedelta(hours=7))
        self.__session = {'last':last,'next':next,'repeat':0}
        self.update()
        return self.__session
    
    def toprint(self):
        last = self.__session["last"].strftime("%H:%M %d-%m-%y")
        next = self.__session["next"].strftime("%H:%M %d-%m-%y")
        repeat = self.__session["repeat"]
        return (last,next,str(repeat))
    
    @property
    def next(self):
        return self.__session["next"]
    
    @next.setter
    def next(self,value):
        self.__session["next"] = value
    
    @property
    def last(self):
        return self.__session["last"]
    
    @last.setter
    def last(self,value):
        value = ' '.join([value,self.date])
        self.__session["last"] = datetime.strptime(value,"%H:%M %d-%m-%y")
        if self.repeat == 1:
            self.next = self.__session["last"]+timedelta(hours=17)
        else:
            self.next = self.__session["last"]+timedelta(hours=7)
    
    @property
    def repeat(self):
        return self.__session["repeat"]
    
    @repeat.setter
    def repeat(self,value):
        self.__session["repeat"] = value%3
        return self.__session["repeat"]
    
    def __str__(self) -> str:
        return f'Last: {self.last} , Next: {self.next} , Repeat: {self.repeat}'
    
    def __repr__(self):
        return '<{0}.{1} object at {2}>'.format(
        self.__module__, type(self).__name__, hex(id(self)))
    
        
class User:
    def __init__(self):
        self.path = Grepo.path()/'data/user.yml'
        self.name,self.pwd = None,None
        if self.usr_exists:
            self.name,self.pwd = self.load()
        
    @property
    def usr_exists(self):
        if not self.path.exists():
            return False
        return True
    
    def update(self):
        data = {"name":self.name,"pwd":self.pwd}
        output = dump(data, Dumper=Dumper)
        with open(self.path, 'w') as stream:
            stream.write(output)

    def load(self):
        with open(self.path, 'r') as stream:
            usr = load(stream, Loader=Loader)
            return usr["name"],usr["pwd"]
            
    def create(self,name,pwd):
        self.name,self.pwd = name,pwd
        self.update()
        return {'name':name,'pwd':pwd}


if __name__ == '__main__':      
    data = Data('/home/vegi/Desktop/Projects/Gimpel/data')
    data.load()

 
