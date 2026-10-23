# Bitácora de Requerimientos y Auditoría IA — Sesión 03
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Headers, Content-Type y Negociación de Contenido  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Javier Alexander Aviles Darza]  
**Matrícula:** [23531054]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lectura y emisión manual de encabezados HTTP  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue entender cómo revisar los encabezados de una petición y comprobar si los datos que manda el cliente están en el formato correcto. También tuve que aprender la diferencia entre Content-Type y Accept, porque uno indica el formato que envío y el otro el formato que quiero recibir.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Estoy trabajando en Google Colab con Python y FastAPI para crear una API de libros. |
| **Rol (R)** | Quiero que la IA me ayude a desarrollar una API y validar correctamente los encabezados HTTP. |
| **Especificación (E)** | Crear las rutas POST y GET para libros. El POST solo acepta JSON y devuelve 415 si el formato no es compatible. El GET devuelve 406 si el cliente solicita XML. Las respuestas correctas deben usar JSON, con código 201 al crear un libro y 200 al consultar la lista. |
| **Output (O)** | Obtener el archivo app.py, pasar las cuatro pruebas de verificación y completar la bitácora de auditoría. |

### 2.2 Prompt Estructurado
```text
[Pega aquí el prompt formal que redactaste para la IA]
```

---

## 3. Código Devuelto por el Modelo
```python
# Código devuelto por el LLM
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas con tipos de contenido no soportados (415)

* [ ] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ ] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ ] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> 

---
**Firma digital:** [Usuario de GitHub]
