from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class StatusOfAuto(BaseModel):
    __tablename__ = 'status_of_auto'
    status_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    status_name = Column(VARCHAR(40))
