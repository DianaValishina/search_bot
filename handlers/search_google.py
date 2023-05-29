import googlesearch
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot
from handlers.start import StartForm


async def answer_search_google(call: CallbackQuery, state: FSMContext):
    """This handler works when user taps 'Google'"""

    state_data = await state.get_data()
    user_question = state_data["user_question"]

    result = googlesearch.search(user_question, num_results=1, advanced=True)
    for result in googlesearch.search(user_question, num_results=1, advanced=True):
        url_question = result.url
        title_question = result.title
        description_question = result.description

    await call.message.edit_text(text="Ищу ответ в Google...", reply_markup=None)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Ссылка на первый результат поиска", url=url_question)
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text=f"Вот что нашлось по запросу {user_question}:\n<b>Название сайта</b>: {title_question}\n<b>Описание сайта</b>: {description_question}",
        reply_markup=keyboard,
    )


async def register_google(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        answer_search_google,
        lambda call: call.data and call.data == "search_google",
        state=StartForm.where_search,
    )
