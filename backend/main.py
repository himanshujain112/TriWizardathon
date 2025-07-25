from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.exam_paper import router as exam_paper_router
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

app.include_router(auth_router)
app.include_router(exam_paper_router)