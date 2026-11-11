# Bitácora de Requerimientos y Auditoría IA — Sesión 11
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Arquitectura en Capas: Router, Servicio y Capa de Datos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Separación manual de controladores y lógica  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue separar las funciones del código en diferentes archivos, ya que cada uno tiene una responsabilidad distinta. También fue necesario conectar correctamente las rutas con el servicio y el repositorio para que las peticiones HTTP siguieran funcionando.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python con FastAPI y Pydantic en Google Colab. |
| **Rol (R)** | Desarrollador especializado en APIs RESTful y arquitectura por capas. |
| **Especificación (E)** | Separar el proyecto en cuatro archivos: app.py, router.py, servicio.py y repositorio.py, manteniendo las rutas y validaciones originales. |
| **Output (O)** | Código Python organizado, modular y funcional, con respuestas HTTP 200, 201 y 422. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador backend especializado en Python y FastAPI.

Necesito organizar una API de biblioteca utilizando arquitectura en capas.

El proyecto debe tener cuatro archivos:
- app.py: crear la aplicación e incluir el router.
- router.py: definir las rutas GET y POST de libros.
- servicio.py: manejar la lógica de creación y listado.
- repositorio.py: guardar los libros en memoria.

Mantén el contrato HTTP original:
- GET /api/libros debe responder 200.
- POST /api/libros debe responder 201.
- Los datos inválidos deben responder 422.

Utiliza Pydantic para validar los datos.
Entrega el código completo de cada archivo,
de forma sencilla y sin cambiar las respuestas esperadas.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI
from router import router

app = FastAPI(title="Biblioteca por capas")

app.include_router(router)


%%writefile repositorio.py

libros = []
siguiente_id = 1

def listar_libros():
    return libros

def guardar_libro(titulo, anio):
    global siguiente_id

    libro = {
        "id": siguiente_id,
        "titulo": titulo,
        "anio": anio
    }

    libros.append(libro)
    siguiente_id += 1

    return libro


%%writefile servicio.py
from repositorio import listar_libros, guardar_libro

def obtener_libros():
    return {"libros": listar_libros()}

def crear_libro(titulo, anio):
    return guardar_libro(titulo, anio)


%%writefile router.py
from fastapi import APIRouter
from pydantic import BaseModel
from servicio import obtener_libros, crear_libro

router = APIRouter()

class Libro(BaseModel):
    titulo: str
    anio: int

@router.get("/api/libros")
def listar():
    return obtener_libros()

@router.post("/api/libros", status_code=201)
def crear(libro: Libro):
    return crear_libro(libro.titulo, libro.anio)
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de aislamiento de errores en lógica de negocio

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante la revisión comprobé que era necesario mantener el código HTTP 201 al crear un libro y el 422 cuando los datos no son válidos. Se utilizó Pydantic para validar los datos recibidos y se configuró la ruta POST para responder con 201.

La verificación permitió revisar que las capas estuvieran conectadas correctamente y que se conservara el contrato HTTP.

---
**Firma digital:** [Javier Alexander2001]
