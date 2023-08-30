import global_variables
import order_placement
from zerodha.util import send_email as email

log = global_variables.log


def update_profit_margin_and_stop_loss(ltp):
    current_stop_loss_level = global_variables.stop_loss_level
    current_target_profit_level = global_variables.target_profit_level
    stpt_threshold = global_variables.stpt_threshold
    existing_trade_type = "Buy" if global_variables.decision_maker == "Sell" else "Sell"

    if global_variables.decision_maker == "Buy":
        stpt_multiple = (global_variables.trade_entry_price - ltp) // stpt_threshold
        global_variables.stop_loss_level = (
            global_variables.trade_entry_price
            + global_variables.trailing_stop_loss
            - stpt_multiple * stpt_threshold
        )
        global_variables.target_profit_level = (
            global_variables.trade_entry_price
            - global_variables.trailing_profit_target
            - stpt_multiple * stpt_threshold
        )
    elif global_variables.decision_maker == "Sell":
        stpt_multiple = (ltp - global_variables.trade_entry_price) // stpt_threshold
        global_variables.stop_loss_level = (
            global_variables.trade_entry_price
            - global_variables.trailing_stop_loss
            + stpt_multiple * stpt_threshold
        )
        global_variables.target_profit_level = (
            global_variables.trade_entry_price
            + global_variables.trailing_profit_target
            + stpt_multiple * 25
        )

    log.info(
        f"Dynamic Target profit level and Stop Loss values has changed. 1. Trade_entry_price = "
        f"{global_variables.trade_entry_price}, 2. Current_LTP = {ltp}, 3. Current_trade_type = "
        f"{existing_trade_type}, 4. Old_stop_loss_level = {current_stop_loss_level}, 5. "
        f"Updated_stop_loss_level = {global_variables.stop_loss_level}, 6. Old_target_profit_level = "
        f"{current_target_profit_level}, 7. Current_target_profit_level = {global_variables.target_profit_level}."
    )


def send_stop_loss_email(closing_price):
    gmail_message = (
        f"StopLoss level breached. Check the below data and please take immediate action incase"
        f" you find any discrepancy.\n 1. Closing price= {closing_price},\n 2. Stop Loss Level="
        f" {global_variables.stop_loss_level},\n 3. Target Profit Level= {global_variables.target_profit_level}, \n 4. "
        f"Decision on the Trade= {global_variables.decision_maker}.  \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=log, subject="Stop Loss Level Breached!!", message=gmail_message
    )

    log.info(
        f"Stop Loss Level is Crossed. Had to make a decision on below dataset-> "
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


def send_target_profit_email(closing_price):
    gmail_message = (
        f"Target Profit Level crossed. Check the below data and if you find any problem then take an "
        f"immediate action on this.\n 1. Closing price= {closing_price},\n 2. target profit level= "
        f"{global_variables.target_profit_level} and 3. Stop Loss Level= {global_variables.stop_loss_level},\n "
        f"3. Decision on the Trade= {global_variables.decision_maker}.  \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=log, subject="Stop Loss Level Crossed!!", message=gmail_message
    )

    log.info(
        f"Target Profit Level is Crossed. Had to make a decision on below dataset-> "
        f"1. Current closing price = {closing_price}, 2. target profit level= {global_variables.target_profit_level}"
        f" and 3. stop loss level = {global_variables.stop_loss_level}. Mail is also sent."
    )

    global_variables.decision_maker = ""
    global_variables.trade_entry_price = 0
    global_variables.target_profit_level = 0
    global_variables.stop_loss_level = 0

    log.debug(
        "reinitialized decision_maker, trade_entry_price, target profit level and stop_loss_level. Now trade "
        "engine start fresh. Next trade will not be dependent on any previous trade decision"
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
        order_id = order_placement.book_order("Buy", 1)
        send_stop_loss_email(closing_price)
    elif (
        closing_price < global_variables.stop_loss_level
        and global_variables.decision_maker == "Sell"
    ):
        log.debug(
            f"Stop loss level is breached. Current closing price is lower than stop loss"
            f"level. So closing existing sell trade by selling underlying."
        )
        order_id = order_placement.book_order("Sell", 1)
        send_stop_loss_email(closing_price)
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
        order_id = order_placement.book_order("Buy", 1)
        send_target_profit_email(closing_price)
    elif (
        closing_price > global_variables.target_profit_level
        and global_variables.decision_maker == "Sell"
    ):
        log.debug(
            f"Target Profit level is much lower than current closing price. So taking decision of selling"
            f" existing trade to minimize loss."
        )
        order_id = order_placement.book_order("Sell", 1)
        send_target_profit_email(closing_price)
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
        update_profit_margin_and_stop_loss(closing_price)
