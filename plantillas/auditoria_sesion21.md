# Bitácora de Requerimientos y Auditoría IA — Sesión 21
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Conexión manual y ejecución de sentencias SQL  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue lograr que los libros se guardaran correctamente en una base de datos SQLite. Al principio utilicé una lista de Python para almacenar la información, pero comprendí que los datos se perdían cuando se reiniciaba el servidor. También tuve dificultades para establecer correctamente la conexión con la base de datos y ejecutar las consultas SQL.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 y FastAPI en Google Colab, utilizando SQLite mediante el módulo sqlite3. |
| **Rol (R)** | Desarrollador especializado en Python, FastAPI y bases de datos SQL, encargado de implementar una API REST funcional. |
| **Especificación (E)** | Crear automáticamente la tabla libros, implementar POST /api/libros para insertar registros con HTTP 201 y GET /api/libros para consultar los registros con HTTP 200. Utilizar consultas SQL parametrizadas y guardar los cambios mediante commit(). |
| **Output (O)** | Código completo y comentado para app.py, con conexión a SQLite, creación automática de la tabla y rutas funcionales que cumplan el verificador del profesor. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador especializado en Python,
FastAPI y bases de datos SQLite.

Necesito implementar una API REST para administrar
libros y guardar la información permanentemente.

Requisitos:
1. Crear automáticamente la base de datos biblioteca.db.
2. Crear la tabla libros si todavía no existe.
3. Implementar POST /api/libros para registrar libros.
4. Recibir los campos titulo y anio.
5. Responder HTTP 201 con el id, titulo y anio.
6. Implementar GET /api/libros para consultar los libros.
7. Responder HTTP 200 con una lista de registros.
8. Utilizar consultas SQL parametrizadas.
9. Ejecutar commit() para guardar los cambios.
10. No utilizar listas de Python como almacenamiento.

Entrega el código completo de app.py, organizado,
comentado y compatible con Google Colab.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Biblioteca con SQLite")

DATABASE = "biblioteca.db"


# Modelo del libro
class Libro(BaseModel):
    titulo: str
    anio: int


# Crear conexión y tabla automáticamente
def conectar():
    conexion = sqlite3.connect(DATABASE)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            anio INTEGER NOT NULL
        )
    """)

    conexion.commit()
    return conexion


# Registrar un libro
@app.post("/api/libros", status_code=201)
def agregar_libro(libro: Libro):

    conexion = conectar()

    cursor = conexion.execute(
        "INSERT INTO libros (titulo, anio) VALUES (?, ?)",
        (libro.titulo, libro.anio)
    )

    nuevo_id = cursor.lastrowid
    conexion.commit()
    conexion.close()

    return {
        "id": nuevo_id,
        "titulo": libro.titulo,
        "anio": libro.anio
    }


# Consultar libros
@app.get("/api/libros")
def listar_libros():

    conexion = conectar()
    conexion.row_factory = sqlite3.Row

    filas = conexion.execute(
        "SELECT id, titulo, anio FROM libros ORDER BY id"
    ).fetchall()

    libros = [dict(fila) for fila in filas]

    conexion.close()

    return {"libros": libros}
```

---
## Evidencia Verificador
### 1

==============================================================================

VERIFICACIÓN DEL RESULTADO · 3 casos · app.py

==============================================================================

✅ 01. La base inicia sin libros

✅ 02. El libro se inserta en SQLite

✅ 03. El listado lee la base

------------------------------------------------------------------------------

RESULTADO: 3/3 casos correctos. ¡Resultado logrado!


### 2

✅ La fila existe en el archivo SQLite

------------------------------------------------------------------------------

RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!




## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de recuperación ante desconexión de DB

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La primera versión del código presentó errores HTTP 500 en los tres casos de prueba. Al principio no había considerado que un problema en la conexión o inicialización de SQLite podía provocar que todas las operaciones fallaran.

Para corregirlo, modifiqué la implementación y creé una función llamada conectar(), que se encarga de abrir la conexión y comprobar que la tabla exista antes de realizar las consultas. También revisé que las consultas estuvieran parametrizadas y que los cambios se guardaran con commit().

Finalmente, el verificador mostró que los tres casos funcionaban correctamente: la base iniciaba vacía, el libro Rayuela se insertaba con el ID 1 y el listado recuperaba la información desde SQLite.


---
**Firma digital:** [Javier Alexander2001]
