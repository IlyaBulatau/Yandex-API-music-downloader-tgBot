from yoomoney import Client, Quickpay
from config import config


class Payment:

    def __init__(self):
        self.client = Client(token=config.YOOMONEY_TOKEN)

    def get_payments_url(self, sum_, label):
        quickpay = Quickpay(receiver=config.YOOMONEY_ID, 
                            quickpay_form='coin', 
                            targets='buy coins', 
                            paymentType='PC', sum=sum_, 
                            successURL=config.BOT_URL, 
                            label=label)
        
        return quickpay.base_url

    def is_succssesful_payment(self, label_payment):
        ...


payment = Payment()