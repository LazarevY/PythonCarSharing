from sqlalchemy import Column, Integer, ForeignKey, VARCHAR

from application.database.modeles.base import *


class ClientLogin(BaseModel):
    __tablename__ = 'client_login'
    client_id = Column(Integer,
                       ForeignKey('clients.client_id'),
                       nullable=False,
                       unique=True,
                       primary_key=True,
                       autoincrement=True)
    password_hash = Column(VARCHAR(500))

