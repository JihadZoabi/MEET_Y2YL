import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    is_volunteer = Column(Boolean)
    questions = relationship('Question', backref="asker")
    user_answers = relationship('Answer', backref="answerer")

    following = relationship(
        'User', lambda: user_following,
        primaryjoin=lambda: User.user_id == user_following.c.user_id,
        secondaryjoin=lambda: User.user_id == user_following.c.following_id,
        backref='followers'
    )

    def is_authenticated(self) -> bool:
        return True

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return str(self.user_id)


user_following = Table(
    'user_following', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.user_id), primary_key=True),
    Column('following_id', Integer, ForeignKey(User.user_id), primary_key=True)
)


class Question(Base):
    __tablename__ = 'question'
    question_id = Column(String, default=lambda: str(uuid.uuid4().hex)[:10], primary_key=True)
    title = Column(String)
    details = Column(String)
    image_link = Column(String)
    asker_id = Column(Integer, ForeignKey('user.user_id'))
    question_answers = relationship('Answer', backref="parent_quest", cascade="all,delete-orphan")


class Answer(Base):
    __tablename__ = 'answer'
    answer_id = Column(Integer, primary_key=True)
    reply = Column(String)
    answerer_id = Column(Integer, ForeignKey('user.user_id'))
    parent_question = Column(Integer, ForeignKey('question.question_id', ondelete="CASCADE"))
