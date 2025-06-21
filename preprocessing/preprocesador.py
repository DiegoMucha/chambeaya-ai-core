# Todas las librerias que se deben importar
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd
import numpy as np
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as spacy_stopwords
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from scipy.sparse import hstack

# Se crea una clase preprocesador general
class Preprocesador:
    def __init__(self):
        self.vectorizador = TfidfVectorizer(max_features=500)
        self.scaler= StandardScaler()
        self.columnas_numericas = ['horas_semanales']
        self.columnas_modalidad = []
        self.nlp = spacy.load("es_core_news_sm")

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
        return " ".join(tokens)

    def crear_perfil_textual_estudiante(self, estudiante):
        return self.crear_perfil_textual(
            ("carrera: " + str(estudiante['carrera']) + " ") * 1 +
            ("habilidades: " + str(estudiante['habilidades_destacadas']) + " ") * 3 +
            ("intereses: " + str(estudiante['areas_interes']) + " ") * 3 +
            ("descripcion: " + str(estudiante['descripcion_personal']) + " ") * 3 +
            ("experiencia: " + str(estudiante['experiencia_relevante']) + " ") * 5
        )

    def crear_perfil_textual_puesto(self, puesto):
        return self.crear_perfil_textual(
            ("puesto: " + str(puesto['titulo_puesto']) + " ") * 1 +
            ("descripcion: " + str(puesto['descripcion_puesto']) + " ") * 5 +
            ("area: " + str(puesto['area_del_puesto']) + " ") * 3
        )

    def fit_transform(self, estudiantes, puestos):
        # Hacemos una copia de los dataframes para no modificarlos directamente
        estudiantes = estudiantes.copy()
        puestos = puestos.copy()

        # Creamos el perfil textual para estudiantes y puestos
        estudiantes['perfil_textual'] = estudiantes.apply(self.crear_perfil_textual_estudiante, axis=1)
        puestos['perfil_textual'] = puestos.apply(self.crear_perfil_textual_puesto, axis=1)

        # Ahora vectorizamos este perfil textual con TF-IDF
        corpus = pd.concat([estudiantes['perfil_textual'], puestos['perfil_textual']], axis=0)
        X_text = self.vectorizador.fit_transform(corpus)

        # Ahora usamos one-hot-encoding para la columna de modalidad
        df_modalidad = pd.concat([estudiantes[['modalidad_de_trabajo']], puestos[['modalidad_de_trabajo']]])
        df_modalidad_encoded = pd.get_dummies(df_modalidad, prefix='modalidad_de_trabajo')
        self.columnas_modalidad = df_modalidad_encoded.columns.tolist()

        # Usamos standard scaler para normalizar las columnas numericas
        columnas_numericas_combinadas = pd.concat([
            estudiantes[self.columnas_numericas],
            puestos[self.columnas_numericas]
        ], axis=0)

        self.scaler.fit(columnas_numericas_combinadas)

        n_estudiantes = len(estudiantes)
        X_puestos = hstack([
            X_text[n_estudiantes:],
            df_modalidad_encoded.iloc[n_estudiantes:].values.astype(np.float32),
            self.scaler.transform(puestos[self.columnas_numericas]).astype(np.float32)
        ])
        X_estudiantes = hstack([
            X_text[:n_estudiantes],
            df_modalidad_encoded.iloc[:n_estudiantes].values.astype(np.float32),
            self.scaler.transform(estudiantes[self.columnas_numericas]).astype(np.float32)
        ])
        return X_estudiantes, X_puestos

    def transform_estudiante(self, estudiante):
        estudiante = estudiante.copy()

        text = self.crear_perfil_textual_estudiante(estudiante.iloc[0])
        X_text = self.vectorizador.transform([text])

        modalidad = pd.get_dummies(pd.DataFrame([estudiante.iloc[0]['modalidad_de_trabajo']], columns=['modalidad_de_trabajo']))
        modalidad = modalidad.reindex(columns=self.columnas_modalidad, fill_value=0)

        num_scaled = self.scaler.transform([estudiante[self.columnas_numericas].iloc[0]])

        return hstack([X_text, modalidad.values.astype(np.float32), num_scaled.astype(np.float32)])