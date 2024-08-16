# LightEffectsAPI
LightEffectsAPI es una API de edición de fotografía, capaz de editar distintos aspectos de un archivo JPG. 

Los parámetros de dichos aspectos, al igual que en la mayoría de programas de edición de fotografía, van de -100 a 100, siendo 0 el valor del archivo original, por lo que un valor negativo restaría fuerza al aspecto correspondiente, mientras que un valor positivo la aumentaría.

Los valores (aspectos) que se pueden editar son:
- Iluminación (brightness)
- Contraste (contrast)
- Saturación (saturation)
- Nitidez (sharpness)
- Canales RGB:
  - Rojo (red)
  - Verde (green)
  - Azul (blue)

El archivo encargado de modificar los valores de la imágen es [filters.py](https://github.com/luisrico5562/LightEffectsAPI/blob/main/src/filters.py)

## Requerimientos

El proyecto está hecho en Python con FastAPI, además de utilizar un par de bibliotecas para su funcionamiento:

- [Python](https://www.python.org/) (v3.12.2)
- [FastAPI](https://fastapi.tiangolo.com/tutorial/) (v0.110.0)
- [OpenCV](https://opencv.org/get-started/) (v4.10.0.84)
- [Numpy](https://numpy.org/install/) (v2.0.1)

__Nota__: Para el proyecto se utilizó [Uvicorn](https://www.uvicorn.org/) (v0.27.1) para el servidor local.

## Instrucciones para configurar y ejecutar de forma local

__Nota__: Se requiere tener instalado python 3
1. Crear una copia del repositorio en remoto
2. Instalar cada biblioteca de forma manual o utilizando el arhivo [requirements.txt](https://github.com/luisrico5562/LightEffectsAPI/blob/main/requirements/requirements.txt). Para esto último se utiliza la consola de comandos. Se abre el directorio donde se ubica el archivo (`LightEffectsAPI/requirements`) y se corre el siguiente comando:

   `pip3 install -r requirements.txt`

3. Dentro de la carpeta `LightEffectsAPI/src` correr el siguiente comando:

    `uvicorn main:app --reload`
   
## Endpoints

### Subir foto

POST `/upload-photo`

Permite subir un archivo al directorio local (src/originals)

### Lista de edits

GET `/get-edits-list`

Retorna la lista de fotos editadas (del directorio src/edits)

### Lista de originales

GET `/get-originals-list`

Retorna la lista de fotos sin editar (del directorio src/originals)

### Foto editada
GET `/get-edited-foto/:fileName`

Retorna la foto editada

Parámetro Path:

- __fileName__ - String - _Required_

### Editar foto

PUT `/edit-photo/{fileName}`

Permite editar una foto a partir de una original.

Parámetro Path:

- __fileName__ - String - _Required_

Parámetros Query:

- __bri__ (brillo) - Integer
- __con__ (contraste) - Integer
- __sat__ (saturación) - Integer
- __sha__ (nitidez) - Integer
- __r__ (canal rojo) - Integer
- __g__ (canal verde) - Integer
- __b__ (canal azul) - Integer

__Nota__: los rangos de los parámetros query van de -100 a 100, siendo 0 su valor por defecto (cambio nulo)
