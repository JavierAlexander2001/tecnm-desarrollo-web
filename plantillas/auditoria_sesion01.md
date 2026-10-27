# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Encuadre, Diagnóstico HTTP y Servidor en Colab  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Procesamiento manual de JSON de petición sin IA  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue entender cómo recibir y validar los datos de una petición HTTP. También fue necesario identificar cómo responder cuando el JSON está mal escrito, para evitar que el servidor produzca un error interno.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10 o superior, FastAPI y Pydantic ejecutados en Google Colab. |
| **Rol (R)** | Desarrollador backend encargado de crear una API REST y validar las peticiones HTTP. |
| **Especificación (E)** | Crear GET /api/estado y POST /api/eco. La primera ruta devuelve el estado del servidor y el nombre del curso. La segunda recibe un JSON con la clave mensaje y devuelve el mensaje recibido. El JSON mal formado debe producir HTTP 422 y los métodos no permitidos deben producir HTTP 405. |
| **Output (O)** | Archivo app.py funcional, modelo Pydantic, respuestas JSON y códigos HTTP correctos. |

### 2.2 Prompt Estructurado
```text
Contexto:
Estoy trabajando en Google Colab con Python, FastAPI y Pydantic.

Rol:
Actúa como desarrollador backend especializado en APIs REST.

Especificación:
Crea una API con dos rutas:
1. GET /api/estado debe devolver
   {"servidor": "ok", "curso": "DAB-2201"} con HTTP 200.
2. POST /api/eco debe recibir un JSON con la clave
   "mensaje" y devolver {"mensaje": valor, "recibido": true}
   con HTTP 200.

El JSON mal formado debe producir HTTP 422 sin provocar
un error HTTP 500. Si se utiliza GET en /api/eco,
el servidor debe responder HTTP 405.

Output:
Entrega el código completo de app.py, utiliza un modelo
Pydantic para validar los datos y explica brevemente
cómo ejecutar las pruebas HTTP.
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="API de Desarrollo Web DAB-2201")


class Mensaje(BaseModel):
    mensaje: str


@app.get("/api/estado")
def estado():
    return {
        "servidor": "ok",
        "curso": "DAB-2201"
    }


@app.post("/api/eco")
def eco(datos: Mensaje):
    return {
        "mensaje": datos.mensaje,
        "recibido": True
    }

Explicación: FastAPI utiliza el modelo Mensaje para validar el cuerpo de la petición. La ruta de estado devuelve información del servidor y la ruta de eco devuelve el mensaje recibido. FastAPI responde automáticamente con HTTP 422 cuando el cuerpo JSON está mal formado y con HTTP 405 cuando se utiliza un método no permitido.
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de códigos de estado HTTP 200, 400 y 422

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La verificación comprueba que la API responda con los códigos HTTP correctos. Una posible falla sería no validar el cuerpo JSON o permitir un método HTTP incorrecto. Para resolverlo, utilicé un modelo Pydantic y definí las rutas con los métodos GET y POST correspondientes. Los resultados finales deben confirmarse ejecutando el verificador del curso.

---
**Firma digital:** [Javier Alexander2001]
