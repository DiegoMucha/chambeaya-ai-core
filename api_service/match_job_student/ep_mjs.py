from models.KawsAIModel import KawsAIModel
from fastapi import HTTPException, APIRouter, Body
from pydantic import BaseModel
from datetime import date
from preprocessing.preprocesador import Preprocesador
import numpy as np
import pandas as pd

router = APIRouter()
preprocesador = Preprocesador()
model = KawsAIModel()

class Estudiante(BaseModel):
    id: int
    name: str
    email: str
    career: str
    description: str
    weekly_availability: int
    preferred_modality: int
    experience_id: int
    date_of_birth: date
    skills: list[int] = []
    interests: list[int] = []
    embedding: dict = None

class filterMatchService(BaseModel):
    job_offer_id: int
    embedding: dict
    status: str
    stage: int

class MatchJobStudent(BaseModel):
    student_id: int
    job_offer_id: int
    score: float
    match_date: date
    rank: int

@router.post("/match_job_student")
async def match_job_student(estudiante: Estudiante = Body(...), job_offer: filterMatchService = Body(...)):
    #se vectoriza el estudiante y se guarda
    df_estudiante = pd.DataFrame([estudiante.dict()])
    X_estudiante = preprocesador.transform_estudiante(df_estudiante)
    estudiante.embedding = {"vector": X_estudiante[0].toarray().tolist()[0]}

    df_jobs = pd.DataFrame(['puestos_text.csv'.dict()])

    #obtenemos el embedding del job_offer (por ahora no se usa porque estamos usando el csv)
    job_offer_vec = np.array(job_offer.embedding["vector"]).reshape(1, -1)

    #entrenamos el modelo
    model.train(df_jobs)
    
    #hacemos el matcheo
    indexes = model.get_positions(X_estudiante)
    return {
        "student_id": estudiante.id,
        "job_offer_id": job_offer.job_offer_id,
        "match_date": date.today(),
        "rank": 1,
        "indexes": indexes.tolist()
    }