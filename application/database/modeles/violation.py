from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class Violation(BaseModel):
    __tablename__ = 'violations'
    note_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('rent_contracts.contract_id'))
    violation_id = Column(Integer,  ForeignKey('violation_type.violation_id'))
    note = Column(VARCHAR(400), nullable=True)
    fine = Column(Integer)
