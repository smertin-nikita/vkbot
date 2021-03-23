import vk_bot

import os
from dotenv import load_dotenv

from vk_user import VkRequester

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

community_token = os.environ.get("FULL_TOKEN")
group_id = os.environ.get("GROUP_ID")
user_token = os.environ.get('USER_TOKEN')

vk_requester = VkRequester(user_token)

vk_bot = vk_bot.Bot(community_token, group_id)
vk_bot.start()