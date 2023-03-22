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
session = False

if action == "s":

    while attempting:

        print("Great respond this questions to create your new account")
        name = input("1/3; Enter your name: ").strip()
        last_name = input("2/3; Enter your last name: ").strip()
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

elif action == "l":
        while attempting:
            print("Ok please enter your name and your password")
            name = input("Enter your name: ").strip()
            passw = input("Enter your password: ")
            user = {
                "name": name,
                "passw": hashlib.sha256(passw.encode()).hexdigest()
            }
            session = USER.log_in(user, DB["users"])
            if session:
                attempting = False
            while session:
                print("Session active !!!!!!!!!!")
                print("You can create a new note (C), delete a note (D), update (U), or review all your notes (R); Press (L) to log out")
                session_action = input("What you wanna do? ")
