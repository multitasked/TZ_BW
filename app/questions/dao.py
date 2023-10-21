
from app.dao.base import BaseDAO, async_session_maker
from app.questions.models import Questions
from app.questions.schemas import SQuestions

import requests



class QuestionsDAO(BaseDAO):
    model = Questions


    @classmethod
    def get_questions(cls, questions_num: int, questions_received_id: set) -> list[SQuestions]:
        '''Получить уникальные вопросы готовые для записи в БД'''
        # Получить вопросы с сервера
        questions = cls.get_questions_from_server(questions_num) 
        # Удалить не нужную информацию из структуры вопроса
        questions = cls.get_cleared_questions(questions)

        verified_questions = []
        number_of_failed_checks = 0

        for i in range(len(questions)):
            if questions[i]['id'] not in questions_received_id:
                verified_questions.append(questions[i])
                questions_received_id.add(questions[i]['id'])
            else:
                number_of_failed_checks += 1
        else: 
            if number_of_failed_checks > 0:
                new_questions = cls.get_questions(number_of_failed_checks, questions_received_id) # рекурсивный запуск функции
                verified_questions.extend(new_questions)

        return verified_questions


    @classmethod
    def get_questions_from_server(cls, num: int) -> list:
        '''Получить вопросы с сервера'''
        BASE_URL = 'https://jservice.io/api/random'
        response = requests.get(f"{BASE_URL}?count={num}")
        return response.json()


    @classmethod
    def get_cleared_questions(cls, questions: list) -> list[dict]:
        '''Оставить в списке questions только нужные параметры'''
        result = []
        for i in range(len(questions)):
            cleared_question = dict()
            cleared_question['id'] = questions[i]['id']
            cleared_question['answer'] = questions[i]['answer']
            cleared_question['question'] = questions[i]['question']
            cleared_question['airdate'] = questions[i]['airdate']
            result.append(cleared_question)

        return result



    
    @classmethod
    async def get_previous_question(cls) -> str:
        '''Получить один из сохранённых предыдущих вопросов'''
        result = await cls.find_all()
        if result != []:
            return result[-1].question
        return result


    @classmethod
    async def get_questions_received_id(cls) -> set:
        '''Получить id всех сохранённых вопросов'''
        questions_received_id = set()
        result = await cls.find_all()
        for i in result:
            questions_received_id.add(i.server_id)
        return set()
        # запросить все id записанных вопросов


    @classmethod
    async def send_questions_to_database(cls, questions: list) -> None:
        '''Записать полученные вопросы в БД'''
        for i in questions:
            await cls.add(
                server_id=i['id'],
                answer=i['answer'],
                question=i['question'],
                airdate=i['airdate']
                )
        
