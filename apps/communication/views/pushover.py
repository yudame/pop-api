import logging
from abc import ABC
from apps.common.utilities.multithreading import start_new_thread

from pushover import init, Client
from settings import PUSHOVER_API_TOKEN, PUSHOVER_USER_KEY

init(PUSHOVER_API_TOKEN)


class Pushover(ABC):

    def __init__(self):
        self.client = Client(PUSHOVER_USER_KEY)

    @start_new_thread
    def send_text(self, text_message: str, title: str="Pop"):
        logging.debug(f"sending text: {text_message}")
        self.client.send_message(text_message, title=title)
