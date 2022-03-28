import pygsheets

#authorization
gc = pygsheets.authorize(service_file='GoogleAuth/google_auth.json') # Google auth file generated from google developer account
worksheet = gc.open('Late Prop Tax Input trent') # Name of the google sheet
sheet = worksheet.worksheet_by_title("DELQ")

def write_data_to_sheet(data_dict):
    new_row = [data_dict["mailingNameOrignal"], data_dict["mailingNameFormatted"], data_dict["mailingAdress"],
               data_dict["mailingCity"], data_dict["mailingState"], data_dict["mailingZip"], data_dict["ownerName"],
               data_dict["ownerAdress"], "Prop Tax"]

    try:
        cells = sheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        sheet.insert_rows(last_row, number=1, values= new_row)
        print("Spread sheet written successfully.")
    except Exception as ex:
        print("=> Spread sheet writing failed...")
        print(new_row)
        print(str(ex))