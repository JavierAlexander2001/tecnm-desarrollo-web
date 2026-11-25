# Bitácora de Requerimientos y Auditoría IA — Sesión 22
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Modelado Relacional (1:1, 1:N, N:M) con ORMs  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Definición de tablas relacionales en código  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue organizar la información de los autores y los libros sin utilizar un ORM. Al principio, relacionar los datos manualmente era más complicado porque tenía que comprobar que cada libro perteneciera al autor correcto. También me di cuenta de que, si utilizaba solamente listas de Python, los datos podían perderse al reiniciar el programa y no tenía la misma seguridad que ofrece una base de datos con llaves foráneas.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3, FastAPI y SQLAlchemy utilizando SQLite en Google Colab. |
| **Rol (R)** | Desarrollador especializado en APIs RESTful con Python y manejo de bases de datos. |
| **Especificación (E)** | Crear los modelos Autor y Libro con una relación uno a muchos (1:N), utilizando ForeignKey y relationship. Implementar los endpoints para registrar autores, registrar libros, consultar un autor con sus libros y listar todos los libros. |
| **Output (O)** | Código completo en app.py, modelos ORM, conexión a SQLite, validación de autores y respuestas HTTP correctas. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador experto en Python, FastAPI y SQLAlchemy.

Necesito crear una API REST para una biblioteca utilizando SQLite
y SQLAlchemy como ORM.

Contexto:
El proyecto debe manejar dos modelos: Autor y Libro.

Especificaciones:
1. Crear el modelo Autor con id y nombre.
2. Crear el modelo Libro con id, titulo, anio y autor_id.
3. Establecer una relación uno a muchos (1:N), donde un autor
   pueda tener varios libros.
4. Utilizar ForeignKey("autores.id") y relationship().
5. Crear POST /api/autores con respuesta 201.
6. Crear POST /api/autores/{autor_id}/libros con respuesta 201.
7. Crear GET /api/autores/{autor_id} para consultar al autor
   junto con sus libros.
8. Crear GET /api/libros para listar todos los libros.
9. Comprobar que el autor exista antes de registrar un libro.
10. Utilizar sesiones de SQLAlchemy y cerrar las conexiones
    correctamente.
11. Manejar los errores con códigos HTTP adecuados.

Entrega el código completo en app.py, organizado y comentado,
utilizando FastAPI, SQLAlchemy, Pydantic y SQLite.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session

# Configuracion de la base de datos
DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Activar llaves foraneas en SQLite
@event.listens_for(engine, "connect")
def activar_llaves_foreign_key(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

app = FastAPI(title="Biblioteca con relaciones ORM")


# MODELOS ORM

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    libros = relationship(
        "Libro",
        back_populates="autor",
        cascade="all, delete-orphan"
    )


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    anio = Column(Integer, nullable=False)

    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)

    autor = relationship("Autor", back_populates="libros")


# CREAR TABLAS AUTOMATICAMENTE
Base.metadata.create_all(bind=engine)


# MODELOS DE ENTRADA

class AutorEntrada(BaseModel):
    nombre: str


class LibroEntrada(BaseModel):
    titulo: str
    anio: int


# CONEXION A LA BASE DE DATOS

def obtener_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREAR AUTOR

@app.post("/api/autores", status_code=201)
def crear_autor(datos: AutorEntrada, db: Session = Depends(obtener_db)):

    autor = Autor(nombre=datos.nombre)

    db.add(autor)
    db.commit()
    db.refresh(autor)

    return {
        "id": autor.id,
        "nombre": autor.nombre
    }


# CREAR LIBRO ASOCIADO A UN AUTOR

@app.post("/api/autores/{autor_id}/libros", status_code=201)
def crear_libro(
    autor_id: int,
    datos: LibroEntrada,
    db: Session = Depends(obtener_db)
):

    autor = db.query(Autor).filter(Autor.id == autor_id).first()

    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    libro = Libro(
        titulo=datos.titulo,
        anio=datos.anio,
        autor=autor
    )

    db.add(libro)
    db.commit()
    db.refresh(libro)

    return {
        "id": libro.id,
        "titulo": libro.titulo,
        "anio": libro.anio,
        "autor_id": libro.autor_id
    }


# CONSULTAR AUTOR Y SUS LIBROS

@app.get("/api/autores/{autor_id}")
def consultar_autor(autor_id: int, db: Session = Depends(obtener_db)):

    autor = db.query(Autor).filter(Autor.id == autor_id).first()

    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")

    return {
        "id": autor.id,
        "nombre": autor.nombre,
        "libros": [
            {
                "id": libro.id,
                "titulo": libro.titulo
            }
            for libro in autor.libros
        ]
    }


# LISTAR TODOS LOS LIBROS

@app.get("/api/libros")
def listar_libros(db: Session = Depends(obtener_db)):

    libros = db.query(Libro).all()

    return {
        "libros": [
            {
                "id": libro.id,
                "titulo": libro.titulo
            }
            for libro in libros
        ]
    }
```

---
## Evidencia Verificador 

### 1

==============================================================================

VERIFICACIÓN DEL RESULTADO · 4 casos · app.py

==============================================================================

✅ 01. Se crea el autor

✅ 02. Se crea el libro asociado

✅ 03. El autor devuelve sus libros

✅ 04. El listado de libros funciona

------------------------------------------------------------------------------

RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

### 2

✅ La relación ORM está declarada

------------------------------------------------------------------------------

RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!



## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de integridad referencial y cascadas

* [ ] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ ] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ ] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> 

---
**Firma digital:** [Usuario de GitHub]
