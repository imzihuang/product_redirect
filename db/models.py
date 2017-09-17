#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Table, MetaData

from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from base import get_engine

BaseModel = declarative_base()
DynamicDModel = declarative_base()

class Redirect(BaseModel):
    __tablename__ = 'redirect'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(12), nullable=False)
    url = Column(VARCHAR(100), nullable=False)
    parameter = Column(VARCHAR(100))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
       return {c.name: getattr(self, c.name, None).strftime('%Y-%m-%d %H:%M:%S') if isinstance(getattr(self, c.name, None), datetime) else getattr(self, c.name, None) for c in self.__table__.columns}



def register_db():
    engine = get_engine()
    BaseModel.metadata.create_all(engine)


def unregister_db():
    engine = get_engine()
    BaseModel.metadata.drop_all(engine)


