from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class AutoModel(BaseModel):
    __tablename__ = 'autos_models'
    model_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    model_name = Column(VARCHAR(60))
    brand_id = Column(Integer, ForeignKey('autos_brands.brand_id'))
    category_id = Column(Integer, ForeignKey('drive_categories.category_id'))

