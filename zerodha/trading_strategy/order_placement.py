import global_variables
from zerodha.util import send_email as email


def send_mail_after_placing_order(crossover, order_id):
    gmail_message = (
        f"At {crossover[1]} time we placed one {crossover[6]} order for {crossover[3]} closing price. \n\n"
        f" More details-> \n 1. Order Id = {order_id},\n 2. Decision for this Trade= {crossover[6]},\n 8. "
        f"Decision for previous trade= {global_variables.decision_maker}. \n Take necessary action if you think the decision "
        f"is wrong. \n\n\n Thanks and Regards,\n TradingMantra"
    )
    email.send_gmail(
        log=global_variables.log,
        subject=f"AlgoTrading - New Order - {order_id} Placed ALERT!!",
        message=gmail_message,
    )

    global_variables.log.info(
        f"Order Gmail is sent after {crossover[6]}ing a new trade for {crossover[3]} closing price."
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
    global_variables.order_id = (
        global_variables.order_id + 1
    )  # these two lines needs to be removed when
    order_id = global_variables.order_id  # we will place real order

    global_variables.log.info(
        f'{quantity} order/s placed for "{order_id}" order id and transaction_type = {transaction_type}.'
    )

    return order_id


def place_order(crossover):
    global_variables.log.debug(
        f"In Place_Order function-> 1. Decision maker= {global_variables.decision_maker}, 2. Crossover Decision= {crossover[6]}"
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
        global_variables.stop_loss_level = (
            global_variables.trade_entry_price - global_variables.trailing_stop_loss
        )
        global_variables.target_profit_level = (
            global_variables.trade_entry_price + global_variables.trailing_profit_target
        )

    elif crossover[6] == "Sell" and global_variables.decision_maker in ("", "Sell"):
        if global_variables.decision_maker == "":
            order_id = book_order(crossover[6], 1)
        else:
            order_id = book_order(crossover[6], 2)

        send_mail_after_placing_order(crossover, order_id)

        global_variables.decision_maker = "Buy"
        global_variables.trade_entry_price = crossover[3]
        global_variables.stop_loss_level = (
            global_variables.trade_entry_price + global_variables.trailing_stop_loss
        )
        global_variables.target_profit_level = (
            global_variables.trade_entry_price - global_variables.trailing_profit_target
        )

    global_variables.log.info(
        f"After executing Place_Order new values are, 1. Decision maker= {global_variables.decision_maker}, 2. "
        f"Trade Entry Price= {global_variables.trade_entry_price}, 3.Stop Loss Level= {global_variables.stop_loss_level}"
    )
