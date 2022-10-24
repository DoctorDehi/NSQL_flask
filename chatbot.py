from chatterbot import ChatBot
from NewSQLStorageAdapter import SQLStorageAdapter


bot = ChatBot(
    "Norman",
    storage_adapter='NewSQLStorageAdapter.SQLStorageAdapter',
    database_uri='sqlite:///chatbot.sqlite3'
)

