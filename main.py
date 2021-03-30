import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import vk_bot

import os
from dotenv import load_dotenv

from app.vk_requester import VkRequester
from app.vkinder import VKinder


def get_url_for_token():
    """
    Print url to get user token
    :return:
    """
    print(requests.get(
        url='https://oauth.vk.com/authorize',
        params={
            'client_id': 7697314,
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'scope': ['friends'],
            'response_type': 'token'
        }).url)
    exit(0)


if __name__ == '__main__':
    # get_url_for_token()

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    community_token = os.environ.get("FULL_TOKEN")
    group_id = os.environ.get("GROUP_ID")
    user_token = os.environ.get('USER_TOKEN')
    db_user = os.environ.get('DATABASE_USER')
    db_password = os.environ.get('DATABASE_PASSWORD')
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_name = os.environ.get('DATABASE_NAME')

    bot = vk_bot.VkBot(community_token, group_id)
    requester = VkRequester(token=user_token)

    engine = create_engine(
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    # Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    db_session = session_factory()

    app = VKinder(bot, requester, db_session)
    app.start()




