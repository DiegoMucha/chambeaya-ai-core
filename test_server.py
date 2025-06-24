from fastapi import FastAPI
from api_service.match_job_student.ep_mjs import model
from api_service.filter_match.ep_fm import Estudiante
from pydantic import BaseModel
import pandas as pd
from preprocessing.preprocesador import Preprocesador

app = FastAPI()
preprocesador = Preprocesador()

# Datos de prueba (estudiante único)
estudiante_prueba = Estudiante(
    career="Ciencias de la Computación",
    habilidades_destacadas="Python, C++, JavaScript, React",
    areas_interes="Desarrollo de Software, Desarrollo Backend",
    description="Apasionado por la tecnología y crear soluciones innovadoras.",
    experience_id="Desarrollador de software con 3 años de experiencia en Python y JavaScript.",
    preferred_modality=1,
    weekly_availability=20
)

@app.get("/")
def root():
    return {"message": "Servidor de prueba para IA (sin backend)"}

@app.get("/test_match/")
def test_match():
    df_puestos = pd.read_csv("datasets/puestos_test.csv")
    df_estudiante = pd.DataFrame([estudiante_prueba.dict()])
    if 'preferred_modality' in df_estudiante.columns:
        df_estudiante = df_estudiante.rename(columns={'preferred_modality': 'modalidad_de_trabajo'})
    if 'preferred_modality' in df_puestos.columns:
        df_puestos = df_puestos.rename(columns={'preferred_modality': 'modalidad_de_trabajo'})
    if 'weekly_availability' in df_estudiante.columns:
        df_estudiante = df_estudiante.rename(columns={'weekly_availability': 'horas_semanales'})
    if 'weekly_availability' in df_puestos.columns:
        df_puestos = df_puestos.rename(columns={'weekly_availability': 'horas_semanales'})
    X_puestos = preprocesador.fit_transform(df_puestos)
    X_estudiante = preprocesador.transform_estudiante(df_estudiante)
    n_ofertas = len(df_puestos)
    n_neighbors = min(3, n_ofertas)
    model.knn = model.knn.__class__(n_neighbors=n_neighbors, metric='cosine')
    model.train(X_puestos)
    indexes = model.get_positions(X_estudiante)
    return {
        "indexes": indexes.tolist(),
        "puestos_ids": df_puestos.iloc[indexes.tolist()].to_dict(orient="records")
    }