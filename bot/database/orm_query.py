from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import *


# *********************************************************************************
#     __tablename__ = 'user'
async def orm_get_user(session: AsyncSession, telegram_id: int, name: str | None = None):
    # получаю user по telegram_id
    query = select(Users).where(Users.telegram_id == telegram_id)
    result = await session.execute(query)
    user = result.scalar()
    if user:
        return user.id
    # нет клиента, создаю новый
    query = insert(Users).values(telegram_id=telegram_id, name=name, phone='')
    result = await session.execute(query)
    user_id = result.inserted_primary_key[0]
    await session.commit()
    return user_id


async def orm_get_user_telegram(session: AsyncSession, telegram_id: int):
    # получаю user по telegram_id
    query = select(Users).where(Users.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_users(session: AsyncSession):
    # получаю всех клиентов
    query = select(Users)
    result = await session.execute(query)
    return result.scalars().all()


# *********************************************************************************
#     __tablename__ = 'catalogs'
async def orm_get_catalogs(session: AsyncSession):
    # получаю весь каталог
    query = select(Catalogs)
    result = await session.execute(query)
    return result.scalars().all()


# *********************************************************************************
#     __tablename__ = 'category'
async def orm_get_categories(session: AsyncSession, catalog_id: int):
    # получаю категории
    query = select(Categories).where(Categories.catalog_id == catalog_id)
    result = await session.execute(query)
    return result.scalars().all()


# *********************************************************************************
#     __tablename__ = 'under_category'
async def orm_get_under_categories(session: AsyncSession, categories_id: int):
    # получаю подкатегории
    query = select(UnderCategories).where(UnderCategories.categories_id == categories_id)
    result = await session.execute(query)
    return result.scalars().all()


# *********************************************************************************
#     __tablename__ = 'product'
async def orm_get_products(session: AsyncSession, undercategories_id: int):
    # получаю все товары
    query = select(Products).where(Products.undercategories_id == undercategories_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_product(session: AsyncSession, product_id: int):
    # получаю товар по id
    query = select(Products).where(Products.id == product_id)
    result = await session.execute(query)
    return result.scalar()


# *********************************************************************************
#     __tablename__ = 'order'
async def orm_get_order_current(session: AsyncSession, telegram_id: int):
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    # получаю текущий заказ покупателя
    query = select(Orders).where(Orders.user_id == user_id,
                                 Orders.payment_number == None)
    result = await session.execute(query)
    order = result.scalar()
    if order:
        # найден недооформленный заказ, поиск по корзинам
        carts = await orm_get_carts(session, order.id)
        return order.id, carts

    # создаю новый заказ
    query = insert(Orders).values(user_id=user_id)
    result = await session.execute(query)
    order_id = result.inserted_primary_key[0]
    await session.commit()
    return order_id, None


async def orm_get_orders(session: AsyncSession, telegram_id: int):
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    # получаю  все заказы
    query = select(Orders).where(Orders.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_orders_for_address(session: AsyncSession, telegram_id: int):
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    # получаю  все заказы
    query = select(Orders).where(Orders.user_id == user_id).distinct(Orders.address)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_orders_paid(session: AsyncSession, telegram_id: int):
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    # получаю  все оплаченные заказы
    query = select(Orders).where(Orders.user_id == user_id, Orders.payment_number != None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_order_id(session: AsyncSession, order_id: int):
    # получаю текущий заказ
    query = select(Orders).where(Orders.id == order_id)
    result = await session.execute(query)
    order = result.scalar()

    carts = await orm_get_carts(session, order.id)
    return order, carts


async def orm_change_order_amm_adr(session: AsyncSession, order_id: int,  ammont: float, address: str):
    # изменяю итого и адрес доставки
    obj = update(Orders).where(Orders.id == order_id).values(ammont=ammont,
                                                             address=address)
    await session.execute(obj)
    await session.commit()


async def orm_change_order_payment(session: AsyncSession, order_id: int, payment_number: str, date_paid):
    # изменяю итого и адрес доставки
    obj = update(Orders).where(Orders.id == order_id).values(payment_number=payment_number,
                                                             date_paid=date_paid)
    await session.execute(obj)
    await session.commit()


# *********************************************************************************
#     __tablename__ = 'cart'
async def orm_add_cart(session: AsyncSession, order_id: int, product_id: int, quantity: int, ammont: float):
    query = insert(Carts).values(order_id=order_id,
                                 product_id=product_id,
                                 quantity=quantity,
                                 ammont=ammont)
    result = await session.execute(query)
    cart_id = result.inserted_primary_key[0]
    await session.commit()
    return cart_id


async def orm_get_carts(session: AsyncSession, order_id: int):
    # получаю все корзины для покупателя
    query = select(Carts).where(Carts.order_id == order_id)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_change_cart_qty(session: AsyncSession, cart_id: int, quantity: int, ammont: float):
    # изменяю кол-во в корзине
    obj = update(Carts).where(Carts.id == cart_id).values(quantity=quantity, ammont=ammont)
    await session.execute(obj)
    await session.commit()


async def orm_delete_cart(session: AsyncSession, cart_id: int):
    # удаляю корзину
    query = delete(Carts).where(Carts.id == cart_id)
    await session.execute(query)
    await session.commit()


# *********************************************************************************
#     __tablename__ = 'question'
async def orm_add_question(session: AsyncSession, question: str, telegram_id: int):
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    query = insert(Questions).values(question=question, user_id=user_id)
    result = await session.execute(query)
    question_id = result.inserted_primary_key[0]
    await session.commit()
    return question_id


async def orm_get_question(session: AsyncSession, question_id):
    # получаю вопрос
    query = select(Questions).where(Questions.id == question_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_questions(session: AsyncSession):
    # получаю все вопросы c ответами
    query = select(Questions).where(Questions.answer != None)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_questions_user(session: AsyncSession, telegram_id: int):
    # получаю вопросы клиента
    # ищу id клиента
    user_id = await orm_get_user(session, telegram_id)

    query = select(Questions).where(Questions.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()


# *********************************************************************************
#     __tablename__ = 'dispatch'
async def orm_get_dispatchs(session: AsyncSession):
    # получаю неотправленные рассылки
    query = select(Dispatchs).where(Dispatchs.ready == False)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_change_dispatch(session: AsyncSession, dispatch_id: int):
    # изменяю что отправлено
    obj = update(Dispatchs).where(Dispatchs.id == dispatch_id).values(ready=True)
    await session.execute(obj)
    await session.commit()


# *********************************************************************************
#     __tablename__ = 'subscription'
async def orm_get_subscriptions(session: AsyncSession):
    # получаю все необходимые подписки
    query = select(Subscriptions)
    result = await session.execute(query)
    return result.scalars().all()
