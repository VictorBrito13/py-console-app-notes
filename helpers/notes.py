from validators.text import greater_than
from .recognizer import Recognizer
import copy

class Note:
    def __init__(self, collection):
        self.collection = collection
        self.RECOGNIZER = Recognizer()

    def ask_for_create_note(self):
        transcription = self.RECOGNIZER.recognize()
        return transcription

    def create_note(self, note):
        try:
            if not(greater_than(note["title"], 1)) or not(greater_than(note["description"], 1)):
                print("The title and description note must be at least 1 or longer")
                return False
            self.collection.insert_one(note)
            print("Note added successfully")
        except Exception as error:
            print(error)
            print("Oh a error has ocurred try again")

    def delete_note(self, filter):
        try:
            result = self.collection.delete_one(filter)
            if(result.deleted_count >= 1):
                print("note deleted")
            else:
                print("The note has not been deleted, maybe this is not it name")
        except Exception as error:
            print("Oh a error has ocurred try again")
            print(error)

    def get_notes(self, user_collection, user_id):
        try:
            #Devuelve TODOS los usuarios con sus notas
            users = user_collection.aggregate([{ "$lookup": { "from": "notes", "localField": "_id", "foreignField": "author", "as": "notes" } }])
            #Buscamos un usuarion en especifico
            for user in users:
                if user["_id"] == user_id:
                    return user["notes"]
        except Exception:
            print("we have a problem try again")

    def update_note(self, filter, new_note):
        try:
            new_note_copy = copy.deepcopy(new_note)
            for key in new_note:
                if new_note[key] == "": del new_note_copy[key]

            print(new_note_copy)
            result = self.collection.update_one(filter, { "$set": new_note_copy }, upsert=False)
            print(f"we have modified {result.modified_count} note")

        except Exception as error:
            print("Error check the title of your note")
            print(error)
