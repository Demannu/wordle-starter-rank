from db import Base, session
from sqlalchemy import select
from models.common import CommonMixin
from sqlalchemy import Column, String, Float


class Words(CommonMixin, Base):
    __tablename__ = "words"

    word = Column(String(5), unique=True)
    full_correct = Column(Float)
    partial_correct = Column(Float)
    none_correct = Column(Float)

    def check_db(self):
        statement = select(Words).filter_by(word=self.word)
        result = session.execute(statement).first()
        if not result:
            self.add_to_db()

    def add_to_db(self):
        session.add(self)
        session.commit()
