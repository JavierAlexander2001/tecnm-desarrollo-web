# Bitácora de Requerimientos y Auditoría IA — Sesión 08
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Respuestas Semánticas y Excepciones HTTP Personalizadas  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lanzamiento manual de excepciones estructuradas  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> Al realizar mi código tuve dificultades para controlar los errores cuando se consultaba un libro que no existía y cuando se enviaban datos incorrectos. También me costó mantener el mismo formato en las respuestas de error, porque FastAPI mostraba sus propios mensajes.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python con FastAPI y Pydantic, trabajando en Google Colab. |
| **Rol (R)** | Desarrollador de software especializado en APIs REST y manejo de errores HTTP. |
| **Especificación (E)** | Crear excepciones personalizadas para libros inexistentes y un manejador global para errores de validación. Las respuestas deben utilizar códigos HTTP 200, 201, 404 y 422. |
| **Output (O)** | Código completo en Python para app.py, con rutas para consultar y registrar libros, validaciones y respuestas de error en formato JSON. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador especializado en Python y FastAPI.

Necesito implementar un manejo de errores para una API de libros.

Requisitos:

1. Crear una excepción personalizada llamada LibroNoEncontrado.
2. Registrar un manejador que responda con HTTP 404.
3. El error 404 debe tener el código NO_ENCONTRADO.
4. Los errores de validación deben responder con HTTP 422 y el código VALIDACION.
5. Rechazar los títulos vacíos.
6. Iniciar la API con el libro 1 llamado Rayuela.
7. GET /api/libros/1 debe responder 200.
8. GET /api/libros/99 debe responder 404.
9. POST /api/libros debe responder 201 cuando los datos sean válidos.
10. Mantener un formato uniforme de errores en JSON.

Entrega el código completo de app.py, explicado de forma sencilla y listo para ejecutar en Google Colab.
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(title="Biblioteca API")

libros = {
    1: {
        "id": 1,
        "titulo": "Rayuela",
        "autor": "Julio Cortázar"
    }
}

class Libro(BaseModel):
    model_config = ConfigDict(extra="allow")

    titulo: str = Field(min_length=1)

class LibroNoEncontrado(Exception):
    def __init__(self, libro_id: int):
        self.libro_id = libro_id

@app.exception_handler(LibroNoEncontrado)
async def manejar_libro_no_encontrado(request: Request, exc: LibroNoEncontrado):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "codigo": "NO_ENCONTRADO",
                "mensaje": f"El libro {exc.libro_id} no existe"
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def manejar_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "codigo": "VALIDACION",
                "mensaje": "Revisa los datos enviados"
            }
        }
    )

@app.get("/api/libros/{id}")
def obtener_libro(id: int):
    if id not in libros:
        raise LibroNoEncontrado(id)

    return libros[id]

@app.post("/api/libros", status_code=201)
def agregar_libro(libro: Libro):
    nuevo_id = max(libros.keys()) + 1

    nuevo_libro = {
        "id": nuevo_id,
        **libro.model_dump()
    }

    libros[nuevo_id] = nuevo_libro

    return nuevo_libro
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de captura de errores sin crashing (HTTP 500)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
>La IA inicialmente no consideró que los datos enviados por la prueba podían tener campos adicionales. Por eso, al registrar un libro válido, la API respondía con HTTP 422 en lugar de HTTP 201.
Para corregirlo modifiqué el modelo Pydantic utilizando ConfigDict(extra="allow"), manteniendo la validación para evitar títulos vacíos.
También comprobé que los errores 404 y 422 tuvieran el mismo formato JSON, facilitando la comprensión de los mensajes para el cliente. 

---
**Firma digital:** [Javier Alexander2001]
