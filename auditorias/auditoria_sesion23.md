# Bitácora de Requerimientos y Auditoría IA — Sesión 23
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Operaciones CRUD Transaccionales y Async Sessions  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Operaciones de inserción y consulta manual  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue procesar las solicitudes HTTP y conectar correctamente las operaciones con la base de datos. También fue necesario validar que los datos enviados fueran correctos y comprobar si el libro existía antes de actualizarlo o eliminarlo. Al hacerlo manualmente, es fácil cometer errores al manejar las respuestas y los códigos HTTP.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Trabajo con Python 3.10+, FastAPI 0.110+ y SQLite. Utilizo SQLAlchemy con AsyncSession y aiosqlite para realizar operaciones asíncronas. |
| **Rol (R)** | La IA debe actuar como un desarrollador especializado en Python, FastAPI y diseño de APIs RESTful. |
| **Especificación (E)** | Implementar un CRUD asíncrono para libros: crear, listar, consultar por ID, actualizar y eliminar. Utilizar create_async_engine, AsyncSession, async def, await y commit. Devolver 201 al crear, 200 al consultar o actualizar, 204 al eliminar y 404 cuando el libro no exista. |
| **Output (O)** | Código completo y organizado para app.py, con modelos, esquemas y rutas que funcionen con el verificador de la actividad. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador especializado en Python y FastAPI.

Necesito implementar una API REST para administrar libros utilizando
FastAPI, SQLAlchemy, SQLite, aiosqlite y AsyncSession.

El código debe utilizar create_async_engine, async_sessionmaker,
async def y await para realizar las operaciones de manera asíncrona.

Implementa las siguientes rutas:
- POST /api/libros: registrar un libro y responder 201.
- GET /api/libros: mostrar todos los libros y responder 200.
- GET /api/libros/{id}: consultar un libro y responder 200.
- PUT /api/libros/{id}: actualizar un libro y responder 200.
- DELETE /api/libros/{id}: eliminar un libro y responder 204.

Si un libro no existe, la API debe responder 404.
Utiliza esquemas Pydantic para validar los datos y realiza
los commit necesarios en las operaciones de escritura.

Asegúrate de que la base de datos y sus tablas estén preparadas
antes de procesar las solicitudes HTTP.

Entrega el código completo de app.py, organizado y comentado,
sin modificar el verificador oficial de la actividad.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Integer, String, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Conexion asincrona con SQLite
DATABASE_URL = "sqlite+aiosqlite:///./biblioteca.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 2. Modelo de base de datos
class Base(DeclarativeBase):
    pass


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    titulo: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    anio: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


# 3. Modelos de entrada y salida
class LibroEntrada(BaseModel):
    titulo: str
    anio: int


class LibroSalida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    anio: int


# 4. Crear la aplicacion
app = FastAPI(title="CRUD asincrono de libros")

tablas_creadas = False


# 5. Preparar la base de datos antes de atender peticiones
@app.middleware("http")
async def preparar_base_datos(request, call_next):
    global tablas_creadas

    if not tablas_creadas:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        tablas_creadas = True

    response = await call_next(request)
    return response


# 6. POST: Crear libro
@app.post(
    "/api/libros",
    response_model=LibroSalida,
    status_code=201
)
async def crear_libro(datos: LibroEntrada):

    async with SessionLocal() as session:

        libro = Libro(
            titulo=datos.titulo,
            anio=datos.anio
        )

        session.add(libro)

        await session.commit()
        await session.refresh(libro)

        return libro


# 7. GET: Listar libros
@app.get("/api/libros")
async def listar_libros():

    async with SessionLocal() as session:

        resultado = await session.execute(
            select(Libro).order_by(Libro.id)
        )

        libros = resultado.scalars().all()

        return {"libros": libros}


# 8. GET: Consultar libro por ID
@app.get(
    "/api/libros/{libro_id}",
    response_model=LibroSalida
)
async def obtener_libro(libro_id: int):

    async with SessionLocal() as session:

        libro = await session.get(Libro, libro_id)

        if libro is None:
            raise HTTPException(
                status_code=404,
                detail="Libro no encontrado"
            )

        return libro


# 9. PUT: Actualizar libro
@app.put(
    "/api/libros/{libro_id}",
    response_model=LibroSalida
)
async def actualizar_libro(
    libro_id: int,
    datos: LibroEntrada
):

    async with SessionLocal() as session:

        libro = await session.get(Libro, libro_id)

        if libro is None:
            raise HTTPException(
                status_code=404,
                detail="Libro no encontrado"
            )

        libro.titulo = datos.titulo
        libro.anio = datos.anio

        await session.commit()
        await session.refresh(libro)

        return libro


# 10. DELETE: Eliminar libro
@app.delete(
    "/api/libros/{libro_id}",
    status_code=204
)
async def eliminar_libro(libro_id: int):

    async with SessionLocal() as session:

        libro = await session.get(Libro, libro_id)

        if libro is None:
            raise HTTPException(
                status_code=404,
                detail="Libro no encontrado"
            )

        await session.delete(libro)
        await session.commit()

    return Response(status_code=204)
```

---
## Evidencia Verificador 

### 1

==============================================================================

VERIFICACIÓN DEL RESULTADO · 5 casos · app.py

==============================================================================

✅ 01. Crear un libro

✅ 02. Listar los libros

✅ 03. Actualizar el libro

✅ 04. Eliminar el libro

✅ 05. El libro eliminado ya no existe

------------------------------------------------------------------------------

### 2

✅ La persistencia es asíncrona

------------------------------------------------------------------------------

RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!


RESULTADO: 5/5 casos correctos. ¡Resultado logrado!
## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de inserción doble y manejo de llaves únicas

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> El principal problema que encontré fue que el verificador devolvía errores HTTP 500 porque las tablas de la base de datos no estaban creadas cuando llegaban las solicitudes. La IA no había considerado inicialmente ese detalle. Para corregirlo, se agregó una preparación de la base de datos mediante un middleware, de manera que las tablas estuvieran listas antes de procesar las peticiones. También se mantuvo el manejo del código 404 para los libros que no existen.

---
**Firma digital:** [Javier Alexander2001]
