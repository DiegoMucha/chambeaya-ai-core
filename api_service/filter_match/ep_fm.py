from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import date
from preprocessing.preprocesador import Preprocesador
from typing import Optional
import pandas as pd

router = APIRouter()
preprocesador = Preprocesador()

class Job_offer(BaseModel):
    id: int
    title: str
    description: str
    required_hours: int
    approximated_salary: int
    duration: int
    start_date: date
    area_id: int
    experience_id: int
    modality: int
    required_skills: list[int] = []
    embedding: Optional[dict] = None

class filterMatchService(BaseModel):
    job_offer_id: int
    embedding: dict
    status: str
    stage: int

@router.post("/preprocess_job_offer", response_model=filterMatchService)
async def preprocess_job_offer(job_offer: Job_offer = Body(...)):
    #vectorizamos el job_offer y se guarda el embedding
    df_puesto = pd.DataFrame([job_offer.dict()])
    X_puesto = preprocesador.fit_transform(df_puesto)

    #lo convertimos a lista para el json
    embedding = X_puesto[0].toarray().tolist()[0]
    return filterMatchService(
        job_offer_id=job_offer.id,
        embedding={"vector": embedding},
        status="filtrado",
        stage=1
    )