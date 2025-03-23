import datetime

from aiogram import F, types, Router, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatMemberStatus

from handlers.menu_processing import get_menu_content, def_choice_catalog, def_show_order, \
    def_payment, def_orders_paid, def_choice_faq, def_new_question_faq, job_with_excel, def_clear_message

from database.orm_query import *

from keyboards.inline import MenuCallBack, get_catalog_btns

from config import logger


user_router = Router()


async def is_user_subscribed(bot: Bot, channel_url: str, telegram_id: int):
    try:
        # Получаем username канала из URL
        channel_username = channel_url.split('/')[-1]

        # Получаем информацию о пользователе в канале
        member = await bot.get_chat_member(chat_id=f"@{channel_username}", user_id=telegram_id)

        # Проверяем статус пользователя
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
            return True
        else:
            return False
    except Exception as e:
        logger.info(f"Ошибка при проверке подписки: {e}", telegram_id=telegram_id)
        return False


async def control_user_subscribed(message: types.Message, bot: Bot, session: AsyncSession, state: FSMContext,
                                  telegram_id: int):
    # проверка подписок
    subscriptions = await orm_get_subscriptions(session)
    if not subscriptions:
        return True     # подписок нет
    text = 'Для использования бота, вам необходимо подписаться на каналы и затем вновь ввести /start:\n'
    ready = True
    for subscription in subscriptions:
        if not await is_user_subscribed(bot, subscription.url, telegram_id):
            ready = False
            text += f'{subscription.name}: {subscription.url}\n'
    if not ready:
        message_show = await message.answer(text)
        messages_show = {'control_message': ['text', message_show.message_id]}
        await state.update_data({'messages_show': messages_show})

        logger.info("У клиента нет подписок!", telegram_id=telegram_id)
        return False
    return True


@user_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    if await control_user_subscribed(message, bot, session, state, message.from_user.id):
        logger.info("Клиент стартовал!", telegram_id=message.from_user.id)

        await message.answer('Бот онлайн магазина!')
        telegram_id = message.from_user.id

        await orm_get_user(session, telegram_id, message.from_user.first_name)

        if await state.get_data():
            await def_clear_message(bot, state, telegram_id)

        await state.update_data({'messages_show': None})
        await state.update_data({'get_message': None})
        await state.update_data({'message_error': None})

        text, reply_markup = await def_choice_catalog(session, state, bot, 0, telegram_id)

        edit_message = await message.answer(text, reply_markup=reply_markup)
        await state.update_data({'edit_message_text': edit_message.message_id})


@user_router.message(Command('catalog'))
async def catalog_cmd(message: types.Message, session: AsyncSession, bot: Bot, state: FSMContext):
    logger.info("Клиент ввел команду catalog!", telegram_id=message.from_user.id)

    await message.delete()

    text, reply_markup = await def_choice_catalog(session, state, bot, 0, message.from_user.id)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


@user_router.message(Command('cart'))
async def cart_cmd(message: types.Message, bot: Bot, session: AsyncSession, state: FSMContext):
    logger.info("Клиент ввел команду cart!", telegram_id=message.from_user.id)

    await message.delete()

    text, reply_markup = await def_show_order(message, bot, session, state, message.from_user.id, 5)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


@user_router.message(Command('orders'))
async def orders_cmd(message: types.Message, bot: Bot, session: AsyncSession, state: FSMContext):
    logger.info("Клиент ввел команду orders!", telegram_id=message.from_user.id)

    await message.delete()

    text, reply_markup = await def_orders_paid(bot, session, state, message.from_user.id, 10)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


@user_router.message(Command('faq'))
async def faq_cmd(message: types.Message, bot: Bot, state: FSMContext):
    logger.info("Клиент ввел команду faq!", telegram_id=message.from_user.id)

    await message.delete()

    text, reply_markup = await def_choice_faq(bot, state, message.from_user.id, 20)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


@user_router.message(Command('about'))
async def about_cmd(message: types.Message, bot: Bot, state: FSMContext):
    logger.info("Клиент ввел команду about!", telegram_id=message.from_user.id)

    await message.delete()

    text = 'Бот онлайн магазина.'
    reply_markup = get_catalog_btns()
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack,
                    session: AsyncSession, bot: Bot, state: FSMContext):
    text, reply_markup = await get_menu_content(
            callback.message,
            session,
            bot,
            state,
            telegram_id=callback.from_user.id,
            level=callback_data.level,
            data_int1=callback_data.data_int1,
            data_int2=callback_data.data_int2,
            data_int3=callback_data.data_int3,
            data_int4=callback_data.data_int4,
            data_string=callback_data.data_string,
            page=callback_data.page)

    if text:
        await def_refresh_message(bot, state, callback.from_user.id, reply_markup, text)


# **************************************************************************
async def def_refresh_message(
        bot: Bot, state: FSMContext, telegram_id: int, reply_markup, text):
    data_state = await state.get_data()
    edit_message = data_state['edit_message_text']
    # редактирую текст
    await bot.edit_message_text(text=text,
                                chat_id=telegram_id,
                                message_id=edit_message,
                                reply_markup=reply_markup,
                                parse_mode='Markdown')


# ****************************************************************************************************
@user_router.message(F.text)
async def def_message_text(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    data_state = await state.get_data()
    get_message = data_state['get_message']
    await message.delete()

    if get_message == 'new_address':
        await def_new_address(message, bot, state, session)
    elif get_message == 'new_question':
        await def_new_question(message, bot, state, session)


async def def_new_address(message: types.Message, bot: Bot, state: FSMContext, session: AsyncSession):
    logger.info("Клиент ввел новый адрес!", telegram_id=message.from_user.id)

    # прием  нового адреса
    data_state = await state.get_data()
    order_id = data_state['order_id']

    text, reply_markup = await def_payment(bot, session, state, message.from_user.id,
                                           8, order_id, message.text)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


async def def_new_question(message: types.Message, bot: Bot, state: FSMContext, session: AsyncSession):
    logger.info("Клиент ввел новый вопрос!", telegram_id=message.from_user.id)

    # прием  нового вопроса
    question_id = await orm_add_question(session, message.text, message.from_user.id)

    text, reply_markup = await def_new_question_faq(session, state, 23, question_id)
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)


# ****************************************************************************************************
@user_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)


@user_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message,  state: FSMContext, session: AsyncSession, bot: Bot) -> None:
    logger.info("Клиент произвел оплату!", telegram_id=message.from_user.id)

    data_state = await state.get_data()

    order_id = data_state['order_id']
    payment_info = str(message.successful_payment.telegram_payment_charge_id)
    await orm_change_order_payment(session, order_id, payment_info, datetime.datetime.now())

    # удаляю сообщение
    messages_show = data_state['messages_show']
    message_show = messages_show['control_message']
    await bot.delete_message(message.from_user.id, message_show[1])
    await state.update_data({'messages_show': None})

    text = 'Заказ успешно оплачен!\nОжидайте поставку.'
    reply_markup = get_catalog_btns()
    await def_refresh_message(bot, state, message.from_user.id, reply_markup, text)

    await job_with_excel(session, message.from_user.id, order_id)


@user_router.message()
async def def_error(message: types.Message):
    await message.delete()


# ***********************************************************************************
async def def_timer_dispatch(session_scheduler: AsyncSession, bot: Bot):
    dispatchs = await orm_get_dispatchs(session_scheduler)
    if dispatchs:
        for dispatch in dispatchs:
            text = f'*Рассылка от бота:* _{dispatch.text}_'
            users = await orm_get_users(session_scheduler)
            for user in users:
                await bot.send_message(chat_id=user.telegram_id, text=text, parse_mode='Markdown')
            await orm_change_dispatch(session_scheduler, dispatch.id)
            logger.info("Бот произвел рассылку!", telegram_id=0)
