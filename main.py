import hashlib
from validators.text import greater_than
from helpers.connection_db import MongoConnector
from helpers.users import User

STRING_CONNECTOR = "mongodb://127.0.0.1/console_app_notes"

DB_CONNECTOR = MongoConnector(STRING_CONNECTOR)

DB = DB_CONNECTOR.connect()

USER = User(DB["users"])

print("Hey there what you wanna do?")
action = input("Log in (L) or Sign up (S): ").lower().strip()
attempting = True

if action == "s":

    while attempting:

        print("Great respond this question to create your new account")
        name = input("1/3; Enter your name: ")
        last_name = input("2/3; Enter your last name: ")
        passw = input("3/3; Enter your password: ")
        if not(greater_than(passw, 8)):
            print("password must be at least 8 characters")
            continue

        user = {
            "name": name,
            "last_name": last_name,
            "passw": hashlib.sha256(passw.encode()).hexdigest()
        }

        attempting = USER.sign_up(user)