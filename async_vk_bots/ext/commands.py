from .Context import Context
from .Scenario import Scenario, create_handler


def create_command(commands):
    def command(regexp):
        def decorator(func):
            if regexp not in commands:
                commands[regexp] = list()
            commands[regexp].append(func)
            return func
        return decorator
    return command


def need_ability(abilities_list):
    def decorator(func):
        async def wrapper(msg, data, reply):
            for ability in abilities_list:
                if ability in msg["client_info"] or ability in msg["client_info"]["button_actions"]:
                    return await func(msg, data, reply)
        return wrapper
    return decorator
