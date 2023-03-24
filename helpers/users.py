from validators.text import greater_than
from .recognizer import Recognizer
import re


class User:

    def __init__(self, db_collection):
        self.collection = db_collection
        self.RECOGNIZER = Recognizer()

    def ask_for_user_action(self):
        try:

            transcription = self.RECOGNIZER.recognize()
            re_match = re.search("sign\s?up", transcription) or re.search("log\s?in", transcription)
            return re_match

        except Exception:
            print("Error try again")

    def sign_up(self, user):
        if not(greater_than(user["name"], 1)) or not(greater_than(user["last_name"], 1)):
            print("Hey you got a error please verify each field \n the name and last name must be longer than 1")
            return True
        else:
            try:
                self.collection.insert_one(user)
                print("Your user has been created successfully")
                return False
            except Exception as error:
                print(error)
                print("Oh no something went wrong try again")

    def log_in(self, user, user_collection):
        query_user = user_collection.find_one({"name": user["name"]})
        if not query_user:
            print("**********Sorry we could not find the user try again**********")
            return { "session": False }
        validate = query_user["passw"] == user["passw"]
        if not validate:
            print("**********Your password does not match**********")
            return { "session": validate }
        return { "session": validate, "user":query_user }