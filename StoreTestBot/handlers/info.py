from config import bot, dp
from aiogram import types, Dispatcher


async def info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f"TestHomeworkStore: Особый онлайн бот магазин,\n"
                                f"способный хранить и продовать абсолютно любую вещ, если оно в ассортименте\n"
                                f"Надеюсь вы найдете что нибудь для себя!")



def register_info(dp: Dispatcher):
    dp.register_message_handler(info, commands=["info"])