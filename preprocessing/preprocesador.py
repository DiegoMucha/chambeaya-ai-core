# Todas las librerias que se deben importar
import re
import pandas as pd
import numpy as np
import spacy
from spacy.lang.es.stop_words import STOP_WORDS as spacy_stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from sentence_transformers import SentenceTransformer

class Preprocesador:
    def __init__(self):
        self.modelo_embedding = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
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
            ("descripcion: " + str(puesto['descripcion_puesto']) + " ") * 3 +
            ("area: " + str(puesto['area_del_puesto']) + " ") * 8 +
            ("requisitos: " + str(puesto['requisitos'])) * 10
        )

    # Embeddings para todos los puestos
    def get_embeddings_alloffers(self, puestos):
        puestos = puestos.copy()
        puestos['perfil_textual'] = puestos.apply(self.crear_perfil_textual_puesto, axis=1)
        corpus = puestos['perfil_textual'].tolist()
        embeddings = self.modelo_embedding.encode(corpus, convert_to_numpy=True, show_progress_bar=True)
        return embeddings

    # Embeddings para todos los estudiantes
    def get_embeddings_allstudents(self, estudiantes):
        estudiantes = estudiantes.copy()
        estudiantes['perfil_textual'] = estudiantes.apply(self.crear_perfil_textual_estudiante, axis=1)
        corpus = estudiantes['perfil_textual'].tolist()
        embeddings = self.modelo_embedding.encode(corpus, convert_to_numpy=True, show_progress_bar=True)
        return embeddings
    
    # Embedding para un estudiante
    def get_embedding_student(self, estudiante):
        estudiante = estudiante.copy()
        text = self.crear_perfil_textual_estudiante(estudiante.iloc[0])
        embedding = self.modelo_embedding.encode([text], convert_to_numpy=True)
        return embedding
    
    # Embedding para un puesto
    def get_embedding_offer(self, offer):
        offer = offer.copy()
        text = self.crear_perfil_textual_puesto(offer.iloc[0])
        embedding = self.modelo_embedding.encode([text], convert_to_numpy=True)
        return embedding