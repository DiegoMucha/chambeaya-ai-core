from fastapi import FastAPI
from api_service.match_job_student import ep_mjs

app = FastAPI()
app.include_router(ep_mjs.router, prefix="/aimodel")

@app.get("/")
async def root():
    return {"message": "API de ChambeaYA"}