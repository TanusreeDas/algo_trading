import matplotlib.pyplot as plt
import pandas as pd
from kite.util import generate_file as create_file, generate_kite as gen_kite, date, send_email as email

# Initialize values
no_of_data=9
instrument_token=256265 #256265=NIFTY 50
from_date=date.get_delta_india_time(1)
to_date=date.get_current_india_time()
interval="15minute"
continuous=False
oi=False

custom_col_1 = "Sma_9"
decision_maker = ""
custom_col_1_value=0
stop_loss=0
trade_entry_price=0

def find_crossovers(dates,closing_prices):
    global custom_col_1_value
    # Calculate the SMA9 for last two points
    custom_col_1_value = closing_prices.rolling(int(custom_col_1[4:])).mean()

    # Check for crossovers to take the buy and sell decision
    crossover = []

    old_closing_price= closing_prices.values[no_of_data-1]
    new_closing_price = closing_prices.values[no_of_data]
    old_date= dates.values[no_of_data-1]
    new_date=dates.values[no_of_data]
    old_sma= custom_col_1_value.values[no_of_data-1]
    new_sma= custom_col_1_value.values[no_of_data]

    if old_closing_price > old_sma and new_closing_price < new_sma:#Price crosses above SMA9 (crossover from below)
        crossover.append((old_date, new_date, old_closing_price, new_closing_price, old_sma,new_sma,'Buy'))
    elif old_closing_price < old_sma and new_closing_price > new_sma:#Price crosses below SMA9 (crossover from above)
        crossover.append((old_date, new_date, old_closing_price, new_closing_price, old_sma,new_sma,'Sell'))

    return crossover

def plot_crossovers(dates,closing_prices,crossover):
    global decision_maker,trade_entry_price,stop_loss

    plt.plot(dates, closing_prices, label='Closing Price')
    plt.plot(dates, custom_col_1_value, label=custom_col_1)

    print(decision_maker.values())

    #One Buy and Sell at al time
    #need to complete this logic tommorrow
    if crossover[5] == 'Buy'and decision_maker in ("","Buy"):
            plt.scatter(crossover[1], crossover[3], marker='o', color='green') #Single Buy
            decision_maker = "Sell"
            trade_entry_price=crossover[3]
            stop_loss = trade_entry_price - 50
    elif crossover[5] == 'Sell' and decision_maker in ( "", "Sell") :
            plt.scatter(crossover[1], crossover[3], marker='o', color='red')  # Single Buy
            decision_maker = "Buy"
            trade_entry_price = crossover[3]
            stop_loss = trade_entry_price + 50

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{instrument_token} - Closing Price and Soft Margin Average with Crossovers')
    plt.legend()
    plt.show()

def check_stop_loss(date_index,closing_price):
    global trade_entry_price,stop_loss,decision_maker
    if closing_price < stop_loss:
        if decision_maker == "Buy":
            plt.scatter(date_index, closing_price, marker='x', color='darkgreen')
        elif decision_maker == "Sell":
            plt.scatter(date_index, closing_price, marker='x', color='maroon')
        decision_maker = ""
        trade_entry_price = 0
        stop_loss=0


def main():

    kite=gen_kite.generate_instance()
    current_india_time=to_date

    historical_data=kite.historical_data( instrument_token, from_date, to_date, interval, continuous, oi)
    current_data=kite.ltp("NSE:NIFTY 50")

    #merge two files
    latest_data = [(dict1['date'], dict1['close']) for dict1 in historical_data[-no_of_data:]]
    latest_data.append((current_india_time, current_data['NSE:NIFTY 50']['last_price']))
    latest_data_df=pd.DataFrame(latest_data,columns=['date','close'])

    dates=latest_data_df['date']
    closing_prices=latest_data_df['close']

    #create_file.generate_csv_file("converted_data",latest_data_df,['date','close'])

    crossovers = find_crossovers(dates,closing_prices)
    len_crossover=len(crossovers)

    # Stop loss value, mark both decision and column name=""
    #add logger

    if len_crossover == 1:
        crossover = crossovers[0]
        plot_crossovers(dates, closing_prices, crossover)
        gmail_message = f"At {crossover[1]} time we found one crossover for {crossover[3]} closing price. \n\n" \
                        f" More details-> \n 1. Previous time= {crossover[0]},\n 2. Current time= {crossover[1]}," \
                        f"\n 3. Previous closing price= {crossover[2]},\n 4. Latest closing price= {crossover[3]}," \
                        f"\n 5. Previous SMA9= {crossover[4]},\n 6. Latest SMA9= {crossover[5]},\n 7. Decision for this Trade= {crossover[6]}.\n" \
                        f"Take necessary action if you think the decision is wrong. \n\n\n Thanks and Regards,\n TradingMantra"
        email.send_gmail(subject="AlgoTrading - New Crossover ALERT!!",message=gmail_message)
    elif len_crossover>1:
        gmail_message = f"Multiple Crossover Generated, Fix the problem ASAP!! Details-> First two messages are {crossovers[0]} " \
                        f"and {crossovers[1]}. There could be more. Please check"
        email.send_gmail(subject="Bug in Crossover Logic!!", message=gmail_message)
    check_stop_loss(current_india_time, current_data['NSE:NIFTY 50']['last_price'])

if __name__ == "__main__":
    while True:
        main()