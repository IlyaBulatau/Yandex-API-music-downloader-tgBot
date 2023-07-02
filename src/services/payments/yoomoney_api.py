from yoomoney import Client, Quickpay, OperationDetails
from config import config
from logger.logger import logger


class Payment:

    def __init__(self):
        self.client = Client(token=config.YOOMONEY_TOKEN)

    def get_payments_url(self, sum_, label):
        try:
            quickpay = Quickpay(receiver=config.YOOMONEY_ID, 
                                quickpay_form='button', 
                                targets='donat', 
                                paymentType='PC', 
                                sum=sum_, 
                                successURL=config.BOT_URL, 
                                label=label)

            return quickpay.base_url
        except Exception as e:
            logger.critical(f'EXCEPTION QUICKPAY OPERATIONS {e}')

    def is_succssesful_payment(self, label_payment):
        verification = self.client.operation_history(label=label_payment)
        for operation in verification.operations:
            if operation.status == 'success':
                return operation.amount
        return False


payment = Payment()