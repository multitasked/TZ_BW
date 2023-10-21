from fastapi import FastAPI
from app.questions.router import router as router_questions


app = FastAPI()
app.include_router(router_questions)


