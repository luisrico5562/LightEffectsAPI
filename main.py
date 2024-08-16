from fastapi import FastAPI, Query, UploadFile
from fastapi.responses import FileResponse
from typing import Optional
from filters import filterFunction
import cv2 as cv
import os

app = FastAPI()

@app.post("/upload-photo")
async def uploadFile(file: UploadFile):
    try:
        file_path = f"originals/{file.filename}" 
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        return {"message": "File saved successfully"}
    except Exception as e:
        return {"message": e.args}


@app.get('/get-edited-photo')
async def getEditedPhoto(fileName : str):
    editedFilePath = "edits/" + fileName
    return FileResponse(editedFilePath)


@app.get('/get-edits-list')
def getEditsList():
    return os.listdir('edits/')


@app.get('/get-originals-list')
def getOriginalsList():
    return os.listdir('originals/')


@app.put('/edit-photo')
async def editPhoto(
    fileName : str,
    bri : Optional[int] = Query(0, ge = -100, le = 100),
    con : Optional[int] = Query(0, ge = -100, le = 100),
    sat : Optional[int] = Query(0, ge = -100, le = 100),
    sha : Optional[int] = Query(0, ge = -100, le = 100),
    r : Optional[int] = Query(0, ge = -100, le = 100),
    g : Optional[int] = Query(0, ge = -100, le = 100),
    b : Optional[int] = Query(0, ge = -100, le = 100)):
    
    try:
        filePath = "originals/" + fileName
        image = cv.imread(filePath)

        if (bri != 0): image = filterFunction(image, 'brightness', bri)
        if (con != 0): image = filterFunction(image, 'contrast', con)
        if (sat != 0): image = filterFunction(image, 'saturation', sat)
        if (sha != 0): image = filterFunction(image, 'sharpness', sha)
        if (r != 0): image = filterFunction(image, 'red', r)
        if (g != 0): image = filterFunction(image, 'green', g)
        if (b != 0): image = filterFunction(image, 'blue', b)
        
        editedFilePath = "edits/" + os.path.splitext(fileName)[0] + '_edited.jpg'    
        cv.imwrite(editedFilePath, image)

        return FileResponse(editedFilePath)
    
    except Exception as e:
        return {"error": e.args}
