# Bitácora de Requerimientos y Auditoría IA — Sesión 17
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Control de Acceso Basado en Roles (RBAC)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Verificación manual de permisos de usuario (Admin/User)  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue comprobar que cada usuario tuviera los permisos correctos. También fue necesario revisar que el administrador pudiera entrar al panel y que un usuario normal no tuviera acceso. Se me complicó diferenciar los errores de autenticación (401) y los de permisos (403).

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 y FastAPI en Google Colab, utilizando JWT para la autenticación y control de acceso por roles. |
| **Rol (R)** | Desarrollador especializado en Python, FastAPI y seguridad de aplicaciones web. |
| **Especificación (E)** | Crear los usuarios admin y ana, generar tokens JWT con sus respectivos roles, permitir que ambos consulten /api/ perfil y restringir /api/ admin/panel únicamente al administrador. Responder HTTP 401 cuando no exista un token válido y HTTP 403 cuando el usuario no tenga permisos. |
| **Output (O)** | Archivo app.py completo, comentado y funcional, con las rutas de autenticación, perfil y panel administrativo, cumpliendo los seis criterios del verificador. |

### 2.2 Prompt Estructurado
```text
Quiero que me ayudes a realizar la actividad de la Sesión 17 sobre Control de Acceso Basado en Roles (RBAC). Estoy trabajando con Python y FastAPI en Google Colab y utilizando JWT para la autenticación.

Actúa como un desarrollador especializado en Python, FastAPI y seguridad de aplicaciones web.

Necesito crear un sistema con dos usuarios: admin, con contraseña admin123 y rol admin; y ana, con contraseña secreta y rol user. Ambos usuarios deben poder iniciar sesión, obtener su token JWT y consultar su perfil mediante la ruta /api/perfil. Solamente el administrador debe tener acceso a /api/admin/panel.

También necesito que el sistema distinga entre los errores HTTP 401, cuando no existe un token válido, y HTTP 403, cuando el usuario está autenticado, pero no tiene permisos para acceder.

Quiero que me entregues el código completo de app.py, con comentarios y explicaciones sencillas, respetando los requisitos de la actividad y cumpliendo los seis casos de verificación.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
import os
import secrets

# Crear aplicación FastAPI
app = FastAPI(title="Sistema de Control de Acceso RBAC")

# Configuración del token JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usuarios de prueba y sus roles
usuarios = {
    "admin": {"password": "admin123", "rol": "admin"},
    "ana": {"password": "secreta", "rol": "user"}
}


# Modelo para recibir los datos de inicio de sesión
class DatosLogin(BaseModel):
    usuario: str
    password: str


# Configuración de autenticación OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


# Crear un token con el usuario y su rol
def crear_token(username: str, rol: str):

    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos = {
        "usuario": username,
        "rol": rol,
        "exp": expiracion
    }

    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


# Obtener token al iniciar sesión
@app.post("/api/token")
def iniciar_sesion(datos: DatosLogin):

    usuario = usuarios.get(datos.usuario)

    # Comprobar usuario y contraseña
    if not usuario or usuario["password"] != datos.password:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generar token JWT
    access_token = crear_token(
        datos.usuario,
        usuario["rol"]
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Validar token y recuperar los datos del usuario
def obtener_usuario(token: str = Depends(oauth2_scheme)):

    try:
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = datos.get("usuario")
        rol = datos.get("rol")

        # Comprobar que el usuario y el rol sean correctos
        if username not in usuarios or rol != usuarios[username]["rol"]:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {
            "usuario": username,
            "rol": rol
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o vencido",
            headers={"WWW-Authenticate": "Bearer"}
        )


# Consultar perfil: cualquier usuario autenticado puede entrar
@app.get("/api/perfil")
def consultar_perfil(usuario: dict = Depends(obtener_usuario)):

    return {
        "usuario": usuario["usuario"],
        "rol": usuario["rol"]
    }


# Verificar que el usuario tenga rol de administrador
def verificar_admin(usuario: dict = Depends(obtener_usuario)):

    if usuario["rol"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para acceder al panel administrativo"
        )

    return usuario


# Panel administrativo: solamente para administradores
@app.get("/api/admin/panel")
def panel_admin(usuario: dict = Depends(verificar_admin)):

    return {
        "panel": "admin"
    }


```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de acceso denegado por rol insuficiente (HTTP 403)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante la verificación se encontraron errores HTTP 404 y 422. El primero ocurrió porque la ruta de inicio de sesión no coincidía con la que esperaba el verificador. El segundo se presentó porque el código esperaba el campo username, pero las pruebas enviaban el campo usuario.
> Para corregirlo se modificó la ruta a /api/token y se adaptó el modelo de inicio de sesión para recibir el campo usuario. También se mantuvo la validación de permisos para diferenciar entre los errores 401 y 403.

---
**Firma digital:** [Javier Alexander2001]
