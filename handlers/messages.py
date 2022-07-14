import dispatcher
from dispatcher import dp, bot
from bot import db
from aiogram.types import Message, ReplyKeyboardRemove
from states import States
from markups import reply_keyboards, inline_keyboards
from aiogram.dispatcher import FSMContext
import config
from aiogram.utils.exceptions import MessageToDeleteNotFound


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: Message):
    if db.check_user_exists(msg.from_user.id):
        await msg.answer("С возвращением! Для нового заказа\n/new_order", reply_markup=ReplyKeyboardRemove())
        await States.first()
    else:
        await msg.answer(
            "Для начала работы нужно поделиться своим номером телефона. Это нужно для связи водителя с вами",
            reply_markup=reply_keyboards.contact
        )
        await States.last()


@dp.message_handler(commands=['cancel'], state=States.search)
async def cancel_form(msg: Message, state: FSMContext):
    try:
        # Cancel search
        data = await state.get_data()
        await bot.delete_message(config.CHANNELS[data['tariff']], data['msg_id'])
        await msg.answer("Поиск отменён")
    except MessageToDeleteNotFound:
        await msg.answer("Для отмены свяжитесь с водителем")


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_form(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await States.first()
    await msg.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['contact'], state=States.contact)
async def register_user(msg: Message):
    db.register_user(msg.from_user.id, msg.contact.first_name, msg.contact.phone_number)
    await msg.answer(
        "Отлично! Для нового заказа\n/new_order",
        reply_markup=ReplyKeyboardRemove()
    )
    await States.first()


@dp.message_handler(commands=['new_order'], state=States.order)
async def order_taxi(msg: Message):
    await msg.answer(
        "Отправте геопозицию, куда должна подъехать машина.",
        reply_markup=reply_keyboards.location
    )
    await States.next()


@dp.message_handler(content_types=['location', 'venue'], state=States.location)
async def get_location(msg: Message, state: FSMContext):
    await state.update_data(lat=msg.location.latitude, lon=msg.location.longitude)
    await msg.answer("Выберите тариф", reply_markup=inline_keyboards.tariff)
    await States.next()
