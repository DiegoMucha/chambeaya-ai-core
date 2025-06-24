from fastapi import APIRouter
from pydantic import BaseModel, EmailStr
from datetime import date

router = APIRouter()

#inicializacion de clases como estudiante y job_offer para que se usen en el backend
class Estudiante(BaseModel):
    career: str
    habilidades_destacadas: str
    areas_interes: str
    description: str
    experience_id: str
    preferred_modality: int
    weekly_availability: int

class Job_offer(BaseModel):
    title: str
    description: str
    required_hours: int
    approximated_salary: int
    duration: int
    start_date: date
    modality: int

class filterMatchService(BaseModel):
    student_id: Estudiante
    job_offer_id: Job_offer
    model_score: float
    status: str
    stage: int

def filter():
    classFilter = filterMatchService


@router.post("/filter_match")
async def filter_match(filter_input: filterMatchService):
    #se retorna la lista de datos filtrados para que lo use el match, y tambien
    #para que se mande al backend y este lo guarde en la base de datos
    return {
        "student_id": filter_input.student_id,
        "job_offer_id": filter_input.job_offer_id,
        "model_score": filter_input.model_score,
        "status": filter_input.status,
        "stage": filter_input.stage
    }