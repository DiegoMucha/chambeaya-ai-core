from fastapi import FastAPI, Body
from api_service.filter_match import ep_fm
from api_service.match_job_student import ep_mjs

app = FastAPI()
app.include_router(ep_fm.router, prefix="/filter")
app.include_router(ep_mjs.router, prefix="/aimodel")

@app.get("/")
async def root():
    return {"message": "API de ChambeaYA"}

@app.post("/test_match/")
async def test_match(estudiante: dict = Body(...), job_offer: dict = Body(...)):
    #llama al endpoint de matching
    result = await ep_mjs.match_job_student(estudiante=estudiante, job_offer=job_offer)
    return result