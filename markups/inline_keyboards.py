from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tariff = InlineKeyboardMarkup(2).add(
    InlineKeyboardButton("Комфорт", callback_data="comfort"),
    InlineKeyboardButton("Эконом", callback_data="economy")
)
confirm = InlineKeyboardMarkup(2).add(
    InlineKeyboardButton("Да", callback_data="1"),
    InlineKeyboardButton("Нет", callback_data="0")
)


def get_take_order_btn(user_id):
    return InlineKeyboardMarkup(1).add(
        InlineKeyboardButton("Взять заказ", callback_data=user_id)
    )


def get_driver_contact_btn(name, phone):
    return InlineKeyboardMarkup(1).add(
        InlineKeyboardButton("Связь с водителем", callback_data=f'{name} {phone}')
    )


def get_driver_btns(name, phone, client_id):
    return InlineKeyboardMarkup(2).add(
        InlineKeyboardButton("Связь с клиентом", callback_data=f'{name} {phone}'),
        InlineKeyboardButton("Я на месте", callback_data=str(client_id))
    )
