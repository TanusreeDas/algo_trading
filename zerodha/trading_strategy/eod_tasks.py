import global_variables
import order_placement
from zerodha.util import send_email as email, date

log = global_variables.log
kite = global_variables.kite
decision_maker = global_variables.decision_maker
to_date = date.get_current_day()


def eod_send_email(order_id=""):
    if order_id != "":
        gmail_message = (
            f"Market is Closed for the Day. We closed all open trades by placing a {decision_maker} order."
            f"Order id = {order_id}. Have a nice day. \n\n\n Thanks and Regards,\n TradingMantra"
        )
    else:
        gmail_message = (
            f"Market is Closed for the Day. We did not have any open trade. Have a "
            f"nice day. \n\n\n Thanks and Regards,\n TradingMantra"
        )
    email.send_gmail(log=log, subject=f"EOD Mail- {to_date}", message=gmail_message)
    log.debug(f"EOD email sent for {to_date}")


def close_all_trades():
    if decision_maker != "":
        log.info(f"EOD we need to close trade by placing {decision_maker} trade.")
        order_id = order_placement.book_order(decision_maker, 1)
        eod_send_email(order_id)
    else:
        log.info("Nothing to Close")
        eod_send_email()
