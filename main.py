import configparser

from AutomateLookup import AutomateLookup
from SeleniumDriver import WebDriver

parser = configparser.ConfigParser()
parser.read("Conf/config.ini")


def confParser(section):
    if not parser.has_section(section):
        print("No section info  rmation are available in config file for", section)
        return
    # Build dict
    tmp_dict = {}
    for option, value in parser.items(section):
        option = str(option)
        value = value
        tmp_dict[option] = value
    return tmp_dict


def read_parcel_record():
    parcel_rec = {}
    f = open("record/parcel_id_name.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        splitted_line = line.split("|")
        parcel_rec[splitted_line[0].strip()] = splitted_line[-1].strip()
        line = f.readline().split("\n")[0]
    f.close()
    return parcel_rec


def write_parcel_record(parcel_info_obj):
    f = open("record/parcel_id_name.txt", "a")
    for parcel in parcel_info_obj.keys():
        f.write(parcel + "|" + parcel_info_obj[parcel] + "\n")
    f.close()


def write_parcel_record_data(path, parcel_info_obj):
    f = open(path, "w")
    for parcel in parcel_info_obj.keys():
        f.write(parcel + "|" + parcel_info_obj[parcel] + "\n")
    f.close()


def apply_validation(parcel_record_data):
    final_parcel_rec = {}
    skipped_parcel_rec = {}
    exclude_list = ["APTS", "CORP", "Inc", "Incorporated", "LLC", "AGENCY"]
    for parcel_id in parcel_record_data:
        res = [True if x.lower() in parcel_record_data[parcel_id].lower() else False for x in exclude_list]
        #res = list(set(res))
        while False in res: res.remove(False)
        if len(res) == 0:
            final_parcel_rec[parcel_id] = parcel_record_data[parcel_id]
        else:
            skipped_parcel_rec[parcel_id] = parcel_record_data[parcel_id]
    write_parcel_record_data("record/skipped_parcel_id_name.txt", skipped_parcel_rec)
    write_parcel_record_data("record/final_parcel_id_name.txt", final_parcel_rec)
    return final_parcel_rec


general_conf = confParser("general_conf")
CHROME_PATH = general_conf["chrome_path"]

parcel_lookup_url = general_conf["parcel_lookup_url"]
delq_lookup_url = general_conf["delq_lookup_url"]
property_tax_pdf_lookup = general_conf["property_tax_pdf_lookup"]
google_spread_sheet_link = general_conf["google_spread_sheet_link"]

parcel_record = read_parcel_record()

selenium_webdriver = WebDriver(CHROME_PATH)


if __name__ == '__main__':
    automate_lookup = AutomateLookup(CHROME_PATH)

    #automate_lookup.open_page(parcel_lookup_url)
    #parcel_record = automate_lookup.get_parcel_owner_info()
    #write_parcel_record(parcel_record)

    parcel_record = apply_validation(parcel_record)

    automate_lookup.open_page(delq_lookup_url)
    for parcel_id in parcel_record.keys():
        automate_lookup.search_parcel_delq(parcel_id)

    automate_lookup.open_page(property_tax_pdf_lookup)
    for parcel_id in parcel_record.keys():
        automate_lookup.search_parcel_tax_pdf(parcel_id)

    automate_lookup.close_website()
