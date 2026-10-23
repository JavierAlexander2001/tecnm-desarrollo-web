# Bitácora de Requerimientos y Auditoría IA — Sesión 03
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Headers, Content-Type y Negociación de Contenido  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lectura y emisión manual de encabezados HTTP  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue entender cómo revisar los encabezados de una petición y comprobar si los datos que manda el cliente están en el formato correcto. También tuve que aprender la diferencia entre Content-Type y Accept, porque uno indica el formato que envío y el otro el formato que quiero recibir.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Estoy trabajando en Google Colab con Python y FastAPI para crear una API de libros. |
| **Rol (R)** | Quiero que la IA me ayude a desarrollar una API y validar correctamente los encabezados HTTP. |
| **Especificación (E)** | Crear las rutas POST y GET para libros. El POST solo acepta JSON y devuelve 415 si el formato no es compatible. El GET devuelve 406 si el cliente solicita XML. Las respuestas correctas deben usar JSON, con código 201 al crear un libro y 200 al consultar la lista. |
| **Output (O)** | Obtener el archivo app.py, pasar las cuatro pruebas de verificación y completar la bitácora de auditoría. |

### 2.2 Prompt Estructurado
```text
Estoy trabajando en Google Colab con Python y FastAPI.

Ayúdame a crear una API REST para registrar y consultar libros
en la ruta /api/libros.

Necesito que el POST solo acepte Content-Type: application/json
y responda con HTTP 415 cuando se envíe otro formato.

El GET debe revisar el encabezado Accept y responder HTTP 406
si el cliente solicita un formato que no está soportado, como XML.

Cuando se cree un libro correctamente, debe responder HTTP 201.
Cuando se consulte la lista de libros, debe responder HTTP 200.

Las respuestas correctas deben incluir Content-Type: application/json.

Quiero un código claro en app.py que pueda ejecutar en Colab
y que cumpla con los cuatro casos de verificación del ejercicio.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="API de libros con negociación de contenido")

# Lista temporal para almacenar los libros creados
libros = []


@app.post("/api/libros")
async def crear_libro(request: Request):
    # Verificar el formato que envía el cliente
    content_type = request.headers.get("content-type", "")
    content_type = content_type.split(";")[0].strip().lower()

    if content_type != "application/json":
        return JSONResponse(
            status_code=415,
            content={"detail": "Unsupported Media Type"}
        )

    # Leer y validar los datos recibidos
    try:
        datos = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"detail": "JSON inválido"}
        )

    if not isinstance(datos, dict):
        return JSONResponse(
            status_code=422,
            content={"detail": "Se esperaba un objeto JSON"}
        )

    if not isinstance(datos.get("titulo"), str) or not isinstance(datos.get("anio"), int) or isinstance(datos.get("anio"), bool):
        return JSONResponse(
            status_code=422,
            content={"detail": "El título debe ser texto y el año un número entero"}
        )

    # Crear el libro y asignarle un identificador
    libro = {
        "id": len(libros) + 1,
        "titulo": datos["titulo"],
        "anio": datos["anio"]
    }
    libros.append(libro)

    return JSONResponse(
        status_code=201,
        content=libro,
        media_type="application/json"
    )


@app.get("/api/libros")
async def listar_libros(request: Request):
    # Verificar el formato que acepta el cliente
    accept = request.headers.get("accept", "*/*")
    formatos = [formato.split(";")[0].strip().lower()
                for formato in accept.split(",")]

    acepta_json = any(
        formato in ("application/json", "*/*", "application/*")
        for formato in formatos
    )

    if not acepta_json:
        return JSONResponse(
            status_code=406,
            content={"detail": "Not Acceptable"}
        )

    return JSONResponse(
        status_code=200,
        content=libros,
        media_type="application/json"
    )

La IA me ayudó a crear el archivo app.py utilizando Python y FastAPI. El código permite registrar libros y consultar la lista de libros mediante las rutas POST y GET.

También valida los encabezados HTTP. Si envío datos que no son JSON, responde con el código 415. Si solicito un formato que no está soportado, como XML, responde con el código 406.

Cuando registro un libro correctamente, la API devuelve el código 201, y cuando consulto los libros, devuelve el código 200.

Después, ejecuté el verificador del cuaderno para comprobar si el código cumplía con los requisitos de la actividad.
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas con tipos de contenido no soportados (415)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Un error que tuve que prevenir fue aceptar formatos que la API no soporta. Para solucionarlo, agregué validaciones de los encabezados Content-Type y Accept, de manera que la API pueda devolver los códigos 415 y 406 cuando corresponda.

También consideré que los datos recibidos deben tener una estructura válida antes de registrar un libro.

---
**Firma digital:** [Javier Alexander2001]
