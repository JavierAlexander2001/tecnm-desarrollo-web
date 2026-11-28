
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="Biblioteca API",
    description="Mock API RESTful de libros - Hito 1",
    version="0.1.0"
)


class Libro(BaseModel):
    titulo: str = Field(min_length=1)
    anio: int = Field(ge=1500)


libros_db = {}
siguiente_id = 1


@app.get("/api/libros")
def listar_libros():
    return {"libros": list(libros_db.values())}


@app.post("/api/libros", status_code=201)
def crear_libro(libro: Libro):
    global siguiente_id

    nuevo_libro = {
        "id": siguiente_id,
        "titulo": libro.titulo,
        "anio": libro.anio
    }

    libros_db[siguiente_id] = nuevo_libro
    siguiente_id += 1

    return nuevo_libro

@app.get("/api/libros/{libro_id}")
def consultar_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    return libros_db[libro_id]


@app.put("/api/libros/{libro_id}")
def actualizar_libro(libro_id: int, libro: Libro):
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    libros_db[libro_id] = {
        "id": libro_id,
        "titulo": libro.titulo,
        "anio": libro.anio
    }

    return libros_db[libro_id]


@app.delete("/api/libros/{libro_id}", status_code=204)
def eliminar_libro(libro_id: int):
    if libro_id not in libros_db:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    del libros_db[libro_id]
    return Response(status_code=204)

