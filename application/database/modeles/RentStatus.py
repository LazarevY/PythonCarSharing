from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, VARCHAR

from application.database.modeles.base import BaseModel


class RentStatus(BaseModel):
    __tablename__ = 'rent_statuses'
    status_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    status_name = Column(VARCHAR(20))