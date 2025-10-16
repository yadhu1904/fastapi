from fastapi import APIRouter
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from models.note import Note
from config.db import conn
from fastapi.templating import Jinja2Templates


note = APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        # Safely extract fields with defaults
        _id = str(doc.get("_id", ""))  # ObjectId -> string for templates
        title = doc.get("title", "")
        # Prefer "description", fall back to "desc", else empty string
        description = doc.get("description", doc.get("desc", ""))
        # Coerce important to bool with default False
        important = bool(doc.get("important", False))

        newDocs.append({
            "id": _id,
            "title": title,
            "description": description,
            "important": important,
        })
    print("rendering docs:", len(newDocs))
        # Optional: log the normalized doc
        # print({"id": _id, "title": title, "description": description, "important": important})

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "newDocs": newDocs}
    )


@note.post("/")
async def create_note(request:Request):
    form = await request.form()
    print(form)
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(formDict)
    return{"success":True}
