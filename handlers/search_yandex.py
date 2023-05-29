import requests
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup

from bot import bot
from handlers.start import StartForm


async def answer_search_yandex(call: CallbackQuery, state: FSMContext):
    """This handler works when user taps 'Yandex'"""

    state_data = await state.get_data()
    user_question = state_data["user_question"]

    user_question = user_question.replace(" ", "+")
    url = "https://yandex.ru/search/?text=" + user_question + "&lr=118890&p=1"

    response = requests.get(url)
    response.encoding = "utf-8"

    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    keyboard = InlineKeyboardMarkup()
    items = soup.find_all("a", {"class": "organic__url"})
    if items:
        url = items[0].get["href"]
        keyboard.add(
            InlineKeyboardButton(text="Сссылка на первый реультат поиска", url=url)
        )
    else:
        keyboard = None

    text = soup.get_text()

    await call.message.edit_text(text=text, reply_markup=keyboard)


async def register_yandex(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        answer_search_yandex,
        lambda call: call.data and call.data == "search_yandex",
        state=StartForm.where_search,
    )
