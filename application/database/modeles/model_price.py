from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class ModelPrice(BaseModel):
    __tablename__ = 'model_price'
    model_id = Column(Integer,
                      ForeignKey('autos_models.model_id'),
                      nullable=False,
                      unique=True,
                      primary_key=True,
                      autoincrement=True)
    price = Column(Integer)
