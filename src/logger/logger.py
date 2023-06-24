from logging.handlers import SMTPHandler
import logging

from config import config

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
# Handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(filename='log.log', mode='a', encoding='utf-8')
email_handler = SMTPHandler(
    mailhost=('smtp.yandex.ru', 587),
    fromaddr=config.EMAIL,
    toaddrs=config.EMAIL,
    subject='MusicBot Logg',
    credentials=(config.EMAIL, config.EMAIL_PASSWORD),
    secure=()
)

#Formatter
formatter = logging.Formatter(fmt='{levelname} | {asctime} | {message}', style='{')

#Set level
stream_handler.setLevel('DEBUG')
file_handler.setLevel('DEBUG')
email_handler.setLevel('WARNING')

#Set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
email_handler.setFormatter(formatter)

#Add handlers
logger.addHandler(stream_handler)
logger.addHandler(file_handler)
logger.addHandler(email_handler)