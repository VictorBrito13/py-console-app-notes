from validators.text import greater_than
import copy

class Note:
    def __init__(self, collection):
        self.collection = collection

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

    def delete_note(self, note_name):
        try:
            delete_count = self.collection.delete_one({"title": note_name})
            if(delete_count >= 1):
                print("note deleted")
            else:
                print("The note has not been deleted, maybe this is not it name")
        except Exception:
            print("Oh a error has ocurred try again")

    def get_notes(self, user_collection, user_id):
        try:
            users = user_collection.aggregate([{ "$lookup": { "from": "notes", "localField": "_id", "foreignField": "author", "as": "notes" } }])
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
