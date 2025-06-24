# Chambea Ya - Repositorio para IA

### Este repositorio contiene toda la información y códigos para los modelos de IA de Chambea Ya.

# Después de instalar lo de requirements.txt
Colocar: !python -m spacy download es_core_news_sm

### Acerca de la conexión con el backend ###
Base de datos
---
La base de datos está en PostgreSQL y ya contiene toda la estructura de entidades como student, job_offer, company, skill, interest, etc.

Tanto la tabla student como job_offer incluyen un campo embedding (JSONB) que contiene un vector de floats TF-IDF de longitud 500 generado a partir de su descripción, intereses y habilidades.

Los embeddings se utilizan para comparar similitud entre perfiles usando técnicas de machine learning (principalmente KNN).

La tabla filter_match guarda el estado del filtrado por etapa para cada job_offer, sin incluir datos del estudiante, ya que el filtrado solo se aplica a las ofertas.

La tabla match_job_student guarda los top N matches entre un estudiante y las ofertas, incluyendo el score (similitud), el rank y la fecha del match.

Lógica del sistema
---
Cuando se crea un estudiante:

Se vectoriza su descripción y perfil (TF-IDF).

El embedding se guarda directamente en la columna embedding de la tabla student.

Las ofertas laborales ya vienen vectorizadas y guardadas en su propia tabla (job_offer.embedding).

El sistema aplica un filtro inicial a las ofertas (filter_match) por etapas (como modalidad, área, experiencia, etc.) y guarda el resultado por job_offer_id y stage.

Luego se ejecuta un algoritmo de KNN entre el vector del estudiante (1x500) y las ofertas filtradas (Nx500) para determinar las más similares.

Los top 5 resultados se guardan en la tabla match_job_student junto con su score y posición (rank).

Reglas importantes
---
No se crean tablas adicionales para eficiencia; todo está contenido en las tablas ya mencionadas.

El campo embedding se maneja como JSONB por flexibilidad y bajo costo.

El vector del estudiante solo se actualiza si edita su perfil (no se recalcula en cada match).

El sistema evita recalcular embeddings a cada rato, priorizando rendimiento y bajo costo computacional.

No se almacena model_score ni filtered_at en filter_match para no cargarla innecesariamente.

