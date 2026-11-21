from fastapi import FastAPI
from database import fetch_all_makes
from database import fetch_all_makes, fetch_models_by_make

app = FastAPI()

@app.get("/parts")
def list_parts():
    parts = ["كشاف يمين", "باب أمامي يسار", "قير أوتوماتيك"]
    return parts

@app.get("/makes")
def list_makes():
    return fetch_all_makes()

@app.get("/models")
def list_models(make_id: int):
    return fetch_models_by_make(make_id)