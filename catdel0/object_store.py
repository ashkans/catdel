from replit.object_storage import Client
from catdel.state_manager import StateManager

sm = StateManager.get_instance()


def upload_from_bytes(file):
    client = Client()
    client.upload_from_bytes("file.png", file)
    
