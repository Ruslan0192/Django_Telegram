
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix="rent"):
    level: int
    data_int1: int | None = None
    data_int2: int | None = None
    data_int3: int | None = None
    data_int4: int | None = None
    data_string: str | None = None
    page: int = 1


def get_callback_btns(*, btns: dict[str, str], sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()

    for text, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()


# ***************************************************************************************
def get_choice_catalog_btns(*, level: int, data_list: list, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    for c in data_list:
        keyboard.add(InlineKeyboardButton(text=c.name,
                                          callback_data=MenuCallBack(level=level + 1,
                                                                     data_int1=c.id,
                                                                     page=1).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_catalog_btns(*, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Каталог',
                                      callback_data=MenuCallBack(level=0).pack()))
    return keyboard.adjust(*sizes).as_markup()


# def get_dispatch_btns(*, sizes: tuple[int] = (2,)):
#     keyboard = InlineKeyboardBuilder()
#     keyboard.add(InlineKeyboardButton(text='ОК'))
#     return keyboard.adjust(*sizes).as_markup()


def get_empty_data_btns(*, level: int, back_id: int = 0, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1,
                                                                 data_int1=back_id,
                                                                 page=1).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_choice_category_btns(*,
                             level: int,
                             page: int,
                             id_value: int = 0,
                             back_id: int = 0,
                             pagination_btns: dict,
                             data_list: list,
                             sizes: tuple[int] = (2, )):
    keyboard = InlineKeyboardBuilder()
    if pagination_btns:
        if len(pagination_btns.items()) % 2:
            sizes = (1, 2, )
        else:
            sizes = (2, )
        for text, menu_name in pagination_btns.items():
            if menu_name == "next":
                keyboard.add(InlineKeyboardButton(text=text,
                                                  callback_data=MenuCallBack(
                                                    level=level,
                                                    data_int1=id_value,
                                                    page=page + 1).pack()))

            elif menu_name == "previous":
                keyboard.add(InlineKeyboardButton(text=text,
                                                  callback_data=MenuCallBack(
                                                    level=level,
                                                    data_int1=id_value,
                                                    page=page - 1).pack()))
    for c in data_list:
        keyboard.add(InlineKeyboardButton(text=c.name,
                                          callback_data=MenuCallBack(level=level + 1,
                                                                     data_int1=c.id).pack()))

    row = [InlineKeyboardButton(text='Назад',
                                callback_data=MenuCallBack(
                                        level=level - 1,
                                        data_int1=back_id,
                                        page=1).pack()), ]
    keyboard.adjust(*sizes)
    return keyboard.row(*row).as_markup()


def get_choice_product_btns(*,
                            level: int,
                            product_id: int,
                            order_id: int,
                            cart_id: int,
                            flags_cart: bool,
                            quantity: float,
                            flags_views: bool,
                            sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    if flags_cart:
        keyboard.add(InlineKeyboardButton(text='Убрать',
                                          callback_data=MenuCallBack(level=level,
                                                                     data_int1=product_id,
                                                                     data_int2=order_id,
                                                                     data_int3=cart_id,
                                                                     data_int4=quantity-1,
                                                                     data_bool=flags_cart).pack()))
        keyboard.add(InlineKeyboardButton(text='Добавить',
                                          callback_data=MenuCallBack(level=level,
                                                                     data_int1=product_id,
                                                                     data_int2=order_id,
                                                                     data_int3=cart_id,
                                                                     data_int4=quantity+1,
                                                                     data_bool=flags_cart).pack()))
    else:
        if not flags_views:
            keyboard.add(InlineKeyboardButton(text='Добавить в корзину',
                                              callback_data=MenuCallBack(level=level,
                                                                         data_int1=product_id,
                                                                         data_int2=order_id,
                                                                         data_int3=cart_id,
                                                                         data_int4=1).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_choice_product_last_btns(*, level: int, back_id: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 2,
                                                                 data_int1=back_id,
                                                                 page=1).pack()))
    keyboard.add(InlineKeyboardButton(text='Корзина',
                                      callback_data=MenuCallBack(level=level + 1).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_show_order_last_btns(*, level: int, order_id: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Каталог',
                                      callback_data=MenuCallBack(level=0).pack()))
    keyboard.add(InlineKeyboardButton(text='Заказать',
                                      callback_data=MenuCallBack(level=level + 1,
                                                                 data_int1=order_id).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_choice_address_btns(*, level: int, orders: list, order_id: int, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for c in orders:
        if c.address:
            keyboard.add(InlineKeyboardButton(text=c.address,
                                              callback_data=MenuCallBack(level=level + 1,
                                                                         data_int1=order_id,
                                                                         data_string=c.address).pack()))
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 2).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_user_payment_btns(*, level: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Оплатить',
                                      callback_data=MenuCallBack(level=level + 1,
                                                                 menu_name='payment_card',
                                                                 category_control_type=True,).pack()))
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1,
                                                                 menu_name='payment').pack()))


def get_choice_orders_btns(*, level: int, orders: list, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for c in orders:
        if c.address:
            keyboard.add(InlineKeyboardButton(text=f'от {c.date_paid}',
                                              callback_data=MenuCallBack(level=level + 1,
                                                                         data_int1=c.id).pack()))
    keyboard.add(InlineKeyboardButton(text='Каталог',
                                      callback_data=MenuCallBack(level=0).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_show_order_paid_last_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Каталог',
                                      callback_data=MenuCallBack(level=0).pack()))
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_choice_faq_btns(*, level: int, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Задать новый вопрос',
                                      callback_data=MenuCallBack(level=level + 2).pack()))
    keyboard.add(InlineKeyboardButton(text='Мои вопросы',
                                      callback_data=MenuCallBack(level=level + 1).pack()))
    keyboard.add(InlineKeyboardButton(text='Каталог',
                                      callback_data=MenuCallBack(level=0).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_choice_question_btns(*, level: int, questions: list, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    for c in questions:
        keyboard.add(InlineKeyboardButton(text=c.question,
                                          callback_data=MenuCallBack(level=level + 1,
                                                                     data_int1=c.id).pack()))
    keyboard.add(InlineKeyboardButton(text='Назад',
                                      callback_data=MenuCallBack(level=level - 1).pack()))
    return keyboard.adjust(*sizes).as_markup()
