def noteEntity(item) -> dict:
    return{
        "_id" : str(item["_id"]),
        "title" : item["title"],
        "description":item["description"],
        "important":item["important"],
    }

def notesEntity(items) -> list:
    return[noteEntity(item) for item in items]