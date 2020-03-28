from Bot import Bot
from .Scenario import Scenario
from .Context import Context


def command(regexp):
    def decorator(func):
        if Bot.bot:
            Bot.bot.add_command(regexp, func)
    return decorator
