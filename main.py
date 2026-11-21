from fastapi import FastAPI
from database import fetch_all_makes

app = FastAPI()

@app.get("/parts")
def list_parts():
    parts = ["كشاف يمين", "باب أمامي يسار", "قير أوتوماتيك"]
    return parts

@app.get("/makes")
def list_makes():
    return fetch_all_makes()