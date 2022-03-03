# The selenium module
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

ua = UserAgent()


class WebDriver:
    def __init__(self, chrome_path):
        self.webdriver = None
        self.chrome_path = chrome_path

    def init_driver(self):
        WINDOW_SIZE = "1920,1080"
        CHROME_DRIVER_PATH = "ChromDriver/chromedriver"
        driver = None
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = self.chrome_path
        chrome_options.add_argument("User-Agent=" + str(ua.random))
        chrome_options.add_argument(f'Referer=https://www.google.com/')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("disable-notifications")
        self.webdriver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)

    def close_webdriver(self):
        try:
            self.webdriver.close()
        except:
            pass
