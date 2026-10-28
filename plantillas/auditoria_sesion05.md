# Bitácora de Requerimientos y Auditoría IA — Sesión 05
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Pydantic v2 / DTOs en PHP y Tipado Estático  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* DTO manual con validación de tipos primitivos  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> Al principio me costó validar los datos que recibía la API y comprobar que cada campo tuviera el tipo correcto. También necesitaba evitar que se aceptaran datos adicionales que no pertenecían al libro. Con Pydantic pude hacer estas validaciones de una manera más sencilla.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python con FastAPI y Pydantic v2, ejecutado en Google Colab. |
| **Rol (R)** | 	Desarrollador de APIs REST encargado de validar los datos de entrada y salida. |
| **Especificación (E)** | Crear una API para registrar y consultar libros. Validar título, año, precio y disponibilidad; convertir años numéricos y rechazar datos inválidos o campos adicionales. |
| **Output (O)** | Archivo app.py con DTO de entrada y salida, rutas POST y GET, respuestas JSON y códigos HTTP correctos. |

### 2.2 Prompt Estructurado
```text
Desarrolla una API REST utilizando Python, FastAPI y Pydantic v2 para registrar y consultar libros. Crea un DTO de entrada con los campos titulo (str), anio (int), precio (float) y disponible (bool), y un DTO de salida que incluya también el id. Permite convertir cadenas numéricas como "1966" a enteros, pero rechaza años no numéricos y campos adicionales con error HTTP 422. Implementa POST /api/libros con respuesta HTTP 201 y GET /api/libros con respuesta HTTP 200. Guarda los libros en una lista y devuelve los datos en formato JSON. El código debe ser sencillo, funcional y cumplir con las pruebas del laboratorio.
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, status
from pydantic import BaseModel, ConfigDict

app = FastAPI(title="API de libros")


# DTO de entrada
class LibroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str
    anio: int
    precio: float
    disponible: bool


# DTO de salida
class LibroSalida(BaseModel):
    id: int
    titulo: str
    anio: int
    precio: float
    disponible: bool


libros: list[LibroSalida] = []


# Registrar un libro
@app.post(
    "/api/libros",
    response_model=LibroSalida,
    status_code=status.HTTP_201_CREATED
)
def crear_libro(libro: LibroEntrada) -> LibroSalida:
    nuevo_libro = LibroSalida(
        id=len(libros) + 1,
        titulo=libro.titulo,
        anio=libro.anio,
        precio=libro.precio,
        disponible=libro.disponible
    )

    libros.append(nuevo_libro)
    return nuevo_libro


# Consultar todos los libros
@app.get(
    "/api/libros",
    response_model=dict[str, list[LibroSalida]]
)
def listar_libros() -> dict[str, list[LibroSalida]]:
    return {"libros": libros}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de tipos incompatibles y coerción

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Al revisar el código, comprobé que era necesario rechazar los campos adicionales y los datos incorrectos. Para solucionarlo, utilicé `ConfigDict(extra="forbid")` en el DTO de entrada, de modo que los campos no permitidos generen un error HTTP 422. También separé el DTO de entrada del DTO de salida para controlar los datos que recibe y devuelve la API.

---
**Firma digital:** [Javier Alexander2001]
