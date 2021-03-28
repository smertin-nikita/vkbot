import sqlalchemy as sq

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class VkUserModel(BaseModel):
    __tablename__ = 'vk_user'

    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    firstname = sq.Column(sq.VARCHAR(60), nullable=False)
    lastname = sq.Column(sq.VARCHAR(60), nullable=False)
    bdate = sq.Column(sq.DATE, nullable=False)
    sex = sq.Column(sq.BINARY)
    city = sq.Column(sq.Integer, nullable=False)
    search_sex = sq.Column(sq.BINARY, nullable=False)
    age_to = sq.Column(sq.Integer, nullable=False)
    age_from = sq.Column(sq.Integer, nullable=False)


class UserLikeModel(BaseModel):
    __tablename__ = 'user_like'

    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False, unique=True)
    like_id = sq.Column(sq.Integer, nullable=False)


class UserDislikeModel(BaseModel):
    __tablename__ = 'user_dislike'

    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False, unique=True)
    dislike_id = sq.Column(sq.Integer, nullable=False)

