from py.client import Client
from py.config import url, TOKEN

client = Client(base_url=url, headers={'X-API-Key': TOKEN if TOKEN else 'no token'})
