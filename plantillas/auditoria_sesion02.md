# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Enrutamiento manual por verbo HTTP  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | FastAPI 0.110+ (Python 3.10+) o PHP 8.2 con servidor embebido |
| **Rol (R)** | Arquitecto de software senior especialista en APIs RESTful y Seguridad Web |
| **Especificación (E)** | Especificación semántica de verbos e idempotencia |
| **Output (O)** | Solo código modular, esquemas Pydantic/DTO y códigos HTTP semánticos |

### 2.2 Prompt Estructurado
```text
Necesito crear una API de libros utilizando Python y FastAPI. Debe permitir registrar libros con POST, consultar con GET, actualizar con PUT y eliminar con DELETE. Los libros deben guardarse en memoria, sin utilizar una base de datos. La API debe responder con los códigos HTTP correctos, incluyendo 404 cuando un libro no existe y 405 cuando se utiliza un método no permitido. Genera el código completo de app.py y asegúrate de cumplir los ocho casos de prueba de la actividad.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="CRUD de libros")

# Modelo para recibir los datos de un libro
class LibroEntrada(BaseModel):
    titulo: str
    anio: int

# Almacenamiento temporal
libros = {}
siguiente_id = 1


# GET: consultar todos los libros
@app.get("/api/libros")
def listar_libros():
    return {"libros": list(libros.values())}


# POST: registrar un libro
@app.post("/api/libros", status_code=201)
def crear_libro(datos: LibroEntrada):
    global siguiente_id

    libro = {
        "id": siguiente_id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }

    libros[siguiente_id] = libro
    siguiente_id += 1

    return libro


# GET: consultar un libro por su ID
@app.get("/api/libros/{id}")
def obtener_libro(id: int):
    if id not in libros:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    return libros[id]


# PUT: reemplazar la información de un libro
@app.put("/api/libros/{id}")
def actualizar_libro(id: int, datos: LibroEntrada):
    if id not in libros:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    libros[id] = {
        "id": id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }

    return libros[id]


# DELETE: eliminar un libro
@app.delete("/api/libros/{id}", status_code=204)
def eliminar_libro(id: int):
    if id not in libros:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    del libros[id]
    return None# Código devuelto por el LLM
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de métodos no permitidos (HTTP 405)

* [X] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [X] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [X] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La verificación permite comprobar que los errores 404 y 405 se manejen correctamente. Utilicé HTTPException para los libros inexistentes y dejé que FastAPI respondiera automáticamente con 405 cuando se utiliza PATCH.

---
**Firma digital:** [Javier Alexander2001]
