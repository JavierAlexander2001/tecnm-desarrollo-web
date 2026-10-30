# Bitácora de Requerimientos y Auditoría IA — Sesión 07
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Especificación OpenAPI (Swagger) y ReDoc  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Anotación manual de metadata de endpoints  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> Me costó configurar manualmente la documentación de los endpoints porque tenía que agregar los nombres, descripciones y respuestas de cada ruta. También necesitaba que la documentación coincidiera con lo que realmente hacía la API.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10+, FastAPI y Pydantic v2 trabajando en Google Colab. |
| **Rol (R)** | Desarrollador encargado de crear y documentar una API REST de libros. |
| **Especificación (E)** | Crear una API llamada Biblioteca API, versión 1.0.0, con las rutas GET y POST /api/ libros. Generar /openapi.json, /docs y /redoc. La consulta debe responder HTTP 200 y el registro HTTP 201. |
| **Output (O)** | Código app.py funcional, modelos Pydantic, rutas documentadas y respuestas en formato JSON. |

### 2.2 Prompt Estructurado
```text
Desarrolla una API REST utilizando Python, FastAPI y Pydantic v2 para administrar libros.

La aplicación debe llamarse "Biblioteca API", tener la versión 1.0.0 y la descripción "API de libros del curso DAB-2201".

Crea un modelo Pydantic llamado Libro con los campos id, titulo y autor.

Implementa GET /api/libros para consultar los libros y devolver un objeto JSON con la propiedad "libros". La lista debe iniciar vacía y responder con HTTP 200.

Implementa POST /api/libros para registrar un libro y responder con HTTP 201.

Documenta las rutas utilizando summary y response_model. Asegúrate de que FastAPI genere correctamente /openapi.json, /docs y /redoc.

Entrega un código sencillo, organizado y funcional que cumpla con los cuatro casos de verificación del laboratorio.
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI(
    title="Biblioteca API",
    version="1.0.0",
    description="API de libros del curso DAB-2201"
)

class Libro(BaseModel):
    id: int
    titulo: str
    autor: str

libros = []

@app.get(
    "/api/libros",
    response_model=dict[str, list[Libro]],
    summary="Listar libros",
    status_code=status.HTTP_200_OK
)
def listar_libros():
    return {"libros": libros}

@app.post(
    "/api/libros",
    response_model=Libro,
    summary="Crear un libro",
    status_code=status.HTTP_201_CREATED
)
def crear_libro(libro: Libro):
    libros.append(libro)
    return libro
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Verificación de renderizado de interfaz Swagger UI

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La primera versión del código no tenía configurados los metadatos de la API ni el modelo para documentar los libros. También se detectó que el endpoint devolvía una lista directamente y después dos libros de ejemplo, cuando el verificador esperaba un objeto JSON con una lista vacía. Lo corregí agregando el modelo Libro, configurando response_model y utilizando libros = []. Finalmente, las cuatro pruebas fueron aprobadas.

---
**Firma digital:** [Javier Alexander2001]
