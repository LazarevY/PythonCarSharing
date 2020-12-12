from sqlalchemy import Column, Integer, ForeignKey

from application.database.modeles.base import *


class AutoTrack(BaseModel):
    __tablename__ = 'auto_track'
    track_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('rent_contracts.contract_id'))
    state_id = Column(Integer, ForeignKey('status_of_auto.status_id'))
    duration = Column(Integer, nullable=False)
