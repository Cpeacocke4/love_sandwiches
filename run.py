import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Request sales data input from user, and repeat request 
    until valid data input is given.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, seperated by commas.")
        print("example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here:")
    
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each menu item.

    Surplus is defined as the sale subtracted from the stock:
    - Positive indicates left over stock.
    - Negative indicates fresh stock made when product was sold out.
    """
    print("Calculating surplus data...\n")
    
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def validate_data(values):
    """
    Inside the try, converts all string values into intergers.
    Raises ValueError if strings cannot be converted into int, 
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6: 
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e: 
        print(f"Invalid data: {e}, please try again.")
        return False

    return True

#def update_sales_worksheet(data):
    #"""
    #Update sales worksheet by adding new data with the list data provided.
    #"""
    #print("Updating sales worksheet, please wait...\n")
    #sales_worksheet = SHEET.worksheet('sales')
    #sales_worksheet.append_row(data)
    #print("Sales worksheet updated succesfully!\n")

#def update_surplus_worksheet(surplus_row):
   # """
   # Update surplus worksheet by adding the data returned from the 
    #calculate_surplus_data function.
    #"""
    #print("Updating surplus worksheet, please wait...\n")
    #surplus_worksheet = SHEET.worksheet('surplus')
    #surplus_worksheet.append_row(surplus_row)
    #print("Surplus worksheet updated succesfully!\n")

def update_worksheet(data, worksheet):
    """
    Updates relevant worksheet with relevant data.
    """
    print(f"Updating {worksheet} worksheet, please wait...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated succesfully!\n")

def get_last_5_entries_sales():
    """
    Collects colloms of data from the worksheet, collecting the last 5 
    entries for each sandwich, and returns them as a list of lists.
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def calculate_stock_data(data):
    """
    Calculating the average stock for each menu item, adding 10%.
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data
 
def main(): 
    """
    Runs all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love Sandwiches Data Automation\n")
main()


