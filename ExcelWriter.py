import pygsheets

#authorization
gc = pygsheets.authorize(service_file='GoogleAuth/google_auth.json') # Google auth file generated from google developer account
worksheet = gc.open('Late Prop Tax Input trent') # Name of the google sheet

def write_data_to_sheet(sheet_num, data_dict):
    new_row = [data_dict["mailingNameOrignal"], data_dict["mailingNameFormatted"], data_dict["mailingAdress"],
               data_dict["mailingCity"], data_dict["mailingState"], data_dict["mailingZip"], data_dict["ownerName"],
               data_dict["ownerAdress"], "Prop Tax"]

    try:
        if sheet_num == 1:
            sheet = worksheet.worksheet_by_title("DELQ1") #Sheet name
        else:
            sheet = worksheet.worksheet_by_title("DELQ2") #Sheet name

        cells = sheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        sheet.insert_rows(last_row, number=1, values= new_row)
        print("Spread sheet "+str(sheet_num)+" written successfully.")
    except Exception as ex:
        print("=> Spread sheet " + str(sheet_num) + " writing failed...")
        print(new_row)
        print(str(ex))