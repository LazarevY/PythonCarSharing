from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR


class AutoBrand(BaseModel):
    __tablename__ = 'autos_brands'
    brand_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    brand_name = Column(VARCHAR(20))

    def __repr__(self):
        return f"brand_id - {self.brand_id}, brand_name = {self.brand_name}"
