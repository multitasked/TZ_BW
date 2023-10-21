from fastapi import APIRouter
from app.questions.dao import QuestionsDAO
from app.questions.schemas import SQuestions


router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)



@router.post("/")
async def add_questions_num(questions_num: int):
    # получение ранее сохранённого вопроса
    previous_question = await QuestionsDAO.get_previous_question()
    
    # получение новых уникальных вопросов и сохранение их в БД
    questions_received_id = await QuestionsDAO.get_questions_received_id()
    questions = QuestionsDAO.get_questions(questions_num, questions_received_id)
    await QuestionsDAO.send_questions_to_database(questions)

    return previous_question







