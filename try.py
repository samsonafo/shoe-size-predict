import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("new.json", scope)

client = gspread.authorize(creds)

sheet = client.open("shoe-size").sheet1  # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records

row = sheet.row_values(3)  # Get a specific row
col = sheet.col_values(3)  # Get a specific column
cell = sheet.cell(1,2).value  # Get the value of a specific cell

print(data)

insertRow = [35,4, 23]
# sheet.add_rows(insertRow, 4)  # Insert the list as a row at index 4
sheet.insert_row(insertRow, 2)

# numRows = sheet.row_count  # Get the number of rows in the sheet
