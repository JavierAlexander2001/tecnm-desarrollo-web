# Bitácora de Requerimientos y Auditoría IA — Sesión 12
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Inyección de Dependencias (FastAPI Depends / PHP Container)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Inyector de dependencias manual por funciones  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue organizar el almacenamiento de los libros y hacer que los endpoints utilizaran el mismo repositorio. Al principio utilicé una lista directamente, pero no tenía implementada la inyección de dependencias ni la validación correcta de los datos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3 y FastAPI en Google Colab.|
| **Rol (R)** | Asistente de programación para desarrollar una API RESTful sencilla. |
| **Especificación (E)** | Crear un repositorio en memoria utilizando la clase RepositorioMemoria y la función get_repositorio(). Inyectarlo en los endpoints mediante Depends(). Validar los datos con Pydantic. |
| **Output (O)** | Archivo app.py con código funcional, modelos de validación, repositorio y endpoints con sus códigos HTTP correspondientes.|

### 2.2 Prompt Estructurado
```text
Actúa como un asistente de programación especializado
en Python y FastAPI.

Necesito desarrollar una API para la sesión 12 de
Desarrollo de Aplicaciones Web.

El objetivo es implementar inyección de dependencias
utilizando Depends de FastAPI.

Requisitos:

1. Crear una clase llamada RepositorioMemoria.
2. Crear una función get_repositorio() que devuelva
   una instancia del repositorio.
3. Utilizar Depends(get_repositorio) en los endpoints.
4. Crear GET /api/diagnostico que devuelva el nombre
   del repositorio utilizado.
5. Crear POST /api/libros con respuesta HTTP 201.
6. Crear GET /api/libros con respuesta HTTP 200.
7. Validar los datos con Pydantic para que los datos
   incorrectos devuelvan HTTP 422.
8. Mantener los libros guardados en memoria.

Entrega el código completo en un archivo app.py,
con una estructura sencilla y fácil de entender.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field


app = FastAPI(title="Biblioteca API")


# Modelo para validar los datos
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=1)
    anio: int


# Repositorio que guarda los libros en memoria
class RepositorioMemoria:

    def __init__(self):
        self.libros = []
        self.contador = 1

    def crear_libro(self, libro):
        nuevo_libro = {
            "id": self.contador,
            "titulo": libro.titulo,
            "anio": libro.anio
        }

        self.libros.append(nuevo_libro)
        self.contador += 1

        return nuevo_libro

    def obtener_libros(self):
        return self.libros


# Instancia del repositorio
repositorio = RepositorioMemoria()


# Función de inyección de dependencia
def get_repositorio():
    return repositorio


# Diagnóstico
@app.get("/api/diagnostico")
def diagnostico(
    repo: RepositorioMemoria = Depends(get_repositorio)
):
    return {
        "repositorio": repo.__class__.__name__
    }


# Registrar libros
@app.post("/api/libros", status_code=201)
def crear_libro(
    libro: LibroEntrada,
    repo: RepositorioMemoria = Depends(get_repositorio)
):
    return repo.crear_libro(libro)


# Consultar libros
@app.get("/api/libros")
def obtener_libros(
    repo: RepositorioMemoria = Depends(get_repositorio)
):
    return {
        "libros": repo.obtener_libros()
    }
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de ciclo de vida de dependencias por request

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante las primeras pruebas se detectó que el registro de libros devolvía HTTP 200 en lugar de HTTP 201. También se aceptaban datos incorrectos en el año del libro, cuando deberían generar un error HTTP 422.

Para corregirlo se agregó el código de estado 201 en el endpoint POST y se utilizó un modelo Pydantic para validar los datos recibidos. También se corrigió el nombre del repositorio que aparecía en el diagnóstico.

---
**Firma digital:** [Javier Alexander2001]
