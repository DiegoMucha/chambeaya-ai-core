# Documentación de módulos y endpoints IA

## Carpeta `filter_match`
Esta carpeta contiene los endpoints para el preprocesamiento de datos, es decir, la generación de embeddings a partir de la información cruda de ofertas de trabajo y estudiantes. No realiza matching, solo transforma los datos en vectores útiles para el modelo de IA.

### `filter_job_offer.py`
- **/filter/job_offer/preprocess_job_offer**
  - **POST**
  - Recibe: Un JSON con los datos de una oferta de trabajo (`Job_offer`).
  - Devuelve: El embedding generado para esa oferta y metadatos.
- **/filter/job_offer/preprocess_all_job_offer**
  - **POST**
  - Recibe: Una lista de ofertas de trabajo.
  - Devuelve: Una lista de embeddings para cada oferta.

### `filter_student.py`
- **/filter/student/preprocess_student**
  - **POST**
  - Recibe: Un JSON con los datos de un estudiante (`Estudiante`).
  - Devuelve: El embedding generado para ese estudiante y metadatos.
- **/filter/student/preprocess_all_student**
  - **POST**
  - Recibe: Una lista de estudiantes.
  - Devuelve: Una lista de embeddings para cada estudiante.

**Funcionamiento:**
- Estos endpoints esperan recibir los datos en el body de la petición (JSON).
- El preprocesador transforma los datos en texto y luego en vectores numéricos (embeddings) usando modelos de lenguaje.
- No acceden a base de datos ni almacenan información, solo procesan y devuelven el resultado.

---

## Carpeta `match_job_student`
Esta carpeta contiene los endpoints para realizar el matching entre estudiantes y ofertas de trabajo, usando los embeddings generados previamente.

### `match_job_offer.py`
- **/aimodel/job_offer/matching_offers**
  - **POST**
  - Recibe: Un estudiante y una oferta de trabajo.
  - Devuelve: El resultado del matching entre ese estudiante y esa oferta (score, ranking, etc.).

### `match_student.py`
- **/aimodel/student/best_students**
  - **POST**
  - Recibe: Una oferta de trabajo.
  - Devuelve: Los mejores estudiantes para esa oferta, ordenados por score.
- **/aimodel/student/best_job_offers**
  - **POST**
  - Recibe: Un estudiante.
  - Devuelve: Las mejores ofertas para ese estudiante, ordenadas por score.

**Funcionamiento:**
- Estos endpoints reciben los datos ya preprocesados o crudos (según el endpoint).
- Usan el modelo de IA para calcular la similitud entre embeddings y devolver los mejores matches.
- No acceden a base de datos ni almacenan información, solo procesan y devuelven el resultado.

---

**Resumen:**
- `filter_match`: Preprocesa y vectoriza datos.
- `match_job_student`: Realiza el matching entre estudiantes y ofertas usando los vectores.

Ambos módulos esperan recibir los datos desde un backend externo, que es el responsable de obtenerlos de la base de datos y enviarlos a esta API de IA.
