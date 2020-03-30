from async_vk_bots.Bot import Bot
from .Context import Context
from .Scenario import Scenario


def command(regexp):
    def decorator(func):
        if Bot.bot:
            Bot.bot.add_command(regexp, func)
        return func
    return decorator


def need_ability(abilities_list):
    def decorator(func):
        async def wrapper(msg, data, reply):
            for ability in abilities_list:
                if ability in msg["client_info"] or ability in msg["client_info"]["button_actions"]:
                    return await func(msg, data, reply)
        return wrapper
    return decorator
