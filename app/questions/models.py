from sqlalchemy import Column, Integer, String
from app.database import Base


class Questions(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, nullable=False)
    answer = Column(String, nullable=False)
    question = Column(String, nullable=False)
    airdate = Column(String, nullable=False)

