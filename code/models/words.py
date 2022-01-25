from db import Base, session
from wordleStarter import Results
from sqlalchemy import select, desc
from models.common import CommonMixin
from sqlalchemy import Column, String, Float


class Words(CommonMixin, Base):
    __tablename__ = "words"

    word = Column(String(5), unique=True)
    full_correct = Column(Float)
    partial_correct = Column(Float)
    none_correct = Column(Float)
    score = Column(Float)

    @classmethod
    def check_db(cls, word):
        statement = select(cls).filter_by(word=word)
        result = session.execute(statement).first()
        return bool(result)

    def add_to_db(self, result: Results):
        self.full_correct = result.full_correct
        self.partial_correct = result.partial_correct
        self.none_correct = result.none_correct
        self.score = result.score
        session.add(self)
        session.commit()

    def get_from_db(self):
        statement = select(Words).filter_by(word=self.word)
        result = session.execute(statement).first()
        for word in result:
            self.full_correct = word.full_correct
            self.partial_correct = word.partial_correct
            self.none_correct = word.none_correct
            self.score = word.score
        return self

    @classmethod
    def get_highest_scores(cls, metric):
        statement = select(cls).order_by(desc(cls.score)).limit(5)
        result = session.execute(statement)
        return result

    def __str__(self):
        return f"Word: {self.word}"
