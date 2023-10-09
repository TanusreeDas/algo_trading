import global_variables
from zerodha.util import send_email as email

log = global_variables.log
kite = global_variables.kite

def send_order_placement_email_stop_level_crossed(type, order_id):
    current_order_decision = global_variables.decision_maker
    if current_order_decision == "":
        previous_order_decision = "None"
    elif current_order_decision == "Sell":
        previous_order_decision = "Buy"
    else:
        previous_order_decision = "Sell"

    current_closing_price = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]
    gmail_message = (
        f"""
        Dear Client,<br><br>
    
        We are writing to inform you that a {type} breach has occurred in your trading account, involving a closing price of {current_closing_price}.<br><br>
    
        To address this situation, we have taken the following action:
        <ol>
            <li><b>Action:</b> Place a new trade order</li>
            <li><b>Order Id:</b> {order_id}</li>
            <li><b>Decision for this Trade:</b> {current_order_decision}</li>
            <li><b>Decision for previous trade:</b> {previous_order_decision}</li>
        </ol>

        Your satisfaction and success in trading are our top priorities. If you have any questions or concerns about this decision, please feel free to reach out to us. We're here to assist you.<br><br>

        Thank you for choosing TradingMantra.<br><br>

        Warm Regards,<br>
        TradingMantra Support Team<br>
        """
 )
    disclaimer = "<b>Disclaimer:</b> Please note that closing prices may slightly vary due to the timing of order placement."
    full_gmail_message = gmail_message + "<br><br>" + disclaimer
    email.send_gmail(
        log=log,
        subject=f"AlgoTrading - New Order - {order_id} Placed ALERT!!",
        message=full_gmail_message,
    )


def send_mail_after_placing_order(crossover, order_id):
    current_order_decision = global_variables.decision_maker
    if current_order_decision == "":
        previous_order_decision = "None"
    elif current_order_decision == "Sell":
        previous_order_decision = "Buy"
    else:
        previous_order_decision = "Sell"

    if crossover:
        gmail_message = (
            f"""
            Dear Client,<br><br>

            At {crossover[1]}, we took action to optimize your trading account. We placed a {crossover[6]} order for a closing price of {crossover[3]}.<br><br>

            Here are the details:
            <ol>
                <li><b>Order Id:</b> {order_id}</li>
                <li><b>Decision for this Trade:</b> {crossover[6]}</li>
                <li><b>Decision for previous trade:</b> {previous_order_decision}</li>
            </ol>
            
            Your satisfaction and success in trading are our top priorities. If you have any questions or concerns about this decision, please feel free to reach out to us. We're here to assist you.<br><br>

            Thank you for choosing TradingMantra.<br><br>

            Warm Regards,<br>
            TradingMantra Support Team<br>
            """
        )
    else:
        current_closing_price = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]

        gmail_message = (
            f"""
            Dear Client,<br><br>

            At the end of the trading day, we have closed all open trades as part of our standard procedure. Currently, one trade was open, and we have taken action by placing a complementary trade for a closing price of {current_closing_price}.<br><br>

            Here are the details:
            <ol>
                <li><b>Order Id:</b> {order_id}</li>
                <li><b>Decision for this Trade:</b> {current_order_decision}</li>
                <li><b>Decision for previous trade:</b> {previous_order_decision}</li>
            </ol>

            If you have any questions or concerns regarding this action, please don't hesitate to contact us. We value your peace of mind and are here to provide any assistance you may need.<br><br>

            Thank you for choosing TradingMantra.<br><br>
            
            Warm Regards,<br>
            TradingMantra Support Team<br>
            """
        )

    disclaimer = "<b>Disclaimer:</b> Please note that closing prices may slightly vary due to the timing of order placement."
    full_gmail_message = gmail_message + "<br><br>" + disclaimer
    email.send_gmail(
        log=log,
        subject=f"AlgoTrading - New Order - {order_id} Placed ALERT!!",
        message=full_gmail_message,
    )
    if crossover:
        log.info(
            f"Order Gmail is sent after {crossover[6]}ing a new trade for {crossover[3]} closing price."
        )


def update_profit_margin_and_stop_loss(ltp):
    current_stop_loss_level = global_variables.stop_loss_level
    current_target_profit_level = global_variables.target_profit_level
    stpt_threshold = global_variables.stpt_threshold
    existing_trade_type = "Buy" if global_variables.decision_maker == "Sell" else "Sell"

    if existing_trade_type == "Buy":
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
    elif existing_trade_type == "Sell":
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
        f"Trailing Target profit level and Stop Loss levels have been modified. 1. Trade_entry_price = "
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
        f'{quantity} order(s) placed for "{order_id}" order id and transaction_type = {transaction_type}.'
    )

    return order_id


def place_cross_over_order(crossover):
    log.info(
        f"Before executing place_cross_over_order old values are, 1. Decision maker= {global_variables.decision_maker}, "
        f"2. Crossover Decision= {crossover[6]}, 3. Trade Entry Price= {global_variables.trade_entry_price}, "
        f"4.Stop Loss Level= {global_variables.stop_loss_level}, 5. Target profit Loss= {global_variables.target_profit_level}"
    )

    # One Buy and Sell at al time
    if crossover[6] == "Buy" and global_variables.decision_maker in ("", "Buy"):
        if global_variables.decision_maker == "":
            order_id = book_order(crossover[6], 1)
        else:
            order_id = book_order(crossover[6], 2)

        global_variables.trade_entry_price = crossover[3]
        send_mail_after_placing_order(crossover, order_id)

        global_variables.decision_maker = "Sell"
        update_profit_margin_and_stop_loss(crossover[3])

    elif crossover[6] == "Sell" and global_variables.decision_maker in ("", "Sell"):
        if global_variables.decision_maker == "":
            order_id = book_order(crossover[6], 1)
        else:
            order_id = book_order(crossover[6], 2)

        global_variables.trade_entry_price = crossover[3]
        send_mail_after_placing_order(crossover, order_id)

        global_variables.decision_maker = "Buy"
        update_profit_margin_and_stop_loss(crossover[3])

    log.info(
        f"After executing place_cross_over_order new values are, 1. Decision maker= {global_variables.decision_maker}, "
        f"2. Trade Entry Price= {global_variables.trade_entry_price}, 3.Stop Loss Level= "
        f"{global_variables.stop_loss_level}, 4. Target profit Loss= {global_variables.target_profit_level}"
    )
