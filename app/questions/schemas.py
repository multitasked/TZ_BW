from pydantic import BaseModel


class SQuestions(BaseModel):
    id: int
    server_id: int
    answer: str
    question: str
    airdate: str

