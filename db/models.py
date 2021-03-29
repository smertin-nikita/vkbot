import sqlalchemy as sq

from sqlalchemy import Column, Integer, TIMESTAMP, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# todo Можно ли наполнять модели дополнительнымы функционалом? Вроде как нет
class VkUser(Base):
    __tablename__ = 'vk_user'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    firstname = sq.Column(sq.VARCHAR(60), nullable=False)
    lastname = sq.Column(sq.VARCHAR(60), nullable=False)
    sex = sq.Column(sq.BOOLEAN)
    city_id = sq.Column(sq.Integer, nullable=False)
    city_title = sq.Column(sq.VARCHAR(60), nullable=False)
    search_sex = sq.Column(sq.BOOLEAN, nullable=False)
    age_to = sq.Column(sq.Integer, nullable=False)
    age_from = sq.Column(sq.Integer, nullable=False)


class UserLike(Base):
    __tablename__ = 'user_like'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.vk_id', ondelete='CASCADE'), nullable=False, unique=True)
    like_id = sq.Column(sq.Integer, nullable=False)


class UserDislike(Base):
    __tablename__ = 'user_dislike'

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.vk_id', ondelete='CASCADE'), nullable=False, unique=True)
    dislike_id = sq.Column(sq.Integer, nullable=False)
