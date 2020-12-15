from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class ViolationType(BaseModel):
    __tablename__ = 'violation_type'
    violation_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    violation_type = Column(VARCHAR(100))
    desc = Column(VARCHAR(100))
