from aiogram import Router
from aiogram.types import CallbackQuery
from utils import (
    extract_text_params,
    format_vacancies,
    create_pagination_keyboard,
    strip_html_tags,
    fetch_vacancies,
    calculate_max_pages,
)


callback_router = Router()


@callback_router.callback_query()
async def handle_page_callback(call: CallbackQuery):
    if call.data.startswith("page_"):
        prev_page = int(call.data.split("_")[1])
        current_page = int(call.data.split("_")[2])
        header = call.message.text.split("\n\n")[0]
        params = extract_text_params(header)
        vacancies = list(await fetch_vacancies(**params, page=current_page))
        formatted_vacancies = format_vacancies(vacancies)
        total_pages = await calculate_max_pages(**params)
        await call.message.edit_text(
            strip_html_tags(f"<b>{header}</b>\n\n" + f"{formatted_vacancies}"),
            reply_markup=create_pagination_keyboard(current_page, total_pages),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
