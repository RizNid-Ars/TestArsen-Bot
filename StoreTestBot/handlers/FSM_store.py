from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import buttons

from aiogram.types import ReplyKeyboardRemove
from db import db_main
from decouple import config

class FSM_Store(StatesGroup):
    name_products = State()
    size = State()
    category = State()
    price = State()
    product_id = State()
    info_product = State()
    photo_products = State()
    submit = State()


async def start_fsm(message: types.Message):
    await message.answer('Укажите название или бренд товара: ', reply_markup=buttons.cancel_button)
    await FSM_Store.name_products.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_products'] = message.text

    await message.answer('Укажите категорию товара: ', reply_markup=buttons.cancel_button)
    await FSM_Store.category.set()


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['cotegory_products'] = message.text

    await message.answer('Укажите размер товара: ', reply_markup=buttons.cancel_button)
    await FSM_Store.size.set()


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await message.answer('Введите цену товара: ', reply_markup=buttons.cancel_button)
    await FSM_Store.price.set()


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await message.answer('Введите артикул (он должен быть уникальным): ', reply_markup=buttons.cancel_button)
    await FSM_Store.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await message.answer('Отправьте фото: ', reply_markup=buttons.cancel_button)
    await FSM_Store.photo_products.set()


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await message.answer('Верные ли данные ?')
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Название товара: {data["name_products"]}\n'
                f'Категория товара: {data["cotegory_products"]}\n'
                f'Размер товара: {data["size"]}\n'
                f'Цена товара: {data["price"]}\n'
                f'Артикул: {data["product_id"]}\n',
        reply_markup=buttons.cancel_button)

    await FSM_Store.next()

async def submit(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardRemove()

    if message.text == 'Да':
        async with state.proxy() as data:

            await db_main.sql_insert_products(
                name_products=data['name_products'],
                cotegory_products=data['cotegory_products'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )
            await message.answer('Отлично, Данные в базе!',
                                 reply_markup=kb)
            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, заполенние товаров отменена!',
                             reply_markup=kb)
        await state.finish()
    else:
        await message.answer('Выберите "Да" или "Нет"')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!')


def register_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(
        equals='Отмена',
        ignore_case=True),
                                state="*")

    dp.register_message_handler(start_fsm, commands=['store'])
    async def checker(message: types.Message):
        if message.from_user.id == config('staff'):
            pass
        else:
            await message.answer('Вы не являетесь сотрудником')

    dp.register_message_handler(load_name, state=FSM_Store.name_products)
    dp.register_message_handler(load_category, state=FSM_Store.category)
    dp.register_message_handler(load_size, state=FSM_Store.size)
    dp.register_message_handler(load_price, state=FSM_Store.price)
    dp.register_message_handler(load_product_id, state=FSM_Store.product_id)
    dp.register_message_handler(load_photo, state=FSM_Store.photo_products, content_types=['photo'])
    dp.register_message_handler(submit, state=FSM_Store.submit)