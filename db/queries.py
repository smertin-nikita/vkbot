from db.models import VkUser, UserLike, UserDislike
"""
Module : queries to db
"""


def get_vk_user(session, vk_id: int):
    """
    Return instance of VkUser if exist else return None
    :param session: db session
    :param vk_id: id of vk user
    :return: VkUser
    """
    vk_user = session.query(VkUser).where(VkUser.vk_id == vk_id).one_or_none()
    return vk_user


def add_user_like(session, vk_id, like_id):
    """
    Adds like
    :param session:
    :param vk_id: Who likes
    :param like_id: Who is being liked
    :return:
    """
    session.add(UserLike(vk_id=vk_id, like_id=like_id))
    session.commit()


def add_user_dislike(session, vk_id, dislike_id):
    """
    Adds dislike
    :param session:
    :param vk_id: Who likes
    :param dislike_id: Who is being disliked
    :return:
    """
    session.add(UserDislike(vk_id=vk_id, dislike_id=dislike_id))
    session.commit()


def add_vk_user(session, user: VkUser):
    """
    Adds vk user
    :param session:
    :param user: instance of vk user
    :return:
    """
    session.add(user)
    session.commit()


def update_search_age(session, vk_id: int, age_from: int, age_to: int):
    """
    Updates searching age
    :param session:
    :param vk_id: id of vk user
    :param age_from: searching age from
    :param age_to: searching age to
    :return:
    """
    session.query(VkUser).where(VkUser.vk_id == vk_id).update({
        'age_from': age_from,
        'age_to': age_to
    })


def update_search_sex(session, vk_id: int, search_sex: bool):
    """
    Updates searching sex
    :param session:
    :param vk_id: id of vk user
    :param search_sex: searching sex
    :return:
    """
    session.query(VkUser).where(VkUser.vk_id == vk_id).update({
        'search_sex': search_sex
    })
