from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR

from application.database.modeles.base import BaseModel


class RentHistory(BaseModel):
    __tablename__ = 'rents_history'
    note_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('rent_contracts.contract_id'))
    status_id = Column(Integer, ForeignKey('rent_statuses.status_id'))
    note = Column(VARCHAR(200))
    note_date = Column(TIMESTAMP(timezone=False))
