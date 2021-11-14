import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Question, Answer

engine = create_engine('sqlite:///database.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


# user functions:


def get_user_by_name(name):
    user = session.query(User).filter_by(username=name).first()
    return user


def get_user_by_id(user_id):
    user = session.query(User).filter_by(user_id=user_id).first()
    return user


def query_all(db):
    return session.query(db).all()


def add_user(username, psw, vol=False):
    if get_user_by_name(username) is None:
        user = User(username=username,
                    password=psw,
                    is_volunteer=vol)
        session.add(user)
        try:
            session.commit()
        except:
            session.rollback()
            raise
        return
    return False


def delete_user(username):
    get_user_by_name(username).delete()
    try:
        session.commit()
    except:
        session.rollback()
        raise


# question database

def get_question(question_id):
    question = session.query(Question).filter_by(question_id=question_id).first()
    return question


def delete_question(question_id):
    if get_question(question_id) is None:
        return False
    session.delete(get_question(question_id))
    try:
        session.commit()
    except:
        session.rollback()
        raise


def add_question(title, details, user, link=None):
    new_question = Question(title=title,
                            details=details,
                            image_link=link,
                            asker=user)
    session.add(new_question)
    try:
        session.commit()
    except:
        session.rollback()
        raise


# answer function


def get_answer(question, user):
    answers = user.user_answers
    for ans in answers:
        if ans.parent_question == question:
            return ans
    return False


def add_answer(reply, user, question):
    new_answer = Answer(reply=reply, answerer=user, parent_quest=question)
    session.add(new_answer)
    try:
        session.commit()
    except:
        session.rollback()
        raise
