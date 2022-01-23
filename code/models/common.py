from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer


class CommonMixin(object):

    id = Column(Integer, primary_key=True)
