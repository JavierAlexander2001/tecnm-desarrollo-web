# Bitácora de Requerimientos y Auditoría IA — Sesión 13
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Manejo de Sesiones Stateful vs Stateless Tokens  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Simulador de tabla de sesiones en memoria  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La principal dificultad que encontré fue controlar correctamente las sesiones y manejar las respuestas HTTP. Al principio logré que el inicio de sesión y la consulta del perfil funcionaran, pero tuve un problema al cerrar la sesión porque no se devolvía el código HTTP 204 que solicitaba el verificador.

También tuve que comprender cómo funciona la cookie para que el servidor pudiera reconocer al usuario en las siguientes peticiones.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 y FastAPI en Google Colab. Se utilizan sesiones en memoria, cookies HttpOnly y modelos Pydantic. |
| **Rol (R)** | Desarrollador de aplicaciones web especializado en FastAPI, APIs REST y manejo de sesiones. |
| **Especificación (E)** | Implementar las rutas POST /api/login, GET /api/perfil y POST /api/logout. Validar el usuario ana y la contraseña secreta. Utilizar una cookie session_id con HttpOnly y SameSite=Lax. Las respuestas deben ser HTTP 200, 200, 204 y 401 después del cierre de sesión. |
| **Output (O)** | Código completo de app.py, organizado, comentado y funcional, utilizando FastAPI, Pydantic, identificadores de sesión aleatorios y almacenamiento en memoria. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador de aplicaciones web
especializado en Python y FastAPI.

Necesito implementar un sistema de manejo de sesiones
Stateful utilizando almacenamiento en memoria y cookies.

El sistema debe cumplir los siguientes requisitos:

1. Crear POST /api/login para validar:
   Usuario: ana
   Contraseña: secreta

2. Si los datos son correctos, responder HTTP 200
   y generar una cookie llamada session_id.

3. La cookie debe tener HttpOnly, SameSite=Lax
   y Path=/.

4. Crear GET /api/perfil para consultar al usuario
   mediante la cookie de sesión.

5. Si la sesión no existe o no es válida,
   responder HTTP 401.

6. Crear POST /api/logout para eliminar la sesión
   y la cookie, respondiendo HTTP 204 sin contenido.

Entrega el código completo de app.py,
con comentarios y buena organización.

El código debe cumplir los cuatro casos
de verificación del contrato.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
import secrets

app = FastAPI(title="Sistema de Sesiones")

# Almacenamiento de sesiones en memoria
sesiones = {}

# Usuario de prueba
USUARIO = "ana"
PASSWORD = "secreta"


# Modelo para recibir los datos del login
class LoginRequest(BaseModel):
    usuario: str
    password: str


# Ruta para iniciar sesión
@app.post("/api/login")
def login(datos: LoginRequest, response: Response):

    # Validar usuario y contraseña
    if datos.usuario != USUARIO or datos.password != PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Crear identificador único de sesión
    session_id = secrets.token_urlsafe(32)

    # Guardar la sesión en el servidor
    sesiones[session_id] = datos.usuario

    # Enviar cookie al cliente
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        path="/"
    )

    return {"mensaje": "sesión iniciada"}


# Ruta para consultar el perfil
@app.get("/api/perfil")
def perfil(session_id: str = Cookie(default=None)):

    # Comprobar si la sesión existe
    if not session_id or session_id not in sesiones:
        raise HTTPException(
            status_code=401,
            detail="Sesión no válida"
        )

    # Devolver información del usuario
    return {"usuario": sesiones[session_id]}


# Ruta para cerrar sesión
@app.post("/api/logout")
def logout(
    response: Response,
    session_id: str = Cookie(default=None)
):

    # Eliminar la sesión del servidor
    if session_id:
        sesiones.pop(session_id, None)

    # Eliminar la cookie del cliente
    response.delete_cookie(
        key="session_id",
        path="/",
        httponly=True,
        samesite="lax"
    )

    # Responder con HTTP 204 sin contenido
    response.status_code = 204
    response.body = b""

    return response

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de expiración y revocación de sesión

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> El error que detectó la verificación fue que la ruta de logout no devolvía el código HTTP 204 esperado. Aunque la sesión se eliminaba correctamente, la respuesta no cumplía con el contrato.

Para corregirlo, establecí explícitamente el código de estado 204 y dejé la respuesta sin contenido. Después ejecuté nuevamente el verificador para comprobar que todos los casos funcionaran correctamente.

---
**Firma digital:** [Javier Alexander2001]
