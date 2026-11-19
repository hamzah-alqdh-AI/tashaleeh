from fastapi import FastAPI

app = FastAPI()

@app.get("/parts")
def list_parts():
    parts = ["كشاف يمين", "باب أمامي يسار", "قير أوتوماتيك"]
    return parts

@app.get("/makes")
def list_makes():
    makes = ["toyota", "hyundai", "honda"]
    return makes