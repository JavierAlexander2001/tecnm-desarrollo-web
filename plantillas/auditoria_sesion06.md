# Bitácora de Requerimientos y Auditoría IA — Sesión 06
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Validación Estricta, Constraints y Params Query/Body  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Filtro manual de rangos y longitudes de texto  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> Me costó validar manualmente los datos porque tenía que revisar que el título tuviera la longitud correcta, que el año estuviera dentro del rango permitido y que el precio fuera mayor que cero. También debía comprobar que el límite de consulta no fuera menor que 1 ni mayor que 100.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10+, FastAPI y Pydantic v2 en Google Colab. |
| **Rol (R)** | Desarrollador encargado de crear y validar una API REST de libros. |
| **Especificación (E)** | El título debe tener entre 3 y 80 caracteres, el año entre 1450 y 2100 y el precio debe ser mayor que cero. El parámetro limite debe estar entre 1 y 100. |
| **Output (O)** | Código app.py con modelos de entrada y salida, validaciones mediante Field y Query, y respuestas HTTP 201, 200 o 422 según corresponda. |

### 2.2 Prompt Estructurado
```text
Desarrolla una API REST utilizando Python, FastAPI y Pydantic v2 para registrar y consultar libros.

Crea un DTO de entrada con los campos titulo, anio y precio. El título debe tener entre 3 y 80 caracteres, el año debe estar entre 1450 y 2100 y el precio debe ser mayor que cero.

Utiliza Field para validar los campos y Query para controlar el parámetro limite del método GET, permitiendo valores entre 1 y 100.

Implementa POST /api/libros con respuesta HTTP 201 y GET /api/libros con respuesta HTTP 200. Los datos incorrectos deben generar un error HTTP 422.

Utiliza un DTO de salida que incluya el id, guarda los libros en una lista y devuelve la información en formato JSON. El código debe ser sencillo, organizado y cumplir con los seis casos de verificación del laboratorio.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, Query, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(
    title="API de libros",
    description="API para registrar y consultar libros con validaciones",
    version="1.0.0"
)


# DTO de entrada
class LibroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str = Field(min_length=3, max_length=80)
    anio: int = Field(ge=1450, le=2100)
    precio: float = Field(gt=0)


# DTO de salida
class LibroSalida(BaseModel):
    id: int
    titulo: str
    anio: int
    precio: float


# Almacenamiento temporal
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
        precio=libro.precio
    )

    libros.append(nuevo_libro)

    return nuevo_libro


# Consultar libros con límite de resultados
@app.get(
    "/api/libros",
    response_model=dict[str, list[LibroSalida]],
    status_code=status.HTTP_200_OK
)
def listar_libros(
    limite: int = Query(default=10, ge=1, le=100)
) -> dict[str, list[LibroSalida]]:

    return {"libros": libros[:limite]}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de desbordamiento de cadenas y números negativos

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La primera versión del código no tenía todas las validaciones necesarias. Se corrigió utilizando Field para establecer los límites del título, año y precio, y Query para controlar el límite de resultados. También se comprobó que los datos incorrectos generaran el código HTTP 422 y que las peticiones correctas respondieran con los códigos 201 y 200.

---
**Firma digital:** [Javier Alxander2001]
