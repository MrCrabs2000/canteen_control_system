from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class (Base):
    __tablename__ = ''

    id = Column(Integer, primary_key=True, nullable=False)
     = relationship('', back_populates='')


class (Base):
    __tablename__ = ''

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

     = relationship('', back_populates='')