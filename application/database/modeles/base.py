import datetime

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def __repr__(self):
        return "<{0.__class__.__name__}>".format(self)
