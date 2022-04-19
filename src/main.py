import configparser
import ExcelWriter as GSheetWriter
from AutomateLookup import AutomateLookup

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
    f = open("record/final_parcel_id_name.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        splitted_line = line.split("|")
        parcel_rec[splitted_line[0].strip()] = splitted_line[-1].strip()
        line = f.readline().split("\n")[0]
    f.close()
    return parcel_rec


def write_already_processed_record(parcel_id):
    f = open("record/processed_rec.txt", "a")
    f.write(parcel_id + "\n")
    f.close()


def read_already_processed_record():
    parcel_rec = []
    f = open("record/processed_rec.txt", "r")
    line = f.readline().split("\n")[0]
    while line != "" and line != None:
        parcel_rec.append(line)
        line = f.readline().split("\n")[0]
    f.close()
    return parcel_rec


general_conf = confParser("general_conf")
CHROME_PATH = general_conf["chrome_path"]

parcel_lookup_url = general_conf["parcel_lookup_url"]
delq_lookup_url = general_conf["delq_lookup_url"]
property_tax_pdf_lookup = general_conf["property_tax_pdf_lookup"]
google_spread_sheet_link = general_conf["google_spread_sheet_link"]
pdf_download_link = general_conf["pdf_download_link"]

parcel_record = read_parcel_record()
already_processed_record = read_already_processed_record()

if __name__ == '__main__':

    for parcel_id in parcel_record.keys():
        automate_lookup = AutomateLookup(CHROME_PATH)
        try:
            if parcel_id not in already_processed_record:
                automate_lookup.open_page(delq_lookup_url)
                data_dict = automate_lookup.search_parcel_delq(parcel_id)
                if data_dict["DELQ"]:
                    automate_lookup.open_page(property_tax_pdf_lookup)
                    data_dict = automate_lookup.search_parcel_tax_pdf(parcel_id, pdf_download_link, data_dict)
                    if data_dict:
                        GSheetWriter.write_data_to_sheet(data_dict)
                else:
                    print("NO DELQ found. Skipping...")

                write_already_processed_record(parcel_id)
                already_processed_record.append(parcel_id)
            else:
                print("=> " + parcel_id + " already processed. Skipping...")
        except Exception as e:
            print(e)
            pass
        automate_lookup.close_website()
