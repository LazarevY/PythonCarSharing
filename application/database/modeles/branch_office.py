from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP


class BranchOffice(BaseModel):
    __tablename__ = 'branch_offices'
    office_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    office_name = Column(VARCHAR(20))
    office_address = Column(VARCHAR(200))
