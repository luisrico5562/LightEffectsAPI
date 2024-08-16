from fastapi import FastAPI, Query, UploadFile, Request
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
import os

from filters import filterFunction
import cv2 as cv

from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="../templates")

# Cargar index.html
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {'request': request}) 

# Guardar foto en el directorio local /img/originals
@app.post("/upload-photo")
async def uploadFile(file: UploadFile):
    try:
        file_path = f"img/originals/{file.filename}" 
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}

# Recuperar foto editada
@app.get("/get-edited-photo/{fileName}")
async def getEditedPhoto(fileName : str):
    editedFilePath = "img/edits/" + fileName
    try:
        if fileName not in os.listdir("img/edits/"):
            return {"error": "File does not exist."}
        return FileResponse(editedFilePath)
    except Exception as e:
        return {"error": e.args}

# Recibir lista de fotos editadas/modificadas
@app.get("/get-edits-list")
def getEditsList():
    return os.listdir("img/edits/")

# Recibir lista de fotos originales
@app.get("/get-originals-list")
def getOriginalsList():
    return os.listdir("img/originals/")

# Editar foto
@app.put("/edit-photo/{fileName}")
async def editPhoto(
    fileName : str,
    bri : Optional[int] = Query(0, ge = -100, le = 100),
    con : Optional[int] = Query(0, ge = -100, le = 100),
    sat : Optional[int] = Query(0, ge = -100, le = 100),
    sha : Optional[int] = Query(0, ge = -100, le = 100),
    r : Optional[int] = Query(0, ge = -100, le = 100),
    g : Optional[int] = Query(0, ge = -100, le = 100),
    b : Optional[int] = Query(0, ge = -100, le = 100)):
    
    # Se revisa si el archivo existe en el directorio local /img/originals
    if fileName not in os.listdir("img/originals/"):
        return {"error": "File does not exist."}
    
    try:
        filePath = "img/originals/" + fileName
        image = cv.imread(filePath)
        # Se procesa el filtro de los valores modificados (diferentes a 0)
        if (bri != 0): image = filterFunction(image, "brightness", bri)
        if (con != 0): image = filterFunction(image, "contrast", con)
        if (sat != 0): image = filterFunction(image, "saturation", sat)
        if (sha != 0): image = filterFunction(image, "sharpness", sha)
        if (r != 0): image = filterFunction(image, "red", r)
        if (g != 0): image = filterFunction(image, "green", g)
        if (b != 0): image = filterFunction(image, "blue", b)
        
        # Se guarda el resultado en el directorio /img/edits
        editedFilePath = "img/edits/" + os.path.splitext(fileName)[0] + "_edited.jpg"    
        cv.imwrite(editedFilePath, image)

        return FileResponse(editedFilePath)
    
    except Exception as e:
        return {"error": e.args}
