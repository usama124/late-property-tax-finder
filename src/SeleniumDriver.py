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
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--ignore-certificate-errors')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        chrome_options.binary_location = self.chrome_path
        chrome_options.add_argument("User-Agent=" + str(ua.random))
        chrome_options.add_argument(f'Referer=https://www.google.com/')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("disable-notifications")

        chrome_options.add_experimental_option('prefs', {
            "download.default_directory": "/home/usama/PycharmProjects/Personal/late-property-tax-finder/src/PDF_FILES",  # Change default directory for downloads
            "download.prompt_for_download": False,  # To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
        })

        self.webdriver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options)

    def close_webdriver(self):
        try:
            self.webdriver.close()
        except:
            pass
