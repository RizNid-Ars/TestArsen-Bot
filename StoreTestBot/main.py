from aiogram.utils import executor
from config import bot, dp, staff
from handlers import (start, info, FSM_store, FSM_order, send_products)

start.register_start(dp=dp)
info.register_info(dp=dp)
FSM_store.register_store(dp=dp)
FSM_order.register_order(dp=dp)
send_products.register_send_products_handler(dp=dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)