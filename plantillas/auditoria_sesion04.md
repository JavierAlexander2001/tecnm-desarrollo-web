# Bitácora de Requerimientos y Auditoría IA — Sesión 04
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Anatomía RESTful, URIs Nombres y Recursos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexader Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Diseño de URIs jerárquicas sin verbos en la ruta  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
>La dificultad que encontré fue organizar las rutas para consultar los libros de cada autor y hacer que los filtros funcionaran correctamente. También tuve que comprender cómo validar si un autor existe y cómo responder con un código HTTP 404 cuando no se encuentra. 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilicé Python con FastAPI en Google Colab para desarrollar y probar una API RESTful. |
| **Rol (R)** | Solicité a la IA que actuara como asistente de programación para ayudarme a diseñar rutas y organizar los recursos de autores y libros. |
| **Especificación (E)** | Crear GET /api/libros y GET /api/autores/{autor_id}/libros. Permitir los parámetros opcionales genero y limite. Si el autor no existe, responder con HTTP 404. |
| **Output (O)** | Obtener el código de app.py con respuestas JSON y códigos HTTP correctos, para después comprobarlo con el verificador de la actividad. |

### 2.2 Prompt Estructurado
```text
Ayúdame a desarrollar una API RESTful utilizando Python y FastAPI
en Google Colab.

Necesito crear una ruta GET /api/libros para consultar la colección
de libros y otra ruta GET /api/autores/{autor_id}/libros para
consultar los libros de un autor.

La segunda ruta debe aceptar los parámetros opcionales genero
y limite. Si el autor no existe, debe responder con HTTP 404
y el mensaje "Autor no encontrado".

Utiliza estos datos:
- Autor 1: Gabriel García Márquez.
- Libro 1: Cien años de soledad, género novela.
- Libro 2: Doce cuentos peregrinos, género cuento.
- Autor 2: Julio Cortázar.
- Libro 3: Rayuela, género novela.

Usa nombres de recursos en las rutas, sin verbos.
Entrega el código completo de app.py y explica cómo comprobar
que las respuestas coincidan con los requisitos.
```

---

## 3. Código Devuelto por el Modelo
```python
La IA generó el siguiente código utilizando Python y FastAPI. El código permite consultar los libros, buscar los libros de un autor, filtrar por género, limitar los resultados y responder con un error 404 cuando el autor no existe.


%%writefile app.py
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(title="API de Autores y Libros")

# Datos de los autores
autores = {
    1: "Gabriel García Márquez",
    2: "Julio Cortázar"
}

# Datos de los libros
libros = [
    {"id": 1, "titulo": "Cien años de soledad", "genero": "novela", "autor_id": 1},
    {"id": 2, "titulo": "Doce cuentos peregrinos", "genero": "cuento", "autor_id": 1},
    {"id": 3, "titulo": "Rayuela", "genero": "novela", "autor_id": 2}
]

# Obtener todos los libros
@app.get("/api/libros")
def obtener_libros():
    return {
        "libros": [
            {"id": libro["id"]}
            for libro in libros
        ]
    }

# Obtener los libros de un autor
@app.get("/api/autores/{autor_id}/libros")
def obtener_libros_autor(
    autor_id: int,
    genero: Optional[str] = None,
    limite: Optional[int] = None
):
    # Comprobar si existe el autor
    if autor_id not in autores:
        raise HTTPException(
            status_code=404,
            detail="Autor no encontrado"
        )

    # Buscar los libros del autor
    resultado = [
        libro for libro in libros
        if libro["autor_id"] == autor_id
    ]

    # Filtrar por género si se proporciona
    if genero is not None:
        resultado = [
            libro for libro in resultado
            if libro["genero"].lower() == genero.lower()
        ]

    # Aplicar el límite si se proporciona
    if limite is not None:
        resultado = resultado[:max(0, limite)]

    # Preparar la respuesta sin mostrar autor_id en cada libro
    return {
        "autor_id": autor_id,
        "libros": [
            {
                "id": libro["id"],
                "titulo": libro["titulo"],
                "genero": libro["genero"]
            }
            for libro in resultado
        ]
    }

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de peticiones a recursos inexistentes (404)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Al revisar el código generado por la IA, identifiqué que era importante validar si el autor existía antes de mostrar sus libros. Para solucionarlo, utilicé el código HTTP 404 con el mensaje "Autor no encontrado".

También aprendí que los filtros por género y el límite de resultados deben funcionar con los parámetros enviados en la URL. Para comprobar que el código cumpliera con los requisitos, utilicé el verificador de la actividad.

Con esta revisión comprendí que no basta con que el código parezca funcionar, sino que debe cumplir con las rutas, las respuestas y los códigos HTTP establecidos en el contrato.

---
**Firma digital:** [Javier Alexander2001]
