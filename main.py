import vk_bot

import os
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

token = os.environ.get("FULL_TOKEN")
group_id = os.environ.get("GROUP_ID")


vk_bot = vk_bot.Bot(token, group_id)
vk_bot.start()