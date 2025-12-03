# import ssi_fc_trading
from ssi_fc_data import fc_md_client , model
import config
import sys
import datetime
import json
import csv

def get_date_input():
    """
    Prompts the user for a date (dd/mm/yyyy).
    Returns the user's date, or today's date if the input is empty.
    
    Returns:
        str: The final date string in 'dd/mm/yyyy' format.
    """
    
    # 1. Get today's date for the default value
    today_date = datetime.date.today().strftime("%d/%m/%Y")
    
    # 2. Set the prompt to inform the user of the default
    prompt = f"Enter a date (dd/mm/yyyy) or press Enter for today ({today_date}): "
    
    # 3. Get the user's input
    user_input = input(prompt).strip() # .strip() removes any leading/trailing whitespace
    
    # 4. Check if the input is empty
    if not user_input:
        # If input is empty, use today's date
        final_date = today_date
    else:
        # If input is provided, use it directly (requires validation in a real application)
        final_date = user_input
        
    return final_date

client = fc_md_client.MarketDataClient(config)
def md_access_token():
	print(client.access_token(model.accessToken(config.consumerID, config.consumerSecret)))

def md_get_securities_list():
    req = model.securities('HNX', 1,100)
    print(client.securities(config, req))

def md_get_securities_details():
    req = model.securities_details('HNX', 'ACB', 1, 100)
    print(client.securities_details(config, req))

def md_get_index_components():
	print(client.index_components(config, model.index_components('vn100', 1, 100)))

def md_get_index_list():
	print(client.index_list(config, model.index_list('hnx', 1, 100)))

def md_get_daily_OHLC():
	print(client.daily_ohlc(config, model.daily_ohlc('ssi', '15/10/2020', '15/10/2020', 1, 100, True)))

def md_get_intraday_OHLC():
	print(client.intraday_ohlc(config, model.intraday_ohlc('fpt', '15/10/2020', '15/10/2020', 1, 100, True, 1)))

def md_get_daily_index():
	print(client.daily_index(config, model.daily_index( '123', 'VN100', '15/10/2020', '15/10/2020', 1, 100, '', '')))

def md_get_stock_price():
	print(client.daily_stock_price(config, model.daily_stock_price ('fpt', '15/10/2020', '15/10/2020', 1, 100, 'hose')))



def main():
    # md_get_intraday_OHLC()
    symbol = input("Enter ticker symbol: ")
    startDate = get_date_input()
    endDate = get_date_input()
    print(f"Fetching intraday OHLC data for {symbol} from {startDate} to {endDate}...")
    # print(client.intraday_ohlc(config, model.intraday_ohlc(symbol, startDate, endDate, 1, 100, True, 1)))
    dict = client.intraday_ohlc(config, model.intraday_ohlc(symbol, startDate, endDate, 1, 100, True, 1))
    totalRecords = dict.get('totalRecords', 0)
    data = dict.get('data', [])
    if not data:
        print("No data found for the given parameters.")
        return
    
    fieldnames = data[0].keys()  # Assuming all dictionaries have the same keys
    filename = f"intraday_ohlc_{symbol}_{startDate.replace('/', '-')}_to_{endDate.replace('/', '-')}.csv"

    # 4. Open the file and write the data
    try:
        # Use 'w' (write mode), newline='' (to prevent extra blank rows), and encoding
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a DictWriter object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the header row using the defined fieldnames
            writer.writeheader()
            # Write all the data rows from the list of dictionaries
            writer.writerows(data)
        print(f"✅ Successfully converted list of dictionaries to {filename}")

    except IOError as e:
        print(f"❌ An error occurred while writing to the file: {e}")
    
    # filename = f"intraday_ohlc_{symbol}_{startDate.replace('/', '-')}_to_{endDate.replace('/', '-')}.json"
    # try:    
    #     with open(filename, 'w') as f:
    #         json.dump(data, f, indent=4)
    #     print(f"Data saved to {filename}")
    # except IOError as e:
    #     print(f"Error saving data to file: {e}")

if __name__ == '__main__':
	main()