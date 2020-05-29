from trello import TrelloClient
from static.image.qr import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_TOKEN

client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN  # , token_secret='your-oauth-token-secret'
)
