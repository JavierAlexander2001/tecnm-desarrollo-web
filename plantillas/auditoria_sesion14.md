# Bitácora de Requerimientos y Auditoría IA — Sesión 14
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Hashing Seguro de Contraseñas (Bcrypt / Argon2)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Cifrado manual con Salting y Factor de Costo  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La principal dificultad que encontré fue proteger las contraseñas al momento de registrar un usuario. En mi primera implementación guardaba las contraseñas directamente y las comparaba sin utilizar un método de seguridad. También tuve problemas para validar los datos y evitar que un usuario registrado pudiera sobrescribir su contraseña.

Después comprendí que debía utilizar bcrypt para generar un hash y verificar las contraseñas sin necesidad de guardar la contraseña original.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 y FastAPI en Google Colab. Se utiliza bcrypt para proteger las contraseñas y almacenamiento de usuarios en memoria. |
| **Rol (R)** | Desarrollador de aplicaciones web especializado en APIs REST, Python, FastAPI y seguridad de contraseñas. |
| **Especificación (E)** | Implementar POST /api/registro para recibir usuario y contraseña, generar un hash con bcrypt y guardar solamente el hash. Implementar POST /api/login para verificar la contraseña. El registro debe responder HTTP 201, el login correcto HTTP 200 y la contraseña incorrecta HTTP 401. No se debe mostrar la contraseña ni el hash. Los usuarios repetidos no deben sobrescribir los datos existentes. |
| **Output (O)** | Código completo de app.py, organizado y comentado, utilizando FastAPI, Pydantic y bcrypt, con las respuestas HTTP solicitadas. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador de aplicaciones web
especializado en Python, FastAPI y seguridad informática.

Necesito implementar un sistema de registro e inicio
de sesión utilizando bcrypt para proteger las contraseñas.

El sistema debe cumplir los siguientes requisitos:

1. Crear POST /api/registro para recibir usuario y password.

2. Generar un hash seguro utilizando bcrypt y guardar
   solamente el hash en el servidor.

3. El registro debe responder HTTP 201 y devolver
   únicamente el nombre del usuario.

4. Crear POST /api/login para verificar las credenciales
   utilizando bcrypt.checkpw().

5. Si la contraseña es correcta, responder HTTP 200
   con usuario y autenticado: true.

6. Si la contraseña es incorrecta, responder HTTP 401.

7. Evitar que un usuario repetido sobrescriba
   la contraseña existente.

8. Nunca devolver la contraseña original ni el hash
   en las respuestas de la API.

Entrega el código completo de app.py, organizado,
comentado y funcional, utilizando FastAPI y Pydantic.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt

app = FastAPI(title="Sistema Seguro de Registro y Login")

# Almacenamiento de usuarios en memoria
usuarios = {}


# Modelo para recibir los datos
class Usuario(BaseModel):
    usuario: str
    password: str


# Ruta para registrar usuarios
@app.post("/api/registro", status_code=201)
def registro(datos: Usuario):

    # Comprobar si el usuario ya existe
    if datos.usuario in usuarios:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya está registrado"
        )

    # Convertir la contraseña a bytes
    password_bytes = datos.password.encode("utf-8")

    # Generar hash seguro con bcrypt
    password_hash = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    # Guardar solamente el hash
    usuarios[datos.usuario] = password_hash

    # Responder sin mostrar la contraseña ni el hash
    return {"usuario": datos.usuario}


# Ruta para iniciar sesión
@app.post("/api/login")
def login(datos: Usuario):

    # Comprobar si el usuario existe
    if datos.usuario not in usuarios:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    # Recuperar el hash almacenado
    password_hash = usuarios[datos.usuario]

    # Verificar la contraseña
    password_correcta = bcrypt.checkpw(
        datos.password.encode("utf-8"),
        password_hash
    )

    if not password_correcta:
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    return {
        "usuario": datos.usuario,
        "autenticado": True
    }

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas contra ataques de Rainbow Tables y Timing

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En mi primera implementación encontré problemas de seguridad porque guardaba la contraseña directamente y también la devolvía en la respuesta del registro. Además, no utilizaba un algoritmo de hashing ni controlaba correctamente las contraseñas incorrectas.

Con ayuda de la IA corregí estos problemas utilizando bcrypt, hashpw() y checkpw(). También agregué una validación para evitar que los usuarios repetidos sobrescribieran sus contraseñas.

La verificación permite comprobar que la API no muestre la contraseña original ni el hash y que responda con los códigos HTTP solicitados.

---
**Firma digital:** [Javier Alexander2001]
