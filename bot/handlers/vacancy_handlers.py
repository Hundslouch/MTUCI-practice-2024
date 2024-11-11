from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from parser import search_vacancies
from utils import (
    create_pagination_keyboard,
    extract_params,
    format_vacancies,
    strip_html_tags,
    insert_vacancies,
    fetch_vacancies,
    calculate_max_pages,
)

vacancy_router = Router()


@vacancy_router.message(Command("getvacancies"))
async def handle_get_vacancies(message: Message):
    params = extract_params(message.text)
    header = f'<b>{" ".join(params.values()) + f"\n\n"}</b>'
    vacancies = list(await search_vacancies(**params))
    await insert_vacancies(vacancies)
    vacancies = await fetch_vacancies(**params, page=1, page_size=2)
    total_pages = await calculate_max_pages(**params, page_size=2)

    await message.reply(
        strip_html_tags(header + format_vacancies(vacancies)),
        parse_mode="HTML",
        disable_web_page_preview=True,
        reply_markup=create_pagination_keyboard(1, total_pages),
    )


if __name__ == "__main__":
    test_cases = [
        "/getvacancies программист, москва, 10000",
        "/getvacancies программист москва, 10000",
        "/getvacancies программист москва 10000",
        "/getvacancies программист москва",
        "/getvacancies программист, ",
    ]
    for i, test in enumerate(test_cases, 1):
        print(i, extract_params(test))
