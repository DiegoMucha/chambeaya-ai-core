from models.KawsAIModel import KawsAIModel
from fastapi import HTTPException, APIRouter
from api_service.filter_match.ep_fm import filterMatchService
from pydantic import BaseModel
from datetime import date

router = APIRouter()
model = KawsAIModel()

#funcion de ejecucion del modelo tomando en cuenta los datos filtrados
def execution(match: filterMatchService):
    return model.get_positions(match)

class MatchJobStudent(BaseModel):
    filter_match_service: filterMatchService
    score: int
    match_date: date

@router.post("/match_job_student")
async def match_job_student(match: MatchJobStudent):
    execution = model.get_positions(match)
    if not execution:
        raise HTTPException(status_code=404, detail="No hay match disponible para este estudiante")
    return {
        "execution": execution
    }