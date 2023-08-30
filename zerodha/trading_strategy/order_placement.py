import global_variables
from zerodha.util import send_email as email

log = global_variables.log


def send_mail_after_placing_order(crossover, order_id):
    gmail_message = (
        f"At {crossover[1]} time we placed one {crossover[6]} order for {crossover[3]} closing price. \n\n"
        f" More details-> \n 1. Order Id = {order_id},\n 2. Decision for this Trade= {crossover[6]},\n 8. "
        f"Decision for previous trade= {global_variables.decision_maker}. \n Take necessary action if you think the decision "
        f"is wrong. \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=log,
        subject=f"AlgoTrading - New Order - {order_id} Placed ALERT!!",
        message=gmail_message,
    )

    log.info(
        f"Order Gmail is sent after {crossover[6]}ing a new trade for {crossover[3]} closing price."
    )


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


def book_order(order_type, quantity):
    kite = global_variables.kite

    transaction_type = (
        kite.TRANSACTION_TYPE_BUY if order_type == "Buy" else kite.TRANSACTION_TYPE_SELL
    )

    """order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        tradingsymbol=global_variables.trading_symbol,
        exchange=kite.EXCHANGE_NSE,
        transaction_type=transaction_type,
        quantity=quantity,
        order_type=kite.ORDER_TYPE_MARKET,
        product=kite.PRODUCT_CNC,
        validity=kite.VALIDITY_DAY,
    )"""
    global_variables.cross_over_order_placed = True
    global_variables.order_id = (
        global_variables.order_id + 1
    )  # these two lines needs to be removed when
    order_id = global_variables.order_id  # we will place real order

    log.info(
        f'{quantity} order/s placed for "{order_id}" order id and transaction_type = {transaction_type}.'
    )

    return order_id


def place_order(crossover):
    log.info(
        f"Before executing Place_Order old values are, 1. Decision maker= {global_variables.decision_maker}, "
        f"2. Crossover Decision= {crossover[6]}, 3. Trade Entry Price= {global_variables.trade_entry_price}, "
        f"4.Stop Loss Level= {global_variables.stop_loss_level}, 5. Target profit Loss= {global_variables.target_profit_level}"
    )

    # One Buy and Sell at al time
    if crossover[6] == "Buy" and global_variables.decision_maker in ("", "Buy"):
        if global_variables.decision_maker == "":
            order_id = book_order(crossover[6], 1)
        else:
            order_id = book_order(crossover[6], 2)

        send_mail_after_placing_order(crossover, order_id)

        global_variables.decision_maker = "Sell"
        global_variables.trade_entry_price = crossover[3]
        update_profit_margin_and_stop_loss(crossover[3])

    elif crossover[6] == "Sell" and global_variables.decision_maker in ("", "Sell"):
        if global_variables.decision_maker == "":
            order_id = book_order(crossover[6], 1)
        else:
            order_id = book_order(crossover[6], 2)

        send_mail_after_placing_order(crossover, order_id)

        global_variables.decision_maker = "Buy"
        global_variables.trade_entry_price = crossover[3]
        update_profit_margin_and_stop_loss(crossover[3])

    log.info(
        f"After executing Place_Order new values are, 1. Decision maker= {global_variables.decision_maker}, "
        f"2. Trade Entry Price= {global_variables.trade_entry_price}, 3.Stop Loss Level= "
        f"{global_variables.stop_loss_level}, 4. Target profit Loss= {global_variables.target_profit_level}"
    )
