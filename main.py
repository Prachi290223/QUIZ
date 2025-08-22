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

    class Config():
        orm_mode=True

class QuestionBase(BaseModel):
    question_text:str
    choices:List[ChoiceBase]

    class Config():
        orm_mode=True

def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()

db_dependency=Annotated[session,Depends(get_db)]

@app.get("/questions/{question_id}")
async def read_question(question_id,db:db_dependency):
    result=db.query(models.Questions).filter(models.Questions.id==question_id).first()
    if not result:
        raise HTTPException(status_code=404,detail="No such question")
    return result


@app.post('/questions')
async def create_qestions(question:QuestionBase,db:db_dependency):
    db_questions=models.Questions(question_text=question.question_text)
    db.add(db_questions)
    db.commit()
    db.refresh(db_questions)
    for choice in question.choices:
        db_choice=models.Choices(choice_text=choice.choice_txt,is_correct=choice.is_correct)
        db.add(db_choice)
    db.commit()

@app.put('/questions/{question_id}')
async def update_question(question_id,db:db_dependency,request:QuestionBase):
    db_questions=db.query(models.Questions).filter(models.Questions.id==question_id)
    if not db_questions.first():
        raise HTTPException(status_code=404,detail="No such question")
    db_questions.update({"question_text":request.question_text})
    db.commit()
    return "updated"

@app.delete('/question/{question_id}')
async def destroy_question(question_id,db:db_dependency):
    db.query(models.Questions).filter(models.Questions.id==question_id).delete(synchronize_session=False)
    db.commit()
    return 'deleted'

@app.get('/questions')
async def all_questions(db:db_dependency):
    result=db.query(models.Questions).order_by(models.Questions.id).all() 
    return result






@app.get("/choices/{question_id}")
async def read_choices(question_id,db:db_dependency):
    result=db.query(models.Choices).filter(models.Choices.id==question_id).all()
    if not result:
        raise HTTPException(status_code=404,detail="No such choices for the question")
    return result
