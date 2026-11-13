# Bitácora de Requerimientos y Auditoría IA — Sesión 15
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Autenticación Stateless con JSON Web Tokens (JWT)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Codificación Base64Url y firma HMAC-SHA256  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
>La principal dificultad fue comprender cómo funciona la autenticación mediante JWT y cómo se comprueba que un token sea válido. En mi primera implementación utilicé un token fijo y permití consultar el perfil sin iniciar sesión. Después comprendí que era necesario validar las credenciales, generar un token firmado y comprobar su autenticidad antes de permitir el acceso. 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 con FastAPI en Google Colab. Se utiliza PyJWT para generar y validar tokens. |
| **Rol (R)** | Desarrollador especializado en Python, FastAPI y seguridad de aplicaciones web. |
| **Especificación (E)** | Crear un endpoint POST /api/token para validar el usuario ana y la contraseña secreta. Generar un JWT firmado con HS256, incluyendo el usuario y su fecha de expiración. Crear GET /api/perfil para validar el token Bearer. Rechazar tokens ausentes, alterados o vencidos con HTTP 401. |
| **Output (O)** | Código completo y comentado para app.py, utilizando PyJWT, FastAPI y una clave secreta obtenida de una variable de entorno. |

### 2.2 Prompt Estructurado
```text
Quiero que me ayudes a realizar un sistema de autenticación con JWT utilizando Python y FastAPI en Google Colab. Necesito que el sistema tenga una ruta para iniciar sesión donde se comprueben el usuario ana y la contraseña secreta. Si los datos son correctos, quiero que genere un token JWT firmado con HS256 y que tenga una fecha de expiración.

También necesito otra ruta para consultar el perfil del usuario, pero solamente debe permitir el acceso cuando se envíe un token válido mediante el encabezado Authorization: Bearer. Si no se envía el token, está modificado o ya venció, debe responder con un error HTTP 401.

Quiero que utilices la librería PyJWT y que la clave secreta se obtenga de una variable de entorno, sin escribirla directamente en el código. Proporciona el código completo, comentado y explicado de manera sencilla, para poder ejecutarlo en Google Colab y comprobar que funcione correctamente con las pruebas de la actividad.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import os
import secrets
import jwt

app = FastAPI(title="Sistema de Autenticación JWT")

# Obtiene la clave desde una variable de entorno.
# Si no existe, genera una clave temporal para la práctica.
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usuario de prueba de la actividad
USUARIO = "ana"
PASSWORD = "secreta"


class DatosLogin(BaseModel):
    usuario: str
    password: str


@app.post("/api/token")
def crear_token(datos: DatosLogin):
    # Validar las credenciales
    if datos.usuario != USUARIO or datos.password != PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Crear la fecha de expiración
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Datos que se guardarán dentro del JWT
    payload = {
        "usuario": datos.usuario,
        "exp": expiracion
    }

    # Firmar el token
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/api/perfil")
def consultar_perfil(authorization: str | None = Header(default=None)):
    # Comprobar que exista el encabezado Bearer
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Token no proporcionado"
        )

    token = authorization.split(" ", 1)[1]

    try:
        # Validar firma, algoritmo y expiración
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario = payload.get("usuario")

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return {"usuario": usuario}

    except jwt.InvalidTokenError:
        # Incluye tokens alterados, mal formados o vencidos
        raise HTTPException(
            status_code=401,
            detail="Token inválido o vencido"
        )
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas con tokens alterados o firma inválida

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En la primera implementación no se comprobaba la autenticación del usuario, por lo que cualquier persona podía consultar el perfil sin presentar un token. También se utilizaba un token fijo que no tenía una firma válida.

Esto se corrigió generando tokens JWT firmados con HS256 y agregando la validación de la firma y la fecha de expiración. Cuando el token no existe, está alterado o venció, el servidor responde con HTTP 401.

---
**Firma digital:** [Usuario de GitHub]
