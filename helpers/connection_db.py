from pymongo import MongoClient

class MongoConnector:
    def __init__(self, string_connector):
        self.string_connector = string_connector

    def connect(self):
        try:
            db = MongoClient(self.string_connector)
            return db["terminal-app-notes"] #or console_app_notes for development
        except Exception:
            print("Error trying to connect to Mongodb")
