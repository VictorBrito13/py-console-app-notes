from validators.text import greater_than

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
        delete_count = self.collection.delete_one({"title": note_name})
        if(delete_count >= 1):
            print("note deleted")
        else:
            print("The note has not been deleted, maybe this is not it name")