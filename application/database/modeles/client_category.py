from sqlalchemy import Column, Integer, ForeignKey, VARCHAR

from application.database.modeles.base import *


class ClientCategory(BaseModel):
    __tablename__ = 'clients_categories'
    note_id = Column(Integer,
                     ForeignKey('clients.client_id'),
                     nullable=False,
                     unique=True,
                     primary_key=True,
                     autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    category_id = Column(Integer, ForeignKey('drive_categories.category_id'))
