import os


def startapp(app_name):
    os.mkdir(app_name)
    with open(os.path.join(app_name, "config.py"), "w") as f:
        f.write("token = \"\"\ngroup_id = 0")
    with open(os.path.join(app_name, "bot.py"), "w") as f:
        f.write(
            "from async_vk_bot import Bot\nfrom .config import group_id, token\n\nbot = Bot(group_id)\n\nbot.run(token)"
        )
    with open(os.path.join(app_name, "controllers.py"), "w") as f:
        f.write("from async_vk_bot.ext import Controller\nfrom .views import *")
    with open(os.path.join(app_name, "views.py"), "w") as f:
        f.write("from async_vk_bot.ext import View, PMView, ChatView")
    # TODO: Scenarios and Models
