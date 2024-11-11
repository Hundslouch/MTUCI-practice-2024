from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

command_router = Router()


@command_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Добрый день! Этот бот поможет вам найти вакансии на hh.ru."
        "\n\nВведите /help для списка доступных команд."
        "\n\nДля поиска вакансий используйте следующий формат запроса:"
        "\n\n/getvacancies"
        "\nназвание должности"
        "\nгород"
        "\nжелаемая зарплата"
    )


@command_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Список доступных команд:"
        "\н/start — Начать использование"
        "\н/contacts — Контакты для связи"
        "\н/help — Помощь"
    )


@command_router.message(Command("contacts"))
async def contacts_command(message: Message):
    await message.answer(
        "Контакты для связи:"
        "\н[Telegram](t.me/penetrat1ve)"
        "\н[GitHub](github.com/wixucys)"
        "\н[Ссылка на сайт HeadHunter](hh.ru)",
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )
