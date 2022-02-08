import re
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from SeleniumDriver import WebDriver


class AutomateLookup:

    def __init__(self, chrome_path):
        self.selenium_obj = WebDriver(chrome_path)
        self.selenium_obj.init_driver()
        self.webDriver = self.selenium_obj.webdriver

    def open_page(self, page_url):
        self.webDriver.get(page_url)

    def get_parcel_owner_info(self):
        parcel_info_obj = {}
        cat_button_elements = self.webDriver.find_element_by_id("SelectABC").find_elements_by_tag_name("button")
        for elem in cat_button_elements:
            elem.click()
            parcel_info_obj = self.read_details(parcel_info_obj)

        return parcel_info_obj

    def read_details(self, parcel_info_obj):
        time.sleep(3)
        prev_length = 0
        current_length = 0
        while True:
            page_obj = self.get_page_obj()
            try:
                result_table_data = page_obj.find("table", attrs={"id": "ResultTable"}).find("tbody").findAll("tr")
                for row_data in result_table_data:
                    col_data = row_data.findAll("td")
                    parcel_info_obj[col_data[0].text.strip()] = col_data[1].text.strip()
                current_length = len(parcel_info_obj.keys())
            except Exception as e:
                print(e)
            try:
                self.webDriver.find_element_by_id("ResultTable_next").click()
                if current_length == prev_length:
                    break
                prev_length = current_length
            except Exception as e:
                print(e)
                break

        return parcel_info_obj

    def search_parcel_delq(self, parcel_id):
        current_year = date.today().year - 2
        input = self.webDriver.find_element_by_id("ParcelSearch")
        input.send_keys(parcel_id)
        self.webDriver.find_element_by_id("BeginSearch").click()
        time.sleep(6)

        page_obj = self.get_page_obj()
        result_table = page_obj.find("table", attrs={"class": "table table-bordered table-striped"})
        rows = result_table.find("tbody").findAll("tr")
        delq_counter = 0
        for row in rows:
            col_data = row.findAll("td")
            if int(col_data[2].text.strip()) >= current_year:
                typee = col_data[0].text.strip()
                delq_counter = delq_counter + 1 if typee.lower() == "delq" else delq_counter

        if delq_counter == 1:
            # TODO write in 1st year DELQ spreadsheet
        else:
            # TODO write in 2nd year DELQ spreadsheet

    def search_parcel_tax_pdf(self, parcel_id):
        input = self.webDriver.find_element_by_id("parcelid")
        input.send_keys(parcel_id)
        self.webDriver.find_element_by_id("Submit").click()
        time.sleep(6)

    def close_website(self):
        self.selenium_obj.close_webdriver()

    def get_page_obj(self):
        return BeautifulSoup(self.webDriver.page_source, 'lxml')
