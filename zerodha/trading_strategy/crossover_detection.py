import global_variables
from zerodha.util import send_email as email

log = global_variables.log

def find_crossovers(dates, closing_prices):
    no_of_data = global_variables.no_of_data
    custom_col_1_value = closing_prices.rolling(
        int(global_variables.custom_col_1[4:])
    ).mean()

    crossover = []
    old_closing_price = closing_prices.values[no_of_data - 2]
    new_closing_price = closing_prices.values[no_of_data - 1]
    old_date = dates[no_of_data - 2]
    new_date = dates[no_of_data - 1]
    old_sma = custom_col_1_value.values[no_of_data - 2]
    new_sma = custom_col_1_value.values[no_of_data - 1]
    log.info(
        f"Processing for-> 1. Previous timestamp= {old_date}, 2. Current timestamp= {new_date}, "
        f"3. Previous Closing Price= {old_closing_price}, 4.Current Closing Price= "
        f"{new_closing_price}, 5.Previous SMA9= {old_sma}, 6.New SMA9= {new_sma}."
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
        f"""
        Dear Client,<br><br>
        
        At {crossover[1]} we identified a significant crossover event in your trading account. Here are the details:<br><br>

        <ol>
            <li><b>Previous time:</b> {crossover[0]}</li>
            <li><b>Current time:</b> {crossover[1]}</li>
            <li><b>Previous closing price:</b> {crossover[2]}</li>
            <li><b>Latest closing price:</b> {crossover[3]}</li>
            <li><b>Previous SMA9:</b> {crossover[4]}</li>
            <li><b>Latest SMA9:</b> {crossover[5]}</li>
            <li><b>Decision for this Trade:</b> {crossover[6]}</li>
        </ol>

        We have taken immediate action to address this situation. However, we encourage you to review the decision and take any necessary actions if you have concerns.<br><br>

        Your satisfaction and peace of mind are paramount to us. If you have any questions or require further assistance, please do not hesitate to contact us.<br><br>

        Thank you for choosing Trading Mantra.<br><br>

        Warm regards,<br>
        TradingMantra Support Team<br>
        """
    )
    disclaimer = "<b>Disclaimer:</b> Please note that closing prices may slightly vary due to the timing of order placement."
    full_gmail_message = gmail_message + "<br><br>" + disclaimer

    email.send_gmail(
        log=log,
        subject="AlgoTrading - New Crossover ALERT!!",
        message=full_gmail_message,
    )
    log.info(
        f'CrossOver Gmail is sent for "{crossover[3]}" closing price.'
    )


def send_multi_crossover_email(crossovers):
    gmail_message = (
        f"""
        Dear Client,<br><br>
        
        We are writing to bring to your attention a critical development in your trading account.<br><br>

        <strong>Multiple Crossover Detected</strong><br><br>

        Multiple crossovers have been generated, and immediate attention is required to address this issue. The first two crossovers are recorded as follows:
        <ol>
            <li><b>Crossover 1:</b> {crossovers[0]}</li>
            <li><b>Crossover 2:</b> {crossovers[1]}</li>
        </ol>

        It's important to note that there may be additional crossovers that require your attention. We strongly recommend a thorough review of your trading account to ensure its integrity.<br><br>

        Should you require any assistance or have questions regarding these developments, please do not hesitate to contact us immediately. Your satisfaction and success in trading are our top priorities.<br><br>

        Thank you for entrusting your trading activities to TradingMantra.<br><br>

        Warm regards,<br>
        TradingMantra Support Team<br>
        """

    )
    email.send_gmail(
        log=log,
        subject="Bug in Crossover Logic!!",
        message=gmail_message,
    )
    log.warning("Sent mail for multiple crossover.")
