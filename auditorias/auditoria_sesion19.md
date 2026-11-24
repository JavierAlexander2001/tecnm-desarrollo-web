# Bitácora de Requerimientos y Auditoría IA — Sesión 19
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Sanitización de Entradas, Prevención de XSS e Inyecciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Nombre Completo]  
**Matrícula:** [No. de Control]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Limpieza manual de HTML y caracteres especiales  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue evitar que las etiquetas HTML enviadas por los usuarios se guardaran directamente en la aplicación. Al principio no sabía cómo impedir que un código como <script>alert(1)</script> pudiera ejecutarse. Después investigué y utilicé la función html.escape() para convertir los caracteres especiales en texto seguro.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python con FastAPI, utilizando Google Colab y las librerías Pydantic y html.|
| **Rol (R)** |Desarrollador backend especializado en APIs RESTful y seguridad web. |
| **Especificación (E)** | Crear las rutas POST /api/comentarios y GET /api/comentarios. Recibir comentarios, escapar caracteres HTML peligrosos y devolver respuestas seguras con códigos HTTP 201 y 200. |
| **Output (O)** | Archivo app.py con código funcional, organizado y compatible con el verificador HTTP de la actividad. |

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador backend especializado en
Python, FastAPI y seguridad web.

Necesito implementar una API de comentarios que
prevenga ataques XSS mediante el escape de HTML.

Requisitos:
1. Crear POST /api/comentarios para recibir comentarios.
2. Responder con HTTP 201 al guardar un comentario.
3. Utilizar html.escape() para neutralizar etiquetas HTML.
4. Crear GET /api/comentarios para listar los comentarios.
5. Responder con HTTP 200 al consultar los comentarios.
6. Mantener los comentarios normales sin modificaciones.
7. Utilizar Pydantic para validar los datos recibidos.
8. Evitar que se devuelvan etiquetas script sin escapar.

Entrega el código completo en un archivo app.py,
utilizando FastAPI y Python.
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI
from pydantic import BaseModel
import html

app = FastAPI(title="API segura de comentarios")

comentarios = []

class Comentario(BaseModel):
    texto: str

@app.post("/api/comentarios", status_code=201)
def crear_comentario(datos: Comentario):
    texto_seguro = html.escape(datos.texto)

    nuevo = {
        "id": len(comentarios) + 1,
        "texto": texto_seguro
    }

    comentarios.append(nuevo)

    return nuevo


@app.get("/api/comentarios")
def listar_comentarios():
    return {"comentarios": comentarios}
```

---
## Evidencia Verificador 

==============================================================================

VERIFICACIÓN DEL RESULTADO · 3 casos · app.py

==============================================================================

✅ 01. Un comentario normal se guarda

✅ 02. El script se neutraliza

✅ 03. El listado tampoco devuelve scripts

------------------------------------------------------------------------------

RESULTADO: 3/3 casos correctos. ¡Resultado logrado!


## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de inyección de scripts en payloads

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La primera versión del código no escapaba los caracteres HTML, por lo que permitía guardar etiquetas peligrosas como <script>. También observé que era necesario proteger la ruta GET para evitar que el listado devolviera contenido sin escapar.
> Corregí estos problemas utilizando html.escape() antes de guardar los comentarios. Después ejecuté las pruebas del verificador para comprobar que los comentarios normales siguieran funcionando y que los scripts fueran neutralizados.

---
**Firma digital:** [Javier Alexander2001]
