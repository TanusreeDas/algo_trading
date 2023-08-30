import global_variables
from zerodha.util import send_email as email


def find_crossovers(dates, closing_prices):
    no_of_data = global_variables.no_of_data
    custom_col_1_value = closing_prices.rolling(
        int(global_variables.custom_col_1[4:])
    ).mean()

    crossover = []
    old_closing_price = closing_prices.values[no_of_data - 1]
    new_closing_price = closing_prices.values[no_of_data]
    old_date = dates.values[no_of_data - 1]
    new_date = dates.values[no_of_data]
    old_sma = custom_col_1_value.values[no_of_data - 1]
    new_sma = custom_col_1_value.values[no_of_data]
    global_variables.log.info(
        f"Processing for-> 1. Previous Closing Price= {old_closing_price}, 2.Current Closing Price= "
        f"{new_closing_price}, 3.Previous SMA9= {old_sma}, 4.New SMA9= {new_sma} on {new_date}"
    )

    if old_closing_price > old_sma and new_closing_price <= new_sma:
        crossover.append(
            (
                old_date,
                new_date,
                old_closing_price,
                new_closing_price,
                old_sma,
                new_sma,
                "Sell",
            )
        )
    elif old_closing_price < old_sma and new_closing_price >= new_sma:
        crossover.append(
            (
                old_date,
                new_date,
                old_closing_price,
                new_closing_price,
                old_sma,
                new_sma,
                "Buy",
            )
        )

    return crossover


def send_crossover_email(crossover):
    gmail_message = (
        f"At {crossover[1]} time we found one crossover for {crossover[3]} closing price. \n\n"
        f" More details-> \n 1. Previous time= {crossover[0]},\n 2. Current time= {crossover[1]},"
        f"\n 3. Previous closing price= {crossover[2]},\n 4. Latest closing price= {crossover[3]},"
        f"\n 5. Previous SMA9= {crossover[4]},\n 6. Latest SMA9= {crossover[5]},\n 7. Decision for this Trade= {crossover[6]}.\n"
        f"Take necessary action if you think the decision is wrong. \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=global_variables.log,
        subject="AlgoTrading - New Crossover ALERT!!",
        message=gmail_message,
    )
    global_variables.log.info(
        f'CrossOver Gmail is sent for "{crossover[3]}" closing price.'
    )


def send_multi_crossover_email(crossovers):
    gmail_message = (
        f"Multiple Crossover Generated, Fix the problem ASAP!! Details-> First two messages are {crossovers[0]} "
        f"and {crossovers[1]}. There could be more. Please check. \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=global_variables.log,
        subject="Bug in Crossover Logic!!",
        message=gmail_message,
    )
    global_variables.log.warning("Sent mail for multiple crossover.")
