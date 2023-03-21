from validators.text import greater_than

class User:

    def __init__(self, db_collection):
        self.collection = db_collection

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

    def log_in(self, user):
        pass