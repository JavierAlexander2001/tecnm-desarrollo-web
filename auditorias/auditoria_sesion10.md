# Bitácora de Requerimientos y Auditoría IA — Sesión 10
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Hito 1: Mock API RESTful con OpenAPI y Validation Harness  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Integración de Router y esquemas de validación  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
>La dificultad que encontré fue lograr que las rutas de la API funcionaran correctamente y que cada petición HTTP devolviera el código de estado correspondiente. También tuve que cuidar la validación de los datos de los libros, porque si el título estaba vacío o el año era incorrecto, la API debía rechazar la petición sin provocar un error interno del servidor. 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Se utilizará Python con FastAPI desde Google Colab. Se trabajará con Pydantic para validar los datos y HTTPX para realizar las pruebas HTTP. |
| **Rol (R)** | Desarrollador especializado en Python, FastAPI y diseño de APIs RESTful. |
| **Especificación (E)** | Crear una API de libros con operaciones CRUD, asignación automática de identificadores, validación de títulos y años, manejo de errores HTTP y documentación OpenAPI. |
| **Output (O)** | rchivo app.py con código funcional, modelos Pydantic, rutas CRUD y respuestas HTTP correctas. Debe superar los nueve casos de prueba del verificador. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador especializado en Python y FastAPI.

Necesito crear una Mock API RESTful de libros utilizando
FastAPI y Pydantic desde Google Colab.

La API debe permitir:
- Listar todos los libros mediante GET.
- Registrar libros mediante POST.
- Consultar un libro por su ID.
- Actualizar libros mediante PUT.
- Eliminar libros mediante DELETE.
- Asignar automáticamente un ID a cada libro.
- Validar que el título no esté vacío y que el año
  sea igual o mayor a 1500.

Utiliza los códigos HTTP correspondientes:
200, 201, 204, 404, 405 y 422.

También debe generar la documentación OpenAPI
en /openapi.json.

Entrega el código completo en app.py, organizado
y funcional, que pueda superar los nueve casos
de prueba del Validation Harness.
```

---

## 3. Código Devuelto por el Modelo
```python

%%writefile app.py

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


```

---

## Evidencia Verificación

==============================================================================

VERIFICACIÓN DEL RESULTADO · 9 casos · app.py

==============================================================================

✅ 01. Listado inicial vacío

✅ 02. Creación válida

✅ 03. Consulta del libro creado

✅ 04. Actualización del libro

✅ 05. Eliminación del libro

✅ 06. El libro eliminado ya no existe

✅ 07. Validación de datos inválidos

✅ 08. Método no permitido

✅ 09. Contrato OpenAPI disponible

------------------------------------------------------------------------------

RESULTADO: 9/9 casos correctos. ¡Resultado logrado!

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Suite integral de 10 pruebas HTTP destructivas

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante la auditoría revisé que la API respondiera correctamente ante datos inválidos, libros inexistentes y métodos HTTP no permitidos. La IA proporcionó una solución que logró superar las pruebas del verificador, por lo que no fue necesario realizar correcciones adicionales para completar los nueve casos.

---
**Firma digital:** [Javier Alexander2001]
