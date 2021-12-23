
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from datetime import datetime,timedelta
from pathlib import Path
from gitRepo import gitRepo

def next_time(date,time):
    '''return data object +time hours'''
    return date+timedelta(hours=time)   

def datetime_to_str(data):
    '''Return str from datetime object'''
    return data.strftime("%H:%M %d-%m-%y")

def str_now():
    '''Return current date %H:%M %d-%m-%y'''
    return datetime.now().strftime("%H:%M %d-%m-%y")    

def Todate():
    '''Return current date "%d-%m-%y"'''
    return datetime.now().date().strftime("%d-%m-%y")

def str_to_date(str):
    '''Return datetime object from str %H:%M %d-%m-%y'''
    return datetime.strptime(str,"%H:%M %d-%m-%y")  

def datetime_now():
    '''Return datetime object time now %H:%M %d-%m-%y'''
    return str_to_date(str_now())

class Data:
    def __init__(self,filename):
        self.path = gitRepo.path()/f'data/{filename}'
        if isinstance(self,Item):
            self.path.touch(exist_ok=True)
        self.load()
      
    def update(self):
        output = dump(self.data, Dumper=Dumper,allow_unicode=True)        
        with open(self.path, 'w') as stream:
            stream.write(output)
            return self.data
    def load(self):
        if not self.path.exists():
            return
        with open(self.path, 'r') as stream:
            self.data = load(stream, Loader=Loader)
            return self.data

class Item(Data):
    def __init__(self):
        super().__init__('items.yml')
    
    def add_items(self,items):
        self.data = items
        self.update()

    @property
    def checked(self):
        for index in range(len(self.data)):
            if self.list[index].get("state") == 2:
                return index+1
        return -1
     
class Session(Data):
    def __init__(self):
        super().__init__('session.yml')
        self.date = Todate()
        if not self.path.exists():
            self.create()
    
    def create(self):
        last = datetime_now()
        next = next_time(last,7)
        self.data = {'last':last,'next':next,'repeat':0}
        self.update()
        return self.data
    
    def text(self):
        last = datetime_to_str(self.data["last"])
        next = datetime_to_str(self.data["next"])
        repeat = self.data["repeat"]
        return (last,next,str(repeat))
    
    @property
    def next(self):
        return self.data["next"]
    
    @next.setter
    def next(self,value):
        self.data["next"] = value
    
    @property
    def last(self):
        return self.data["last"]
    
    @last.setter
    def last(self,value):
        value = ' '.join([value,self.date])
        self.data["last"] = str_to_date(value)
        if self.repeat == 1:
            self.next = next_time(self.data["last"],17)
        else:
            self.next = next_time(self.data["last"],7)
    
    @property
    def repeat(self):
        return self.data["repeat"]
    
    @repeat.setter
    def repeat(self,value):
        self.data["repeat"] = value%3
        return self.data["repeat"]
          
class User(Data):
    def __init__(self):
        self.path = Path(gitRepo.path()/f'data/user.yml')
        
    @property
    def usr_exists(self):
        if not self.path.exists():
            return False
        return True
            
    def create(self,name,pwd):
        self.data = {"name":name,"pwd":pwd}
        self.update()
        return self.data


if __name__ == '__main__':      
    data = Session()
    print(data.last)



 
