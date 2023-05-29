from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from bot import bot


class StartForm(StatesGroup):
    question = State()
    where_search = State()


async def answer_start(msg: Message, state: FSMContext) -> None:
    """This handler works when user taps '/start'"""

    await bot.send_message(
        chat_id=msg.from_user.id,
        text="Привет! Введи свой вопрос и я постараюсь найти ответ🔍🧐",
    )

    await StartForm.question.set()


async def get_user_question(msg: Message, state: FSMContext):
    """This handler gets the users question"""

    await state.update_data({"user_question": msg.text})

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Google", callback_data="search_google"))
    keyboard.add(InlineKeyboardButton(text="Yandex", callback_data="search_yandex"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_question"))

    await bot.send_message(
        chat_id=msg.from_user.id, text="Где будем искать ответ?🗃", reply_markup=keyboard
    )

    await StartForm.where_search.set()


async def answer_back(call: CallbackQuery):
    """Thos handler works when user taps 'Назад'"""

    await call.message.edit_text(
        text="Если хочешь найти ответ на свой вопрос, напиши вопрос мне!",
        reply_markup=None,
    )


async def register_start(dp: Dispatcher) -> None:
    dp.register_message_handler(answer_start, commands=["start"], state="*")
    dp.register_message_handler(get_user_question, state=StartForm.question)
    dp.register_callback_query_handler(
        answer_back,
        lambda call: call.data and call.data == "back_question",
        state=StartForm.where_search,
    )
