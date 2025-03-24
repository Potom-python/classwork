import datetime

import sqlalchemy
from sqlalchemy import orm, ForeignKey

from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin



class Jobs(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, ForeignKey('users.id'), nullable=False)
    job = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    user = orm.relationship('User')
