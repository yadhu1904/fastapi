from fastapi import APIRouter
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from models.note import Note
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity,notesEntity

note = APIRouter()

templates = Jinja2Templates(directory="templates")

@note.get("/",response_class=HTMLResponse)
async def read_root(request: Request):
    docs = conn.notes.notes.find({ })
    newDocs = []
    for doc in docs:
        newDocs.append({
            "id":doc["_id"],
            "title": doc["title"],
            "description":doc["description"],
            "important":doc["important"],
        })
        print(doc)
    return templates.TemplateResponse("index.html", {"request": request,"newDocs":newDocs})

@note.post("/")
async def create_note(request:Request):
    form = await request.form()
    print(form)
    formDict = dict(form)
    if formDict["important"] == "on":
        formDict["important"] = True
    else:
        formDict["important"] = False
    note = conn.notes.notes.insert_one(formDict)
    return{"success":True}