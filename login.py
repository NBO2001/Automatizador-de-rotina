from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

class Login:

    def __init__(self, url, user, password,client, op=False, app=False):
        
        self.urlBase = url
        self.user = user
        self.login = True
        self.passwd = password
        self.client = client
        self.option = Options()
        self.option.headless = True

        if op:
            self.driver = webdriver.Firefox(options=self.option)
        else:
            self.driver = webdriver.Firefox()
            
        self.driver.get(self.urlBase)

        if not self.is_loaded():
            self.login = False
        app.situation("Escrevendo as credenciais ...") if app else print("Escrevendo as credenciais ...") 
        self.name = self.driver.find_element_by_name("username")
        self.name.send_keys(self.user)

        self.pwd = self.driver.find_element_by_name("password")
        self.pwd.send_keys(self.passwd)
        
        self.button = self.driver.find_element_by_xpath("//form/div/button")
        self.button.click()
    

    def is_logout(self):
        return self.login
    

    def get_urlBase(self):
        return self.urlBase


    def getClient(self):
        return self.client


    def authentication_validation(self):
   
        try:
            WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.XPATH, "//app-root/app-main/div/mat-sidenav-container/mat-sidenav/div[1]"))
            )
            
            return True
        except:
            
            return False

    
    def is_loaded(self):
        try:
            WebDriverWait(self.driver, 500).until(
                EC.presence_of_element_located((By.XPATH, "//app-root/app-login/div/mat-card/form/div/button/span"))
            )
            
            return True
        except:
            
            return False