import os, time, traceback, urllib
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


Navigator = webdriver.Chrome
Config = Options


path = os.getcwd()
filepath = os.path.join(path, "Files")
driverpath = os.path.join(filepath, "chromedriver")
cookiespath = os.path.join(filepath, "cookies.pkl")

address = "https://web.whatsapp.com/"
from_phone = "55XXYYYYYYYY"
timeout = 15

config = Config()
config.headless = True #default: False
config.add_argument(f"user-data-dir={filepath}")
pickle.load(open(cookiespath, "rb"))

#navigator = Navigator(executable_path=driver_path, chrome_options=config)
driver = os.path.join('Files', "cookies.pkl")
navigator = Navigator(
    executable_path=driver,
    chrome_options=config
)

navigator.get(address)
#navigator.find_elements(By.CLASS_NAME, value=value) #By.CLASS_NAME = 'class name'
#navigator.find_elements(By.CSS_SELECTOR, value=value) #By.CSS_SELECTOR = 'css selector'
#navigator.find_elements(By.ID, value=value)
#navigator.find_elements(By.LINK_TEXT, value=value)
#navigator.find_elements(By.NAME, value=value)
#navigator.find_elements(By.PARTIAL_LINK_TEXT, value=value)
#navigator.find_elements(By.TAG_NAME, value=value)
#navigator.find_elements(By.XPATH, value=value)
while len(navigator.find_elements(By.ID, value="side")) < 1:
    time.sleep(1)

dict = {"phone": from_phone, "text": "hello world!\nUhul!"}

dict['text'] = urllib.parse.quote(dict['text'])
url = "send?phone={phone}&text={text}"
url = url.format(**dict)
navigator.get(address+url)

while len(navigator.find_elements(
        by="id",
        value='side')
        ) < 1:
    time.sleep(1)

web_element = navigator.find_elements(
    by="xpath",
    value='//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button/span'
)[0]
web_element.click()
#web_element.send_keys(Keys.Enter)

pickle.dump(
    navigator.get_cookies(),
    open(cookies_path, "wb")
)





"""
self.toCheck('load', 'find_elements_by_id')


self.checks = {
    "load": {"find_elements_by_id": "side"},
    }
self.actions = {
    "send_message":
        {
        'url': "send?phone={phone}&text={text}",
        'context': {'phone': "", "text": ""},
        'xpath': '//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button/span',
        'press': Keys.ENTER
        },
    }
    
    def toAct(self,
            action: str='send_message',
            by: str='xpath',
            press: str="enter",
            timeout: int=0
            ):
        try:
            _timeout = abs(timeout) or self.timeout
            if press:
                press = WhatsApp.Keyboard.get(press)
            if by == 'xpath':
                self.navigator.find_element_by_xpath(
                    self.actions.get(action).get(by)
                    ).send_keys(press) #Keys.ENTER
                sleep(_timeout)
                return True
            return False
        except Exception:
            print(format_exc())
            return False
    
    def dumpCookies(self, path: str, cookies_file: str="cookies.pkl"):
        try:
            path = path or self.path
            cookies_path = os.path.join(path, cookies_file)
            pickle.dump(
                self.navigator.get_cookies(),
                open(cookies_path, "wb")
                )
            return True
        except Exception: #noqa
            print(format_exc())
            return False

    def loadCookies(self, path: str, cookies_file: str="cookies.pkl"):
        try:
            #self.navigator.get(self.address)
            path = path or self.path
            cookies_path = os.path.join(path, cookies_file)
            if os.path.exists(cookies_path):
                cookies = pickle.load(
                    open(cookies_path, "rb")
                    )
                for cookie in cookies:
                    self.navigator.add_cookie(cookie)
                return True
            return False
        except Exception: #noqa
            print(format_exc())
            return False
    
    def sendMessage(self, phone: str, message: str):
        try:
            self.toCheck("load", "find_elements_by_id")
            text = urllib.parse.quote(message)
            url = self.actions.get("send_message").get("url")
            url.format(phone=phone, text=text)
            _link = self.address + url
            self.toAccess(link)
            self.toCheck('load', 'find_elements_by_id')
            self.toAct(action="send_message", by="xpath", press="enter")
            return True
        except Exception: #noqa
            print(format_exc())
            return False
    
    def closeWhatsApp(self, cookies_file: str="cookies.pkl"):
        try:
            self.dumpCookies(self.path, cookies_file)
            self.navigator.close()
            return True
        except Exception: #noqa
            print(format_exc())
            return False


# UNIT-TEST
if __name__ == "__main__":
    whatsapp = WhatsApp("",
        from_phone="5548991344015",
        driver='chromedriver.exe'
        )




# pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()
driver.get('https://www.google.com')
driver.find_element(By.NAME, 'q').send_keys('Yasser Khalil')









# DUMP & SAVE COOKIIES

import pickle
import selenium.webdriver 

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

e depois para adicioná-los de volta:

import pickle
import selenium.webdriver 

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)




import os
from selenium import webdriver

dir_path = os.getcwd()
profile = os.path.join(dir_path, "profile", "wpp")
options = webdriver.ChromeOptions()
options.add_argument(
    r"user-data-dir={}".format(profile))

browser = webdriver.Chrome("./chromedriver.exe", chrome_options=options)

browser.get("https://web.whatsapp.com")



from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
 
# Replace below path with the absolute path
# to chromedriver in your computer
driver = webdriver.Chrome('/home/saket/Downloads/chromedriver')
 
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
 
# Replace 'Friend's Name' with the name of your friend
# or the name of a group
target = '"Friend\'s Name"'
 
# Replace the below string with your own message
string = "Message sent using Python!!!"
 
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
group_title.click()
inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located((
    By.XPATH, inp_xpath)))
for i in range(100):
    input_box.send_keys(string + Keys.ENTER)
    time.sleep(1)
"""