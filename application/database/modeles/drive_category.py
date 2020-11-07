from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class DriveCategory(BaseModel):
    __tablename__ = 'drive_categories'
    category_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    category_name = Column(VARCHAR(60))
