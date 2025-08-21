from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from typing import List,Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import session


app=FastAPI()

models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_txt:str
    is_correct:bool

class QuestionBase(BaseModel):
    Question_text:str
    choices:List[ChoiceBase]

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()

db_dependency=Annotated[session,Depends(get_db)]



