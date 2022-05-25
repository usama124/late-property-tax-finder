import time
from datetime import date
from bs4 import BeautifulSoup
import PdfMiner

from SeleniumDriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class AutomateLookup:

    def __init__(self, chrome_path):
        self.selenium_obj = WebDriver(chrome_path)
        self.selenium_obj.init_driver()
        self.webDriver = self.selenium_obj.webdriver
        self.action = ActionChains(self.webDriver)

    def open_page(self, page_url):
        self.webDriver.get(page_url)

    def get_parcel_owner_info(self):
        parcel_info_obj = {}
        main_navigation = self.webDriver.find_element_by_id("SelectABC")
        cat_button_elements = main_navigation.find_elements_by_tag_name("button")
        for elem in cat_button_elements:
            time.sleep(2)
            self.webDriver.execute_script("arguments[0].scrollIntoView();", main_navigation)
            #self.action.move_to_element(main_navigation).perform()
            #elem.click()
            self.webDriver.execute_script("arguments[0].click();", elem)
            parcel_info_obj = self.read_details(parcel_info_obj)

        return parcel_info_obj

    def read_details(self, parcel_info_obj):
        time.sleep(3)
        prev_length = 0
        current_length = 0
        cntr = 0
        while True:
            page_obj = self.get_page_obj()
            try:
                result_table_data = page_obj.find("table", attrs={"id": "ResultTable"}).find("tbody").findAll("tr")
                for row_data in result_table_data:
                    col_data = row_data.findAll("td")
                    if float(col_data[-1].text.strip()) > 1000.0:
                        parcel_info_obj[col_data[0].text.strip()] = col_data[1].text.strip()
                current_length = len(parcel_info_obj.keys())
            except Exception as e:
                print(e)
            try:
                # self.webDriver.find_element_by_id("ResultTable_next").click()
                next_page_elem = self.webDriver.find_element_by_xpath('//*[@id="ResultTable_next"]/a')
                #self.action.move_to_element(next_page_elem).perform()
                self.webDriver.execute_script("arguments[0].scrollIntoView();", next_page_elem)
                #next_page_elem.click()
                self.webDriver.execute_script("arguments[0].click();", next_page_elem)
                if current_length == prev_length:
                    if cntr == 3:
                        break
                    cntr += 1
                prev_length = current_length
            except Exception as e:
                print(e)
                break

        return parcel_info_obj

    def type_as_human(self, parcel_id, input_field):
        for one in parcel_id:
            input_field.send_keys(one)
            time.sleep(0.05)

    def search_parcel_delq(self, parcel_id):
        try:
            data_dict = {"DELQ": None}
            current_year = date.today().year - 2
            time.sleep(3)
            input = self.webDriver.find_element_by_id("ParcelSearch")
            input.clear()
            self.type_as_human(parcel_id, input)
            #input.send_keys(parcel_id)
            search_button = self.webDriver.find_element_by_id("BeginSearch")
            self.webDriver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})", search_button)
            time.sleep(3)
            search_button.click()
            time.sleep(10)
            try:
                WebDriverWait(self.webDriver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#multipleCatId > div > table')))
            except:
                pass

            page_obj = self.get_page_obj()
            result_table = page_obj.find("table", attrs={"class": "table table-bordered table-striped"})
            if not result_table:
                return data_dict
            rows = result_table.find("tbody").findAll("tr")
            delq_counter = 0
            for row in rows:
                col_data = row.findAll("td")
                if int(col_data[2].text.strip()) >= current_year:
                    typee = col_data[0].text.strip()
                    delq_counter = delq_counter + 1 if typee.lower() == "delq" else delq_counter
            data_dict["DELQ"] = delq_counter if delq_counter != 0 else None
        except Exception as e:
            print(e)
            return {"DELQ": None}
        return data_dict

    def search_parcel_tax_pdf(self, parcel_id, pdf_download_link, data_dict, exclude_list):
        #iframe = self.webDriver.find_element_by_xpath('//*[@id="leftNavArea"]/div[1]/div[1]/div/iframe')
        #self.webDriver.switch_to.frame(iframe)
        parcel_div_button = self.webDriver.find_element_by_xpath('//*[@id="headingParcelID"]/button')
        self.webDriver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})",
                                      parcel_div_button)
        time.sleep(3)
        parcel_div_button.click()
        input_field = self.webDriver.find_element_by_id("parcelid")
        input_field.send_keys(parcel_id)
        time.sleep(3)
        self.webDriver.find_element_by_id("SubmitParcel").click()
        time.sleep(6)
        #Finding information from table on https://slco.org/assessor
        page_obj = self.get_page_obj()
        table_data = page_obj.select_one("#parcelFieldNames > div.valueSummBox > div > table")
        table_rows = table_data.findAll("tr")
        owner_name = table_rows[0].findAll("td")[-1].text.strip()
        if "BOLLWINKEL, DANE".lower() in owner_name.lower():
            return None
        exclude = False
        for excl in exclude_list:
            if excl.lower() in owner_name.lower():
                exclude = True
                break
        if exclude:
            return None
        data_dict["ownerName"] = owner_name
        data_dict["ownerAdress"] = table_rows[1].findAll("td")[-1].text.strip()
        #Downloading and reading PDF
        prop_tax_pdf_link_gen = self.webDriver.find_element_by_xpath('//*[@id="skipto"]/div/aside/div/div/div/div/ul/li[3]/button')
        self.webDriver.execute_script("arguments[0].scrollIntoView({'block':'center','inline':'center'})",
                                      prop_tax_pdf_link_gen)
        time.sleep(3)
        prop_tax_pdf_link_gen.click()
        time.sleep(10)

        self.webDriver.switch_to.window(self.webDriver.window_handles[-1])
        pdf_download_link = self.webDriver.current_url

        # pdf_download_link = pdf_download_link + parcel_id
        contact_placeholder = PdfMiner.convert_pdf_to_txt(PdfMiner.download_pdf(pdf_download_link, parcel_id))
        #Extracting required information from PDF
        contact_placeholder.pop(0)
        data_dict["mailingAdress"] = contact_placeholder.pop(-2)
        contact_details = contact_placeholder.pop(-1)
        contact_details = contact_details.split(" ")
        while '' in contact_details: contact_details.remove('')
        data_dict["mailingZip"] = contact_details.pop(-1)
        data_dict["mailingState"] = contact_details.pop(-1)
        data_dict["mailingCity"] = " ".join(contact_details)
        data_dict["mailingNameFormatted"] = self.format_name(contact_placeholder)
        mailing_name = " & ".join(contact_placeholder)
        data_dict["mailingNameOrignal"] = mailing_name

        exclude = False
        for excl in exclude_list:
            if excl.lower() in mailing_name.lower():
                exclude = True
                break
        if exclude:
            return None

        return data_dict

    def format_name(self, name_object):
        final_name = []
        for name in name_object:
            name = name.split(";")[0].split(",")
            final_name.append(name[-1].strip() + " " + name[0].strip())

        return " & ".join(final_name)

    def close_website(self):
        try:
            self.selenium_obj.close_webdriver()
        except:
            pass

    def get_page_obj(self):
        return BeautifulSoup(self.webDriver.page_source, 'lxml')
