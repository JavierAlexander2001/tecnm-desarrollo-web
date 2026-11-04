# Bitácora de Requerimientos y Auditoría IA — Sesión 09
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Middleware Web, Intercepción y Logging de Transacciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Middleware manual de tiempo de respuesta (X-Process-Time)  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue medir el tiempo de cada petición y agregar los encabezados correctamente. En mi primer código olvidé generar un identificador cuando el cliente no lo enviaba, por lo que algunas respuestas no tenían todas las cabeceras necesarias.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 con FastAPI en Google Colab. |
| **Rol (R)** | Desarrollador web especializado en Python y creación de API REST. |
| **Especificación (E)** | Crear un middleware que mida el tiempo de las peticiones, agregue X-Process-Time y X-Request-ID, conserve el identificador del cliente y genere uno cuando no exista. También debe funcionar en respuestas 404. |
| **Output (O)** | Código Python completo para el archivo app.py, con comentarios y listo para ejecutar y verificar. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador web especializado en Python y FastAPI.

Necesito crear un middleware que mida el tiempo de cada petición HTTP.

Requisitos:
1. Agregar el encabezado X-Process-Time con el tiempo de respuesta.
2. Agregar el encabezado X-Request-ID.
3. Conservar el identificador enviado por el cliente.
4. Generar un identificador único cuando el cliente no envíe uno.
5. Aplicar el middleware también a las respuestas 404.
6. Mantener GET /api/libros con respuesta HTTP 200.

Entrega el código completo de app.py, con comentarios sencillos y listo para ejecutarse en Google Colab.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
import time
import uuid

from fastapi import FastAPI, Request

app = FastAPI(title="Middleware Web")

# Middleware para medir el tiempo y controlar las peticiones
@app.middleware("http")
async def middleware(request: Request, call_next):

    inicio = time.perf_counter()

    # Obtener el identificador del cliente o generar uno nuevo
    request_id = request.headers.get("X-Request-ID")

    if not request_id:
        request_id = str(uuid.uuid4())

    # Continuar con la petición
    response = await call_next(request)

    # Calcular el tiempo de respuesta
    tiempo = time.perf_counter() - inicio

    # Agregar encabezados a todas las respuestas
    response.headers["X-Process-Time"] = f"{tiempo:.4f}"
    response.headers["X-Request-ID"] = request_id

    return response


# Endpoint para consultar los libros
@app.get("/api/libros")
async def obtener_libros():
    return {"libros": []}

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de inyección de encabezados de rastreo

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En mi primer código, la verificación detectó que no se generaba el encabezado X-Request-ID cuando el cliente no enviaba un identificador. También faltaba generar un ID automáticamente. Lo corregí utilizando UUID en el código de IA. Después de realizar los cambios, el código cumplió con los requisitos de la actividad.

---
**Firma digital:** [Javier Alexander2001]
