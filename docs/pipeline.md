# Chambea Ya - AI Model Pipeline

## 1. Ingesta de datos
- Se generaron los datos de ejemplo con IA (ChatGPT)
- En total son 5000 mypes y 20000 estudiantes simulados.
- Se guardaron en 2 archivos .csv, que son: estudiantes.csv y mypes.csv

## 2. Preprocesamiento
- Se aplica tokenización y limpieza para las columnas que tienen texto libre.
- Se usa stopwords en la tokenización para eliminar palabras sin significado importante.
- Aplicamos lematización para normalizar terminos, usamos SpaCy.

## 3. Entrenamiento
- Aplicamos un TF-IDF básico para mejorar el modelo
- Usamos cosine_similarity3