from fastapi import APIRouter, Body
from pydantic import BaseModel
from datetime import date
from preprocessing.preprocesador import Preprocesador
from typing import List
import pandas as pd

router = APIRouter()
preprocesador = Preprocesador()

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

@router.post("/preprocess_student")
async def preprocess_student(student: Estudiante = Body(...)):
    df = pd.DataFrame([student.dict()])
    embedding = preprocesador.get_embedding_student(df)
    return {
        "student_id": student.id,
        "embedding": {"vector": embedding[0].tolist()},
        "status": "processed",
        "stage": 1
    }

@router.post("/preprocess_all_student")
async def preprocess_all_student(students: List[Estudiante] = Body(...)):
    df = pd.DataFrame([s.dict() for s in students])
    embeddings = preprocesador.get_embeddings_allstudents(df)
    results = []
    for i, student in enumerate(students):
        results.append({
            "student_id": student.id,
            "embedding": {"vector": embeddings[i].tolist()},
            "status": "processed",
            "stage": 1
        })
    return results