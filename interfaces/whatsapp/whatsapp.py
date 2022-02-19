import os, sys, platform, socket
from time import monotonic, sleep
from traceback import format_exc
from pprint import pprint
import urllib
import pickle

from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, InvalidCookieDomainException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import boto3


class WhatsApp():
    
    
    Actions = {
        "send_message":
        {
            'url': "send?phone={phone}&text={text}",
            'context': {'phone': "", "text": ""},
            'xpath': '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button',
            #'//*[@id="main"]/footer/div[1]/div/div/div[2]/div[2]/button/span',  
            'press': Keys.ENTER
        },
    }
    Checks = {
        "load": {"find_elements_by_id": "side"},
    }
    Config = ChromeOptions #Config = FirefoxOptions
    Keyboard = {
        'enter': Keys.ENTER,
    }
    Manager = ChromeDriverManager #Manager = GeckoDriverManager
    Navigator = webdriver.Chrome  #Navigator = webdriver.Firefox
    Remote = webdriver.Remote
    
    
    def __init__(self,
            from_phone: str,
            folder: str="files",
            driver: str='chromedriver',
            cookies_folder: str='cookies',
            headless: bool=True,
            remote: bool=False,
            first_access: bool=False,
            timeout: float=30.0
            ):
        """WhatsApp Constructor"""
        self.name = 'whatsapp bot'
        self.version = '1.0'
        self.description = "whatsapp bot (WABot) via selenium"
        self.address = "https://web.whatsapp.com/"
        self.path = os.getcwd()
        self.driverpath = os.path.join(self.path, folder, driver)
        self.cookiespath = os.path.join(self.path, cookies_folder)
        self.timeout = timeout
        self.buffer = {}
        self.comment = "[WABot] {}."
        self.checks = WhatsApp.Checks
        self.actions = WhatsApp.Actions
        self.from_phone = from_phone \
            or os.environ.get('WHATSAPP_ACCOUNT')
        
        self.config = WhatsApp.Config()
        self.toConfig(headless=headless)
        
        if remote == False:
            self.navigator = WhatsApp.Navigator(
                WhatsApp.Manager().install(),
                chrome_options=self.config,
                )
        else:
            self.config.set_capability("browserName", "Chrome")
            self.navigator = WhatsApp.Remote(
		        options=self.config
            )
        
        self.toAccess()
        self.loadCookies()
        self.is_connected = self.toCheck()
        if self.is_connected:
            self.dumpCookies()
    
    @classmethod
    def getOperationalSystem(cls):
        return platform.system()
    
    @classmethod
    def getComputerUsername(cls):
        opsystem = WhatsApp.getOperationalSystem()
        if opsystem == 'Windows':
            username = os.environ['USERNAME']
        elif opsystem == 'Linux':
            username = os.environ.get('USERNAME') \
                or os.environ.get('LOGNAME')
        else:
            username = None
        return username
    
    @classmethod
    def getCookieSession(cls, session_name: str="Wtsp"):
        try:
            opsystem = WhatsApp.getOperationalSystem()
            username = WhatsApp.getComputerUsername()
            if opsystem == 'Linux':
                CHROME_SYSTEM_PATH=f'/home/{username}/.config/google-chrome/{session_name}'
            elif opsystem == "Windows":
                CHROME_SYSTEM_PATH=f'C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\{session_name}'
            if os.path.exists(CHROME_SYSTEM_PATH):
                CHROME_PROFILE_PATH=f'user-data-dir={CHROME_SYSTEM_PATH}'
                return CHROME_PROFILE_PATH
            return False
        except Exception: #noqa
            print(format_exc())
            return False
    
    def toComment(self, comment: str="WABot comment"):
        print(self.comment.format(comment))
    
    def setCookieSession(self, session_name: str="Wtsp"):
        try:
            return self.config.add_argument(
                WhatsApp.getCookieSession(
                    session_name=session_name
                    )
                )
        except Exception: #noqa
            print(format_exc())
            return False
    
    def toConfig(self,
            cookiespath: str="",
            headless: bool=True
            ):
        try:
            cookiespath = cookiespath or self.cookiespath
            if headless:
                self.config.headless = headless
            self.config.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) " \
                +"AppleWebKit/537.36 (KHTML, like Gecko) " \
                +"Chrome/95.0.4638.54 Safari/537.36"
                )
            self.config.add_argument('--no-sandbox')
            self.config.add_argument('--disable-dev-shm-usage')
            self.config.add_argument(
                f"user-data-dir={cookiespath}"
                )
            self.config.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
                )
            #--proxy-server=host:port
            #--no-proxy-server
            #--proxy-auto-detect
            #--proxy-pac-url=URL
            #--password-store=<basic|gnome|kwallet>
            #$HOME/.config/google-chrome - Default directory for configuration data.
            #$HOME/.cache/google-chrome - Default directory for cache data.
            return True
        except Exception:
            print(format_exc())
            return False
    
    def toAccess(self, link: str=""):
        try:
            link = link or self.address
            self.navigator.get(link)
            sleep(self.timeout)
            return True
        except Exception: #noqa
            print(format_exc())
            return False
    
    def toCheck(self,
            check: str='load',
            condition: str="find_elements_by_id",
            timeout: float=0
            ):
        try:
            start = monotonic()
            timeout = timeout or self.timeout
            
            if check == 'load' \
                    and condition == 'find_elements_by_id':
                by = By.ID
            elif check == 'load' \
                    and condition == 'find_elements_by_xpath':
                by = By.XPATH
            else:
                by = By.TAG_NAME
            
            while len(self.navigator.find_elements(
                        by,
                        self.checks.get(check).get(condition)
                        )
                    ) < 1:
                sleep(1)
                if (monotonic() - start) > timeout:
                    return False
            return True
        except Exception:
            print(format_exc())
            return False
    
    def toSelect(self,
            by: str='id',
            register: str="side",
            timeout: int=0
            ):
        try:
            timeout = abs(timeout) or self.timeout
            if by == 'id': by = By.ID
            elif by == 'xpath': by = By.XPATH
            else: by = By.TAG_NAME
            web_elements = self.navigator.find_element(
                by, register)
            sleep(timeout)
            return web_elements
        except Exception:
            print(format_exc())
            return False
    
    def toSelectOne(self,
            by: str='id',
            register: str="side",
            timeout: int=0
            ):
        timeout = abs(timeout) or self.timeout
        return self.toSelect(
            by=by,
            register=register,
            timeout=timeout)[0]
    
    def toAct(self,
            action: str='send_message',
            by: str='xpath',
            press: str="enter",
            timeout: int=0
            ):
        try:
            # SETUP
            timeout = abs(timeout) or self.timeout
            if press:
                press = WhatsApp.Keyboard.get(press)
            act_by = By.XPATH
            if action == 'send_message':
                if by == 'id': act_by = By.ID
                elif by == 'xpath': act_by = By.XPATH
                elif by == 'tag_name': act_by = By.TAG_NAME
            # ACT
            webelement = self.navigator.find_element(
                act_by,
                self.actions.get(action).get(by)
                )
            #webelement.send_keys(press)
            #webelement.send_keys("submit")
            webelement.click()
            sleep(timeout)
            return True
        except Exception:
            print(format_exc())
            return False
    
    def dumpCookies(self,
            cookiespath: str="",
            cookiesfile: str='cookies.pkl',
            ):
        try:
            cookiespath = cookiespath or self.cookiespath
            cookiespath = os.path.join(cookiespath, cookiesfile)
            pickle.dump(
                self.navigator.get_cookies(),
                open(cookiespath, "wb")
                )
            return True
        except Exception: #noqa
            print(format_exc())
            return False

    def loadCookies(self,
            cookiespath: str="",
            cookiesfile: str='cookies.pkl',
            ):
        """docstring"""
        try:
            cookiespath = cookiespath or self.cookiespath
            cookiespath = os.path.join(cookiespath, cookiesfile)
            if os.path.exists(cookiespath):

                cookies = pickle.load(
                    open(cookiespath, "rb")
                )
                self.navigator.delete_all_cookies()
                for cookie in cookies:
                    if isinstance(cookie.get('expiry'), float):
                        cookie['expiry'] = int(cookie['expiry'])
                    if cookie.get('domain', '').find('whatsapp'):
                        cookie['domain'] = "web.whatsapp.com" #self.address
                    try:
                        self.navigator.add_cookie(
                            cookie,
                        )
                    except InvalidCookieDomainException:
                        print(format_exc())
                
                return True

            return False

        except InvalidCookieDomainException as Error:

            print(Error)
            print(format_exc())
        except Exception: #noqa

            print(format_exc())
            return False
    
    def deleteCookies(self,
            domains=None
            ):
        if domains is not None:

            cookies = self.navigator.get_cookies()
            original_len = len(cookies)
            for cookie in cookies:
                if str(cookie["domain"]) in domains:
                    cookies.remove(cookie)
            if len(cookies) < original_len:  # if cookies changed, we will update them
                # deleting everything and adding the modified cookie object
                self.navigator.delete_all_cookies()
                for cookie in cookies:
                    self.navigator.add_cookie(cookie)
            
        else:

            self.navigator.delete_all_cookies()
    
    def takePrintScreen(self,
            directory: str="",
            folder: str="files",
            filename: str="screenshot",
            extension: str="png"
            ):
        try:
            directory = directory or self.path
            filename = ".".join([filename, extension])
            self.navigator.save_screenshot(
                os.path.join(
                    directory,
                    folder,
                    filename
                )
            )
            
            return True

        except Exception: #noqa

            print(format_exc())
            return False
    
    def sendMessage(self,
            phone: str,
            message: str
            ):
        try:
            message = urllib.parse.quote(message)
            url = self.actions.get("send_message").get("url")
            url = url.format(phone=phone, text=message)

            link = self.address + url
            self.toAccess(link)
            self.toCheck('load', 'find_elements_by_id')
            self.toAct(
                action="send_message",
                by="xpath",
                press="enter"
            )
            sleep(self.timeout)
            self.takePrintScreen(filename="last_message")

            return True

        except Exception: #noqa

            print(format_exc())
            return False
    
    def closeWhatsApp(self,
            cookiespath: str="",
            cookiesfile: str="cookies.pkl"
            ):
        try:
            cookiespath = cookiespath or self.cookiespath
            self.dumpCookies(
                cookiespath=cookiespath,
                cookiesfile=cookiesfile
            )

            self.navigator.quit()
            self.navigator.close()

            return True

        except Exception: #noqa

            print(format_exc())
            return False


