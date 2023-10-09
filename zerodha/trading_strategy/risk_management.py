import global_variables
import order_placement
from zerodha.util import send_email as email

log = global_variables.log


def send_stop_loss_email(type,closing_price):
    gmail_message = (
        f"""
        Dear Client,<br><br>

        <strong>{type} level breached.</strong><br> 
        Check the below data and please take immediate action in case you find any discrepancy.<br>
        
        <ol>
            <li><b>Closing price:</b> {closing_price}</li>
            <li><b>Stop Loss Level:</b> {global_variables.stop_loss_level}</li>
            <li><b>Target Profit Level:</b> {global_variables.target_profit_level}</li>
            <li><b>Decision on the Trade:</b> {global_variables.decision_maker}</li>
        </ol>
        
        We kindly request your immediate attention to this situation. To address the issue, we will take the necessary action to close all open trades and initiate a fresh trade when the next crossover is identified.<br><br>

        If you believe that the decision taken is incorrect or have any concerns, please do not hesitate to contact us. Your feedback is of utmost importance as we are committed to ensuring the best outcomes for your trading account.<br><br>

        Thank you for choosing TradingMantra.<br><br>
        
        Warm Regards,<br>
        TradingMantra Support Team<br>"""
    )

    disclaimer = "<b>Disclaimer:</b> Please note that closing prices may slightly vary due to the timing of order placement."
    full_gmail_message = gmail_message + "<br><br>" + disclaimer

    email.send_gmail(
        log=log, subject=f"{type} Level Breached!!", message=full_gmail_message
    )

    log.info(
        f"{type} level is crossed. Had to make a decision on below dataset-> "
        f"1. Current closing price = {closing_price}, 2. target profit level= {global_variables.target_profit_level}"
        f" and 3. stop loss level = {global_variables.stop_loss_level}."
    )

    global_variables.decision_maker = ""
    global_variables.trade_entry_price = 0
    global_variables.stop_loss_level = 0
    global_variables.target_profit_level = 0

    log.debug(
        "reinitialized decision_maker, trade_entry_price, target profit level and stop_loss_level. Now trade "
        "engine start fresh. Next trade will not be dependent on any previous trade decision."
    )

def check_stop_loss(closing_price):
    if (
        closing_price > global_variables.stop_loss_level
        and global_variables.decision_maker == "Buy"
    ):
        log.debug(
            f"Stop loss level is breached. Current closing price is higher than stop loss"
            f"level. So closing existing sell trade by buying underlying."
        )
        send_stop_loss_email("Stop Loss",closing_price)
        order_id = order_placement.book_order("Buy", 1)
        order_placement.send_order_placement_email_stop_level_crossed("Stop Loss", order_id)
    elif (
        closing_price < global_variables.stop_loss_level
        and global_variables.decision_maker == "Sell"
    ):
        log.debug(
            f"Stop loss level is breached. Current closing price is lower than stop loss"
            f"level. So closing existing sell trade by selling underlying."
        )
        send_stop_loss_email("Stop Loss",closing_price)
        order_id = order_placement.book_order("Sell", 1)
        order_placement.send_order_placement_email_stop_level_crossed("Stop Loss", order_id)
    else:
        order_id = 0
        log.debug("Stop loss level is not breached.")

    return order_id


def check_target_profit(closing_price):
    if (
        closing_price < global_variables.target_profit_level
        and global_variables.decision_maker == "Buy"
    ):
        log.debug(
            f"Target Profit level is much higher than current closing price. So taking decision of buying "
            f"existing trade to minimize loss."
        )
        send_stop_loss_email("Target Profit",closing_price)
        order_id = order_placement.book_order("Buy", 1)
        order_placement.send_order_placement_email_stop_level_crossed("Target Profit", order_id)
    elif (
        closing_price > global_variables.target_profit_level
        and global_variables.decision_maker == "Sell"
    ):
        log.debug(
            f"Target Profit level is much lower than current closing price. So taking decision of selling"
            f" existing trade to minimize loss."
        )
        send_stop_loss_email("Target Profit",closing_price)
        order_id = order_placement.book_order("Sell", 1)
        order_placement.send_order_placement_email_stop_level_crossed("Target Profit", order_id)
    else:
        order_id = 0
        log.debug("Target profit level is not breached.")

    return order_id


def check_profit_margin_and_stop_loss(closing_price):
    target_profit_order_id = check_target_profit(closing_price)
    stop_loss_order_id = 0
    if target_profit_order_id == 0:
        stop_loss_order_id = check_stop_loss(closing_price)
    if stop_loss_order_id == 0 and target_profit_order_id == 0:
        order_placement.update_profit_margin_and_stop_loss(closing_price)
