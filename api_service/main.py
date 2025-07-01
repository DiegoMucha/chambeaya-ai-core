from fastapi import FastAPI, Body
from api_service.filter_match import filter_job_offer, filter_student
from api_service.match_job_student import match_job_offer, match_student

app = FastAPI()
app.include_router(filter_job_offer.router, prefix="/filter/job_offer")
app.include_router(filter_student.router, prefix="/filter/student")
app.include_router(match_job_offer.router, prefix="/aimodel/job_offer")
app.include_router(match_student.router, prefix="/aimodel/student")

@app.get("/")
async def root():
    return {"message": "API de ChambeaYA"}