# Bitácora de Requerimientos y Auditoría IA — Sesión 16
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** OAuth2 Password Flow y Header Authorization Bearer  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Extracción manual del encabezado Authorization  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La principal dificultad fue comprender cómo recibir y comprobar el token que se envía en el encabezado Authorization. En mi primera implementación no tenía una forma de validar el token ni de proteger el perfil. También utilicé JSON para enviar los datos de inicio de sesión, cuando la actividad solicitaba un formulario.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 con FastAPI en Google Colab. Se utilizan las librerías necesarias para implementar OAuth2 y JWT. |
| **Rol (R)** | Desarrollador especializado en Python, FastAPI y seguridad de aplicaciones web. |
| **Especificación (E)** | 

Crear POST /token para recibir el usuario ana y la contraseña secreta mediante un formulario. Si los datos son correctos, generar un token JWT. Crear GET /api/perfil para validar el token enviado mediante Authorization: Bearer. Si no se envía el token o se utiliza otro esquema, responder HTTP 401 e incluir el encabezado WWW-Authenticate: Bearer. |
| **Output (O)** | Código completo y comentado para app.py, utilizando OAuth2PasswordRequestForm y OAuth2PasswordBearer, listo para ejecutarse en Google Colab. |

### 2.2 Prompt Estructurado
```text
Quiero que me ayudes a implementar un sistema de autenticación OAuth2 utilizando Python y FastAPI en Google Colab. Necesito crear una ruta POST /token que reciba el nombre de usuario y la contraseña mediante un formulario, utilizando los datos de prueba ana y secreta. Si las credenciales son correctas, debe generar un token JWT y devolverlo con el tipo bearer.

También necesito una ruta GET /api/perfil que permita consultar la información del usuario solamente cuando se envíe un token válido mediante el encabezado Authorization: Bearer. Si no se proporciona el token o se utiliza un esquema diferente, debe responder con HTTP 401 e incluir el encabezado WWW-Authenticate: Bearer.

Quiero que utilices las herramientas de seguridad de FastAPI, como OAuth2PasswordRequestForm y OAuth2PasswordBearer, y que el código esté completo, comentado y listo para ejecutarse en Google Colab, cumpliendo con los casos de verificación de la actividad.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os
import secrets

app = FastAPI(title="Sistema de Autenticación OAuth2")

# Clave secreta obtenida de una variable de entorno
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    secrets.token_urlsafe(32)
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usuario de prueba
USUARIO = "ana"
PASSWORD = "secreta"

# Esquema OAuth2 para recibir el token Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Función para generar el token JWT
def crear_token(usuario: str):

    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos_token = {
        "usuario": usuario,
        "exp": expiracion
    }

    token = jwt.encode(
        datos_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# Ruta para iniciar sesión mediante formulario
@app.post("/token")
def iniciar_sesion(
    datos: OAuth2PasswordRequestForm = Depends()
):

    # Comprobar usuario y contraseña
    if datos.username != USUARIO or datos.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generar el token
    access_token = crear_token(datos.username)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Función para comprobar el token recibido
def obtener_usuario(token: str = Depends(oauth2_scheme)):

    try:
        # Verificar firma y fecha de expiración
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario = payload.get("usuario")

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return usuario

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o vencido",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Ruta protegida que necesita un token Bearer
@app.get("/api/perfil")
def consultar_perfil(
    usuario: str = Depends(obtener_usuario)
):

    return {"usuario": usuario}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de acceso no autorizado sin token (HTTP 401)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
>La IA proporcionó una implementación utilizando FastAPI y las herramientas OAuth2PasswordRequestForm y OAuth2PasswordBearer.

El código permite recibir los datos de inicio de sesión mediante un formulario, comprobar las credenciales y generar un token JWT firmado. También valida el encabezado Authorization: Bearer para proteger la ruta del perfil.

Además, se agregó el manejo de errores HTTP 401 para rechazar solicitudes sin token o con un esquema de autenticación diferente. 

---
**Firma digital:** [Javier Alexander2001]
