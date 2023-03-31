import hashlib
import os
from dotenv import load_dotenv
import pandas as pd
import keyboard as kb
import re
from datetime import datetime
from validators.text import greater_than
from helpers.connection_db import MongoConnector
from helpers.users import User
from helpers.notes import Note

load_dotenv()

STRING_CONNECTOR = os.getenv("MONGO_URI")

DB_CONNECTOR = MongoConnector(STRING_CONNECTOR)

DB = DB_CONNECTOR.connect()

USER = User(DB["users"])
NOTE = Note(DB["notes"])


print("Hey there what you wanna do? (press `ctrl+*` to speak and say something like: 'I wanna log in' or 'sign up')")

attempting = True
session = False

def listen_to_select_action():
    reg_exp = USER.ask_for_user_action()
    if(reg_exp):
        kb.write(reg_exp.group())
        kb.press("enter")
    else:
        print("Please try something like 'log in' or 'sign up'")

select_action_hotkey = kb.add_hotkey("ctrl+*", lambda: listen_to_select_action())

action = input(">>> Log in (L) or Sign up (S): ").lower().strip()


kb.remove_hotkey(select_action_hotkey)

def write_note_transcription():
    transcription = NOTE.ask_for_create_note()
    kb.write(transcription)

note_creation_hoykey = kb.add_hotkey("ctrl+*", lambda: write_note_transcription())

if action == "s" or re.search("sign\s?up", action):
    while attempting:

        print("Great respond this questions to create your new account")
        name = input(">>> 1/3; Enter your name: ").strip()
        last_name = input(">>> 2/3; Enter your last name: ").strip()
        passw = input(">>> 3/3; Enter your password: ")

        if not(greater_than(passw, 8)):
            print("password must be at least 8 characters")
            continue

        user = {
            "name": name,
            "last_name": last_name,
            "passw": hashlib.sha256(passw.encode()).hexdigest()
        }
        attempting = USER.sign_up(user)

elif action == "l" or re.search("log\s?in", action):
        while attempting:
            print("Ok please enter your name and your password")
            session_user = None
            name = input(">>> Enter your name: ").strip()
            passw = input(">>> Enter your password: ")
            user = {
                "name": name,
                "passw": hashlib.sha256(passw.encode()).hexdigest()
            }
            session = USER.log_in(user, DB["users"])
            if session["session"]:
                attempting = False
                session_user = session["user"]
            else:
                continue
            while session:
                print("Session active !!!!!!!!!!")
                print("You can create a new note (C), delete a note (D), update (U), or review all your notes (R); Press (L) to log out")
                session_action = input(">>> What you wanna do? ").lower().strip()

                #* Create note
                if session_action == "c":
                    print("Ok field the form and you get it")
                    print("You can press ctrl+* to speak, but press enter when your transcription gets writed in to continue")
                    note = {
                        "author": session_user["_id"],
                        "title": input(">>> 1/2; Enter your title: "),
                        "description": input(">>> 2/2; Enter what you gonna do: "),
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                    }
                    NOTE.create_note(note)

                #* Delete note
                elif session_action == "d":

                    print("You can press ctrl+* to speak, but press enter when your transcription gets writed in to continue")
                    note_name = input(">>> What is the name of the note to delete: ")
                    confirm = input(">>> Are you sure you want to delete this note? Y/N: ").lower().strip()
                    if confirm == "y":
                        NOTE.delete_note({"title": note_name, "author": session_user["_id"] })
                    else:
                        print("Your note has not been deleted")

                #* Get notes
                elif session_action == "r":
                    print("****Here you got your notes****")
                    notes = NOTE.get_notes(DB["users"], session_user["_id"])

                    for note in notes:
                        table = pd.DataFrame({
                                "Title": [note["title"]],
                                "Description": [note["description"]]
                            })
                        print(table)
                        print("\n")

                #* Update note
                elif session_action == "u":
                    print("You can press ctrl+* to speak, but press enter when your transcription gets writed in to continue")
                    print("****Press enter in any field that you dont want to change****")
                    note = input(">>> Which note do you want to update? (write the title) ")
                    new_note = {
                        "title": input("1/2; Type the new title: "),
                        "description": input("2/2; Type the new description: "),
                        "updated_at": datetime.now()
                    }
                    NOTE.update_note({"title": note, "author": session_user["_id"] }, new_note)

                elif session_action == "l":
                    confirm = input(">>> Are you sure you want to leave? Y/N ").lower().strip()
                    if(confirm == "y"):
                        session = False
                        print("See you later")
else:
    print("THIS OPTION DOES NOT EXIST")
