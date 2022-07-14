from dispatcher import dp, bot
from states import States
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from markups import inline_keyboards
import config
from bot import db
from aiogram.types import ReplyKeyboardRemove


@dp.callback_query_handler(state=States.tariff)
async def choose_tariff(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await state.update_data(tariff=call.data)
    await call.message.edit_text(
        f"Сумма заказа составит {59 if call.data == 'economy' else 79} от сом. Продолжить?",
        reply_markup=inline_keyboards.confirm
    )
    await States.next()


@dp.callback_query_handler(state=States.confirm)
async def confirm(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    if int(call.data):
        # Search
        await call.message.edit_text("Поиск машины...")
        await States.next()

        data = await state.get_data()
        msg = await bot.send_location(
            config.CHANNELS[data['tariff']],
            data['lat'], data['lon'],
            reply_markup=inline_keyboards.get_take_order_btn(call.from_user.id)
        )
        await state.update_data(msg_id=msg.message_id)
    else:
        await call.message.edit_text("Выберите тариф. Для отмены\n/cancel", reply_markup=inline_keyboards.tariff)
        await States.previous()


@dp.callback_query_handler(is_channel=True)
async def take_order(call: CallbackQuery):
    await call.message.delete()

    # Define tariff
    for channel in config.CHANNELS:
        if config.CHANNELS[channel] == call.message.chat.id:
            table = channel
            break

    driver_info = db.get_driver_info(call.from_user.id, table)
    client_info = db.check_user_exists(call.data)

    # Client
    await bot.send_message(
        call.data, f"Скоро приедет <b>{driver_info[-1]}</b>",
        parse_mode='HTML', reply_markup=inline_keyboards.get_driver_contact_btn(driver_info[1], driver_info[2])
    )
    # Driver
    await bot.send_location(
        call.from_user.id, call.message.location.latitude, call.message.location.longitude,
        reply_markup=inline_keyboards.get_driver_btns(client_info[1], client_info[2], call.data)
    )


@dp.callback_query_handler(is_contact=True, state='*')
async def send_contact(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    name, phone = call.data.split()
    await bot.send_contact(call.from_user.id, phone, name)


@dp.callback_query_handler(state='*')
async def arrive(call: CallbackQuery):
    await bot.answer_callback_query(call.id, 'Отлично! Сообщение было отправлено клиенту')
    await bot.send_message(call.data, "Машина на месте!", reply_markup=ReplyKeyboardRemove())
