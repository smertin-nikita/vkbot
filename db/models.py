import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class VkUser(Base):
    __tablename__ = 'vk_user'

    id = sq.Column(sq.Integer, primary_key=True, unique=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, nullable=False, unique=True)
    firstname = sq.Column(sq.VARCHAR(60), nullable=False)
    lastname = sq.Column(sq.VARCHAR(60), nullable=False)
    bdate = sq.Column(sq.DATE, nullable=False)
    sex = sq.Column(sq.BINARY)
    city = sq.Column(sq.Integer, nullable=False)
    search_sex = sq.Column(sq.BINARY, nullable=False)
    age_to = sq.Column(sq.Integer, nullable=False)
    age_from = sq.Column(sq.Integer, nullable=False)


class UserLike(Base):
    __tablename__ = 'user_like'

    id = sq.Column(sq.Integer, primary_key=True, unique=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False, unique=True)
    like_id = sq.Column(sq.Integer, nullable=False)


class UserDislike(Base):
    __tablename__ = 'user_dislike'

    id = sq.Column(sq.Integer, primary_key=True, unique=True, autoincrement=True)
    vk_id = sq.Column(sq.Integer, sq.ForeignKey('vk_user.id', ondelete='CASCADE'), nullable=False, unique=True)
    dislike_id = sq.Column(sq.Integer, nullable=False)

