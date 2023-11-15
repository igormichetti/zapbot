#auth
from secretapi import __path
import gspread, json
import pandas as pd
from google.oauth2 import service_account

def authenticate_gspread(sheet_title):
    with open(r'C:\Users\miche\Downloads\libertooth-54397966ad63.json', 'r') as json_file:
        credentials_data = json.load(json_file)
    
    credentials = service_account.Credentials.from_service_account_info(
        credentials_data,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"])
    client = gspread.Client(auth=credentials)
    client.login()

    try:
        # Try to open the Google Sheet by title
        sheet = client.open(sheet_title).sheet1
        print(f"Existing Google Sheet opened: {sheet_title}")
    except gspread.exceptions.SpreadsheetNotFound:
        # If the sheet does not exist, create a new one
        sheet = client.create(sheet_title).sheet1
        print(f"New Google Sheet created: {sheet_title}")

    return sheet

def save_to_google_sheet(data, sheet_title):
    sheet = authenticate_gspread(sheet_title)

    # Iterate through each entry in the data
    for entry in data:
        index = entry.get("index", -1)
        data_value = entry.get("Data", "")
        toother = entry.get("Toother", "")
        mensagem = entry.get("Mensagem", "")

        # Check if the row with the given data already exists
        cell = sheet.find(str(index)) if index != -1 else None
        if cell:
            # If the row with the same data exists, skip adding a new row
            print(f"Row with index {index} already exists. Skipping.")
        else:
            # If the row does not exist, append a new row with the data
            sheet.append_row([index, data_value, toother, mensagem])
            print(f"Row added: {entry}")

def read_google_sheet(sheet_title):
    try:
        # Authenticate and open the Google Sheet
        sheet = authenticate_gspread(sheet_title)

        # Read all values from the sheet
        values = sheet.get_all_values()

        # Convert the values to a Pandas DataFrame
        headers = values[0]
        data = values[1:]
        df = pd.DataFrame(data, columns=headers)

        # Display the DataFrame
        print("Data from Google Sheet:")
        print(df)

        return df

    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return None
