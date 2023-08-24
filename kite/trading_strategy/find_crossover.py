import matplotlib.pyplot as plt
import pandas as pd
from kite.util import generate_file as create_file, generate_kite as gen_kite, date
from datetime import datetime

# Initialize values
no_of_data=9
instrument_token=256265 #256265=NIFTY 50
from_date=datetime.strptime("2023-08-10", "%Y-%m-%d")
to_date=datetime.strptime("2023-08-23", "%Y-%m-%d")
interval="15minute"
continuous=False
oi=False

custom_col_1 = "Sma_9"
decision_maker = {"Column_name":"","Decision":""} #1st item= type, 2nd item= buy/sell
custom_col_1_value=0
stop_loss=0
trade_entry_price=0

def find_crossovers(dates,closing_prices):
    global custom_col_1_value
    # Calculate the SMA9
    custom_col_1_value = closing_prices.rolling(int(custom_col_1[4:])).mean()

    # Check for crossovers to take the buy and sell decision
    crossover = []
    i=len(closing_prices)-1

    old_closing_price= closing_prices.values[i-1]
    new_closing_price = closing_prices.values[i]
    old_sma= custom_col_1_value.values[i-1]
    new_sma= custom_col_1_value.values[i]


    print("OLD Closing Price= ", old_closing_price)
    print("NEW closing Price= ", new_closing_price )
    print("OLD SMA9= ", old_sma)
    print("NEW SMA9= ", new_sma)

    if old_closing_price > old_sma and new_closing_price < new_sma:#Price crosses above SMA9 (crossover from below)
        crossover.append((dates.values[i], closing_prices[i], 'Buy '+custom_col_1))
    elif old_closing_price < old_sma and new_closing_price > new_sma:#Price crosses below SMA9 (crossover from above)
        crossover.append((dates.values.index[i], closing_prices[i], 'Sell '+custom_col_1))

    return crossover

def plot_crossovers(dates,closing_prices,crossover):
    global decision_maker,trade_entry_price,stop_loss

    plt.plot(dates, closing_prices, label='Closing Price')
    plt.plot(dates, custom_col_1_value, label=custom_col_1)

    print(decision_maker.values())

    #One Buy and Sell at al time
    #need to complete this logic tommorrow
    if crossover[2][0:1] == 'B':
        if  decision_maker["Decision"]=="" and decision_maker["Column_name"]=="":
            plt.scatter(crossover[0], crossover[1], marker='o', color='green') #Single Buy
            decision_maker["Column_name"] = crossover[2].split(' ')[1]
            decision_maker["Decision"] = "Sell"
            trade_entry_price=crossover[1]
            stop_loss = trade_entry_price - 50
        elif decision_maker["Decision"] == "Buy" and decision_maker["Column_name"] == crossover[2].split(' ')[1]:
            plt.scatter(crossover[0], crossover[1], marker='s', color='green') #Double Buy
            decision_maker["Column_name"] = crossover[2].split(' ')[1]
            decision_maker["Decision"] = "Sell"
            trade_entry_price = crossover[1]
            stop_loss = trade_entry_price - 50
    elif crossover[2][0:1] == 'S':
        if decision_maker["Decision"] == "" and decision_maker["Column_name"] == "":
            plt.scatter(crossover[0], crossover[1], marker='o', color='red')  # Single Buy
            decision_maker["Column_name"] = crossover[2].split(' ')[1]
            decision_maker["Decision"] = "Buy"
            trade_entry_price = crossover[1]
            stop_loss = trade_entry_price + 50
        elif decision_maker["Decision"] == "Buy" and decision_maker["Column_name"] == crossover[2].split(' ')[1]:
            plt.scatter(crossover[0], crossover[1], marker='s', color='red')  # Double Buy
            decision_maker["Column_name"] = crossover[2].split(' ')[1]
            decision_maker["Decision"] = "Buy"
            trade_entry_price = crossover[1]
            stop_loss = trade_entry_price + 50

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{instrument_token} - Closing Price and Soft Margin Average with Crossovers')
    plt.legend()
    plt.show()

def check_stop_loss(date_index,closing_price):
    global trade_entry_price,stop_loss,decision_maker
    if closing_price < stop_loss:
        if decision_maker["Decision"] == "Buy":
            plt.scatter(date_index, closing_price, marker='x', color='darkgreen')
        elif decision_maker["Decision"] == "Sell":
            plt.scatter(date_index, closing_price, marker='x', color='maroon')
        decision_maker["Column_name"] = ""
        decision_maker["Decision"] = ""
        trade_entry_price = 0
        stop_loss=0


def main():

    kite=gen_kite.generate_instance()
    current_india_time=date.get_current_india_time()

    historical_data=kite.historical_data( instrument_token, from_date, to_date, interval, continuous, oi)
    current_data=kite.ltp("NSE:NIFTY 50")

    #merge two files
    latest_data = [(dict1['date'], dict1['close']) for dict1 in historical_data[-no_of_data:]]
    latest_data.append((current_india_time, current_data['NSE:NIFTY 50']['last_price']))
    latest_data_df=pd.DataFrame(latest_data)

    create_file.generate_csv_file("converted_data",latest_data_df,['date','close'])

    '''crossovers = find_crossovers(dates, closing_prices)

    # Stop loss value, mark both decision and column name=""

    if len(crossovers) > 0:
        plot_crossovers(dates, closing_prices, crossovers)
    check_stop_loss(historical_data_df.iloc[-1, 0], closing_prices.iloc[-1])'''


if __name__ == "__main__":
    main()