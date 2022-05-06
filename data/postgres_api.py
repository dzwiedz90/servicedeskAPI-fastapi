import sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from .models import User, Case, CaseUpdate
from data.exceptions import UserNotFoundException

global session
global Student


class PostgresAPI:

    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/servicedeskapi', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def session_commit(self):
        self.session.commit()

    def close_session(self):
        self.session.close()

    def session_rollback(self):
        self.session.rollback()

    def check_if_user_exist(self, user_type, user_id):
        does_user_exist = self.session.query(user_type).filter(user_type.id == user_id).first()
        if does_user_exist:
            return does_user_exist
        return False

    # ADMINS
    # def get_admins(self):
    #     return self.session.query(Admin).all()
    #
    # def get_admin(self, admin_id):
    #     result = self.session.query(Admin).filter(Admin.id == admin_id).first()
    #     if result:
    #         return result
    #     else:
    #         raise UserNotFoundException
    #
    # def create_admin(self, username, password, email=None):
    #     try:
    #         admin = Admin(username=username, password=password, email=email)
    #         self.session.add(admin)
    #         self.session_commit()
    #         self.close_session()
    #     except sqlalchemy.exc.IntegrityError:
    #         self.session_rollback()
    #         self.close_session()
    #         raise sqlalchemy.exc.IntegrityError(None, None, None)
    #
    # def update_admin_password(self, admin_id, password):
    #     try:
    #         if self.check_if_user_exist(Admin, admin_id):
    #             # self.session.update(Admin).where(Admin.id == admin_id).values(password=password)
    #             self.session.query(Admin).filter(Admin.id == admin_id).update({Admin.password: password})
    #         else:
    #             raise UserNotFoundException
    #     except UserNotFoundException:
    #         self.session_rollback()
    #         self.close_session()
    #         raise UserNotFoundException
    #
    # def delete_admin(self, admin_id):
    #     admin = self.check_if_user_exist(Admin, admin_id)
    #     try:
    #         if admin:
    #             self.session.delete(admin)
    #             self.session_commit()
    #             self.close_session()
    #         else:
    #             raise UserNotFoundException
    #     except UserNotFoundException:
    #         self.session.rollback()
    #         self.close_session()
    #         raise UserNotFoundException

    # USERS
    def get_users(self):
        return self.session.query(User).filter(User.is_archived == False).all()

    def get_only_users(self):
        return self.session.query(User).filter(User.is_archived == False, User.is_admin == False).all()

    def get_only_admins(self):
        return self.session.query(User).filter(User.is_archived == False, User.is_admin == True).all()

    def get_archived_users(self):
        return self.session.query(User).filter(User.is_archived == True).all()

    def get_user(self, user_id):
        result = self.session.query(User).filter(User.id == user_id, User.is_archived == False).first()
        if result:
            return result
        else:
            raise UserNotFoundException

    def create_user(self, username, password, email=None, is_admin=False):
        try:
            user = User(username=username, password=password, email=email, is_admin=bool(is_admin), is_archived=False)
            self.session.add(user)
            self.session_commit()
            self.close_session()
        except sqlalchemy.exc.IntegrityError as e:
            self.session_rollback()
            self.close_session()
            raise sqlalchemy.exc.IntegrityError(None, None, None)

    def update_user(self, user_id, password, email, is_admin):
        try:
            if self.check_if_user_exist(User, user_id):
                self.session.query(User).filter(User.id == user_id).update(
                    {User.password: password, User.email: email, User.is_admin: is_admin})
                self.session_commit()
                self.close_session()
            else:
                raise UserNotFoundException
        except UserNotFoundException:
            self.session_rollback()
            self.close_session()
            raise UserNotFoundException

    def delete_user(self, user_id):
        try:
            if self.check_if_user_exist(User, user_id):
                self.session.query(User).filter(User.id == user_id).update({User.is_archived: True})
                self.session_commit()
                self.close_session()
            else:
                raise UserNotFoundException
        except UserNotFoundException:
            self.session_rollback()
            self.close_session()
            raise UserNotFoundException

    def restore_user(self, user_id):
        try:
            if self.check_if_user_exist(User, user_id):
                self.session.query(User).filter(User.id == user_id).update({User.is_archived: False})
                self.session_commit()
                self.close_session()
            else:
                raise UserNotFoundException
        except UserNotFoundException:
            self.session_rollback()
            self.close_session()
            raise UserNotFoundException

    # CASES

    def get_cases(self):
        return self.session.query(Case).filter(Case.is_closed == False).all()

    # TODO
    # content = Column(String, nullable=False)
    # date_created = Column(Date, nullable=False)
    # severity = Column(Integer, nullable=False)
    # is_closed = Column(Boolean, nullable=False)
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    def create_case(self, content, severity, user_id):
        case = Case(content=content, date_created=datetime.now(), severity=severity, is_closed=False, user_id=user_id)
        self.session.add(case)
        self.session_commit()
        self.close_session()

    # CASE UPDATES

    def get_case_updates(self, case_id):
        return self.session.query(CaseUpdate).filter(CaseUpdate.case_id == case_id).all()
