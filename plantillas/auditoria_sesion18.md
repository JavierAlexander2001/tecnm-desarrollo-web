# Bitácora de Requerimientos y Auditoría IA — Sesión 18
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Rate Limiting, Throttling y Prevención de Abuso  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054l]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Contador manual de peticiones por IP en memoria  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La principal dificultad que encontré fue controlar correctamente la cantidad de peticiones que podía realizar cada cliente. En mi primer intento utilicé un contador global, pero después comprendí que esto podía afectar a todos los usuarios. También tuve dificultades para establecer el límite de tres peticiones y controlar el tiempo de espera de 60 segundos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python con FastAPI en Google Colab. Entorno de ejecución y verificación mediante HTTP. |
| **Rol (R)** | Desarrollador backend especializado en APIs REST y seguridad web. |
| **Especificación (E)** | Crear un límite de tres peticiones por cliente mediante su dirección IP, dentro de una ventana de 60 segundos. La cuarta petición debe responder HTTP 429 e incluir Retry-After. |
| **Output (O)** | Archivo app.py funcional, con respuestas JSON, control de peticiones y códigos HTTP correctos. |

### 2.2 Prompt Estructurado
```text
Actúa como desarrollador backend especializado en Python y FastAPI. Necesito implementar un sistema de Rate Limiting para una API.

La ruta GET /api/recurso debe permitir tres peticiones por cliente dentro de una ventana de 60 segundos. La cuarta petición debe responder con HTTP 429 Too Many Requests, incluir el encabezado Retry-After y devolver el JSON {"error":"límite de peticiones alcanzado"}.

Las primeras tres peticiones deben responder con HTTP 200 y un JSON sencillo. El contador debe ser independiente para cada cliente y reiniciarse al iniciar la aplicación.

Entrega el código completo en un archivo app.py, organizado, funcional y compatible con el verificador HTTP de Google Colab.


```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from collections import defaultdict, deque
import time
import math
import threading

app = FastAPI(title="API con Rate Limiting")

# Configuración
LIMITE = 3
VENTANA = 60

# Historial de peticiones por cliente
peticiones = defaultdict(deque)

# Evitar conflictos entre peticiones simultáneas
bloqueo = threading.Lock()


@app.get("/api/recurso")
def obtener_recurso(request: Request):

    cliente = request.client.host
    ahora = time.monotonic()

    with bloqueo:

        historial = peticiones[cliente]

        # Eliminar peticiones fuera de la ventana
        while historial and ahora - historial[0] >= VENTANA:
            historial.popleft()

        # Comprobar si se alcanzó el límite
        if len(historial) >= LIMITE:

            tiempo_restante = math.ceil(
                VENTANA - (ahora - historial[0])
            )

            return JSONResponse(
                status_code=429,
                content={
                    "error": "límite de peticiones alcanzado"
                },
                headers={
                    "Retry-After": str(tiempo_restante)
                }
            )

        # Registrar petición
        historial.append(ahora)

    return {
        "mensaje": "Petición permitida",
        "estado": "correcto"
    }
```

---
## Evidencia Evaluación

==============================================================================

VERIFICACIÓN DEL RESULTADO · 4 casos · app.py

==============================================================================

✅ 01. Primera petición permitida

✅ 02. Segunda petición permitida

✅ 03. Tercera petición permitida

✅ 04. La cuarta petición se limita

------------------------------------------------------------------------------

RESULTADO: 4/4 casos correctos. ¡Resultado logrado!



## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de ráfaga masiva y bloqueo temporal (HTTP 429)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En mi primer código encontré que utilizaba un contador global, permitía cuatro peticiones y no incluía el encabezado Retry-After. Al comparar esta versión con la propuesta por la IA, pude identificar esos errores y mejorar la implementación. La versión corregida utiliza un contador por cliente y responde con HTTP 429 cuando se supera el límite de tres solicitudes.

---
**Firma digital:** [Javier Alexander2001]
