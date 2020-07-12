# Bot
Основной класс для создания чат-бота

## Методы
###Bot(group_id, version="5.120", loop=None)
Инициализация бота, если loop равен None, то значение loop берётся как `asyncio.get_event_loop()`
```python
from async_vk_bots import Bot
bot = Bot(123456789)
```

###on_ready(func)
Декоратор для передачи колбэка, который будет вызвана после запуска бота.
```python
@bot.on_ready
async def ready():
    pass
```

###command(regexp_or_func)(func)
Декоратор для передачи колбэка, вызваного при получении сообщения от пользователя,
соответствующему регулярном выражению или при возврате True
от переданной в regexp_or_func функции.

Колбэк принимает аргументы: msg, data, reply
msg - объект сообщения(ext.DataModels.Message.Message)
data - результат re.fullmatch(<regexp_or_func>) или результат выполнения regexp_or_func
reply - функция messages.send из API с уже переданным peer_id пользователя
```python
@bot.command(r"Hi")
async def hi(msg, data, reply):
    await reply(f"Hi, user with id {msg.from_id}")
```

###event(regexp_or_func)(func)
Декоратор для передачи колбэка, вызваного при получении payload
от callback кнопки, соответствующему регулярному выражению regexp_or_func,
или возврате True от вызова функции regexp_or_func().

Колбэк принимает аргументы: event
event - объект события (ext.DataModels.Message.MessageEvent)
```python
@bot.event(r"{\"action\": \"hi\"}")
async def event_hi(event):
    await bot.api.send(event.user_id, f"Hello user {event.user_id}")
```
