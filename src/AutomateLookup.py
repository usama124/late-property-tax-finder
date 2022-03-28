import time
from datetime import date
from bs4 import BeautifulSoup
import PdfMiner

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
                    if float(col_data[-1].text.strip()) > 1000.0:
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

    def type_as_human(self, parcel_id, input_field):
        for one in parcel_id:
            input_field.send_keys(one)
            time.sleep(0.05)

    def search_parcel_delq(self, parcel_id):
        data_dict = {"DELQ": None}
        current_year = date.today().year - 2
        time.sleep(3)
        input = self.webDriver.find_element_by_id("ParcelSearch")
        input.clear()
        self.type_as_human(parcel_id, input)
        #input.send_keys(parcel_id)
        self.webDriver.find_element_by_id("BeginSearch").click()
        time.sleep(6)

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
        return data_dict

    def search_parcel_tax_pdf(self, parcel_id, pdf_download_link, data_dict):
        iframe = self.webDriver.find_element_by_xpath('//*[@id="leftNavArea"]/div[1]/div[1]/div/iframe')
        self.webDriver.switch_to.frame(iframe)
        input_field = self.webDriver.find_element_by_id("parcelid")
        input_field.send_keys(parcel_id)
        self.webDriver.find_element_by_id("Submit").click()
        time.sleep(6)
        #Finding information from table on https://slco.org/assessor
        page_obj = self.get_page_obj()
        table_data = page_obj.select_one("#parcelFieldNames > div.valueSummBox > div > table")
        table_rows = table_data.findAll("tr")
        data_dict["ownerName"] = table_rows[0].find("td").text.strip()
        data_dict["ownerAdress"] = table_rows[1].find("td").text.strip()
        #Downloading and reading PDF
        pdf_download_link = pdf_download_link + parcel_id
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
        data_dict["mailingNameOrignal"] = " & ".join(contact_placeholder)

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
