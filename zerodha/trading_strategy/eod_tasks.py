import global_variables
import order_placement
from zerodha.util import send_email as email, date

log = global_variables.log
kite = global_variables.kite


def eod_send_email(order_id=""):
    if order_id != "":
        gmail_message = (
            f"""
            Dear Client,<br><br>

            We would like to inform you that the market has closed for the day. As part of our routine procedures, we have closed all open trades by placing a {global_variables.decision_maker} order. The new order ID is {order_id}.<br><br>

            We hope you had a successful trading day, and we look forward to assisting you in future trades.<br><br>

            Thank you for choosing TradingMantra.<br><br>

            Warm Regards,<br>
            TradingMantra Support Team<br>
            """
        )
    else:
        gmail_message = (
            f"""
            Dear Client,<br><br>
    
            We would like to inform you that the market has closed for the day. We are pleased to report that there were no open trades to manage at market close today.<br><br>
    
            We hope you had a successful day, and we look forward to assisting you in future trades.<br><br>
    
            Thank you for choosing TradingMantra.<br><br>
    
            Warm Regards,<br>
            TradingMantra Support Team<br>
            """
        )
    to_date = date.get_current_day()
    email.send_gmail(log=log, subject=f"EOD Mail- {to_date}", message=gmail_message)
    log.debug(f"EOD email sent for {to_date}")


def close_all_trades():
    log.debug(f"EOD process started, Decision maker= {global_variables.decision_maker}")
    decision_maker = global_variables.decision_maker
    if decision_maker != "":
        log.info(f"EOD we need to close trade by placing {decision_maker} trade.")
        order_id = order_placement.book_order(decision_maker, 1)
        order_placement.send_mail_after_placing_order(None, order_id)
        eod_send_email(order_id)
    else:
        log.info("Nothing to Close")
        eod_send_email()
