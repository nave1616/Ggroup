try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException,InvalidArgumentException
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.service import Service
except ImportError as selerror:
    pass

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as webmangererror:
    pass
import logging
import sys
from os import error
from time import sleep
from pathlib import Path
import pickle

# Critcal program cant continue run
# Error Driver module cannot perform function
logging.basicConfig(filename='driver.log',level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s %(message)s',
                    datefmt='%m/%d/%y %H:%M')


class Driver(webdriver.Chrome):
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        #self.options.add_argument('headless')
        service = Service(ChromeDriverManager().install())
        super().__init__(service=service,options=self.options)
        self.implicitly_wait(10)
    
    def save_cookie(self):
        with open('/home/vegi/Desktop/Gproject/data/cookies/cookie.pkl', 'wb') as filehandler:
            pickle.dump(self.get_cookies(), filehandler)

    def load_cookie(self):
        with open('/home/vegi/Desktop/Gproject/data/cookies/cookie.pkl', 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                self.add_cookie(cookie)
                
    def login(self,usr,pwd):
        url = 'https://market.marmelada.co.il/vendor.php?dispatch=auth.login_form&return_url=vendor.php'
        if Path('/home/vegi/Desktop/Gproject/data/cookies/cookie.pkl').is_file():
            self.get(url)
            self.load_cookie()
            self.refresh()
            self.popOver_Handler()
            self.product()
            return True
        try:
            self.get(url)
        except InvalidArgumentException as msg:
            self.Errors(msg)
        try:
            uname = self.find_element(by=By.ID,value='username')
            upwd = self.find_element(by=By.ID,value='password')
            submmit = self.find_element(by=By.NAME,value='dispatch[auth.login]')
        except error as msg:
            self.Errors(msg)
        uname.send_keys(usr)
        upwd.send_keys(pwd)
        submmit.click()
        self.save_cookie()
        sleep(2)
        self.popOver_Handler()
     
    def Errors(self,msg):
        logging.error(msg=f'{msg}')
        self.quit()
        sys.exit(1) 
         
    def update_items(self,checked=None):
        items = []
        try:
            cnt = int(self.find_element(by=By.XPATH,value='//*[@id="pagination_contents"]/div[1]/div[2]/div/a/span[2]').text)
        except error as msg:
            self.Errors(msg)
        for i in range(1,cnt):
            try:
                name = self.find_element(by=By.XPATH ,value='//*[@id="pagination_contents"]/div[3]/table/tbody/tr['+str(i)+']/td[4]/a').get_attribute('title')
            except:
                name = None
                break
            if checked and name == checked:
                items.append({'name':name,'state':2})
            else:
                items.append({'name':name,'state':1})
        return items
    
    def product(self):
        try:
            self.find_element(by=By.XPATH,value='//*[@id="header_subnav"]/ul/ul[2]/li[3]/a').click()
        except error as msg:
            self.Errors(msg)
        try:
            self.find_element(by=By.XPATH,value='//*[@id="header_subnav"]/ul/ul[2]/li[3]/ul/li[1]/a/span[1]').click()
        except error as msg:
            self.Errors(msg)
        
        
    def jump(self,index):
        try:
            self.find_element(by=By.XPATH ,value='//*[@id="pagination_contents"]/div[3]/table/tbody/tr['+str(index)+']/td[11]').click()
        except error as msg:
            self.Errors(msg)
        
    def popOver_Handler(self):
        try:
            pop = self.find_element(by=By.CSS_SELECTOR,value="[id*='poptin']")
        except:
            pass
        try:
            pop.find_element(by=By.XPATH,value='//*[@id="closeXButton"]/span/p/span').click()
        except:
            pass

        
        
        
if __name__ == '__main__':
    driver = Driver()
    driver.login('club.wine.israel@gmail.com','123456')
    driver.close()