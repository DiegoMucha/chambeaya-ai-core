# Todas las librerias que se deben importar
import re
import pandas as pd
import numpy as np
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as spacy_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

# Se crea una clase preprocesador general
class Preprocesador:
    # Primero al crear la clase, vamos a inciar el TF-IDF Vectorizer y el nlp que es el modelo para la lematización
    def __init__(self):
        self.vectorizador = TfidfVectorizer(max_features=500)
        self.nlp = spacy.load("es_core_news_sm")

    # Con esta función recibimos un texto y lo devolvemos ya lematizado sin las stop_words
    def crear_perfil_textual(self, text):
        text = re.sub(r"[^\w\s]", " ", text.lower())
        text = re.sub(r"\s+", " ", text).strip()
        doc = self.nlp(text)
        tokens = []
        for token in doc:
            if token.is_stop or token.is_punct or token.like_num:
                continue
            else:
                tokens.append(token.lemma_)
        return " ".join(tokens) # Se devuelve un string

    # Función para crear el prefil textual de un estudiante (Pesos para cada tipo de carrera)
    def crear_perfil_textual_estudiante(self, estudiante):
        return self.crear_perfil_textual(
            ("carrera: " + str(estudiante['carrera']) + " ") * 1 +
            ("habilidades: " + str(estudiante['habilidades_destacadas']) + " ") * 3 +
            ("intereses: " + str(estudiante['areas_interes']) + " ") * 3 +
            ("descripcion: " + str(estudiante['descripcion_personal']) + " ") * 3 +
            ("experiencia: " + str(estudiante['experiencia_relevante']) + " ") * 5
        )
    
    # Función para crear el prefil textual de un puesto (Pesos para cada tipo de puesto)
    def crear_perfil_textual_puesto(self, puesto):
        return self.crear_perfil_textual(
            ("puesto: " + str(puesto['titulo_puesto']) + " ") * 1 +
            ("descripcion: " + str(puesto['descripcion_puesto']) + " ") * 2 +
            ("area: " + str(puesto['area_del_puesto']) + " ") * 1 +
            ("requisitos: " + str(puesto['requisitos'])) * 5
        )

    # Función para realizar la vectorización TF-IDF de los puestos
    def fit_transform(self, puestos):
        # Hacemos una copia de los dataframes para no modificarlos directamente
        puestos = puestos.copy()

        # Creamos el perfil textual para los puestos
        puestos['perfil_textual'] = puestos.apply(self.crear_perfil_textual_puesto, axis=1)

        # Ahora vectorizamos este perfil textual con TF-IDF
        corpus = puestos['perfil_textual']
        tfidf_puestos = self.vectorizador.fit_transform(corpus)

        # Se retorna la matriz vectorizada de los puestos
        return tfidf_puestos
    
    # Funciń para realizar la vectorización TF-IDF de un estudiante
    def transform_estudiante(self, estudiante):
        estudiante = estudiante.copy()
        text = self.crear_perfil_textual_estudiante(estudiante.iloc[0])
        tfidf_estudiante = self.vectorizador.transform([text])

        return tfidf_estudiante