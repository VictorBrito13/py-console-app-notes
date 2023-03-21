from pymongo import MongoClient

class MongoConnector:
    def __init__(self, string_connector):
        self.string_connector = string_connector

    def connect(self):
        db = MongoClient(self.string_connector)
        return db["console_app_notes"]
