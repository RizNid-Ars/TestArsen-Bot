from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

from aiogram.types import ReplyKeyboardRemove
from db import db_main


class FSM_Orders(StatesGroup):
    product_id = State()
    size = State()
    count = State()
    phone_number = State()
    submit_orders = State()


async def start_fsm_order(message: types.Message):
    await message.answer('Введите нужный вам артикул: ', reply_markup=buttons.cancel_button)
    await FSM_Orders.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Укажите нужный вам размер: ', reply_markup=buttons.cancel_button)
    await FSM_Orders.size.set()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Укажите количество нужного вам товара: ', reply_markup=buttons.cancel_button)
    await FSM_Orders.count.set()


async def load_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count'] = message.text

    await message.answer('Укажите ваш номер телефона для обратной связи: ', reply_markup=buttons.cancel_button)
    await FSM_Orders.phone_number.set()


async def load_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text

    await message.answer(
        f'Верные ли данные ?\n'
                f"Артикул товара: {data['product_id']}\n"
                f"Размер товара: {data['size']}\n"
                f"Количество товара: {data['count']}\n"
                f"Ваш номер телефона: {data['phone_number']}\n",
        reply_markup=buttons.cancel_button
    )
    await FSM_Orders.next()


async def submit_orders(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:

            await db_main.sql_insert_orders(
                product_id=data['product_id'],
                size=data['size'],
                count=data['count'],
                phone_number=data['phone_number']
            )
            await message.answer('Отлично, Заказ сделан!',
                                 reply_markup=kb)
            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, заказ товаров отменен!',
                             reply_markup=kb)
        await state.finish()
    else:
        await message.answer('Выберите "Да" или "Нет"')


async def cancel_fsm(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is not None:
            await state.finish()
            await message.answer('Отменено!')


def register_order(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(
        equals='Отмена',
        ignore_case=True),
                                state="*")
    dp.register_message_handler(start_fsm_order, commands=['order'])
    dp.register_message_handler(load_product_id, state=FSM_Orders.product_id)
    dp.register_message_handler(load_size, state=FSM_Orders.size)
    dp.register_message_handler(load_count, state=FSM_Orders.count)
    dp.register_message_handler(load_phone_number, state=FSM_Orders.phone_number)
    dp.register_message_handler(submit_orders, state=FSM_Orders.submit_orders)