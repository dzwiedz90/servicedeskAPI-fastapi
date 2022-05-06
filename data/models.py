from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.types import Boolean, Date

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/servicedeskapi', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    is_archived = Column(Boolean, nullable=False)
    is_admin = Column(Boolean, nullable=False)
    case_user_created = relationship('Case', back_populates='user_created', cascade='all, delete, delete-orphan')
    case_admin_assigned = relationship('Case', back_populates='admin_assigned', cascade='all, delete, delete-orphan')
    update_creator = relationship('CaseUpdate', back_populates='update_user_creator',
                                  cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'


# class Admin(Base):
#     __tablename__ = 'admins'
#     id = Column(Integer, primary_key=True)
#     username = Column(String, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     email = Column(String, unique=True)
#     is_archived = Column(Boolean, nullable=False)
#     case_admin_assigned = relationship('Case', back_populates='admin_assigned', cascade='all, delete, delete-orphan')
#
#     def __repr__(self):
#         return f'Admin(id={self.id}, username={self.username}, email={self.email})'


class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    date_created = Column(Date, nullable=False)
    severity = Column(Integer, nullable=False)
    is_closed = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_created = relationship('User', back_populates='case_user_created')
    admin_assigned = relationship('User', back_populates='case_admin_assigned')
    case_update = relationship('CaseUpdate', back_populates='case')

    def __repr__(self):
        return f'Case(id={self.id}, content={self.content}, date_created={self.date_created}, severity={self.severity}, is_closed={self.is_closed})'


class CaseUpdate(Base):
    __tablename__ = 'case_updates'
    id = Column(Integer, primary_key=True)
    comment = Column(String, nullable=False)
    date_created = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    case_id = Column(Integer, ForeignKey('cases.id'), nullable=False)
    update_user_creator = relationship('User', back_populates='update_creator')
    case = relationship('Case', back_populates='case_update')

    def __repr__(self):
        return f'CaseUpdate(id={self.id}, comment={self.comment}, date_created={self.date_created}, user_id={self.user_id}'


Base.metadata.create_all(engine)
