from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select, or_
from database.db import async_session_maker
from database.models import JobVacancy
import re


def format_JobVacancy(JobVacancy: JobVacancy) -> str:
    return f"""\
<b>{JobVacancy.name}</b>
<b>Город</b>: {JobVacancy.city}
<b>Опыт</b>: {JobVacancy.experience}
<b>Занятость</b>: {JobVacancy.employment}
<b>Требования</b>: {JobVacancy.requirement}
<b>Обязанности</b>: {JobVacancy.responsibility}
<b>Зарплата</b>: {JobVacancy.salary}
<b>Ссылка</b>: {JobVacancy.link}
"""


def create_pagination_keyboard(current: int, total: int) -> InlineKeyboardMarkup:
    buttons = []
    if current > 1:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=f"page_{current}_{current - 1}"
                )
            ]
        )
    if current < total:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="Вперёд ➡️", callback_data=f"page_{current}_{current + 1}"
                )
            ]
        )
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def format_vacancies(vacancies) -> str:
    return "\n\n".join(format_JobVacancy(JobVacancy) for JobVacancy in vacancies)


def extract_params(text: str) -> dict:
    text = text.lstrip("/getvacancies").strip().split("\n")
    params = ["query", "city", "salary"][: len(text)]
    values = [item.strip().strip(",").capitalize() for item in text]
    return dict(zip(params, values))


def extract_text_params(text: str) -> dict:
    text = text.strip().split()
    params = ["query", "city", "salary"][: len(text)]
    values = [item.capitalize() for item in text]
    return dict(zip(params, values))


def strip_html_tags(text: str) -> str:
    return re.sub(r"<(?!\/?b\b)[^>]*>", "", text)


async def fetch_vacancies(
    query: str, city: str = None, salary: int = None, page: int = 1, page_size: int = 2
) -> list[JobVacancy]:
    async with async_session_maker() as session:
        async with session.begin():
            stmt = (
                select(JobVacancy)
                .where(
                    or_(
                        JobVacancy.name.like(f"%{query}%"),
                        JobVacancy.requirement.like(f"%{query}%"),
                    ),
                    JobVacancy.city == city,
                    JobVacancy.salary.like(f"%{salary}%"),
                )
                .limit(page_size)
                .offset((page - 1) * page_size)
            )
            result = await session.execute(stmt)
            return result.scalars().all()


async def insert_vacancies(vacancies: list) -> None:
    async with async_session_maker() as db:
        async with db.begin():
            JobVacancy_objs = [JobVacancy(**v) for v in vacancies]
            existing_ids = [
                row[0]
                for row in await db.execute(select(JobVacancy.hh_id))
                if row[0] is not None
            ]
            new_vacancies = [
                JobVacancy for JobVacancy in JobVacancy_objs if JobVacancy.hh_id not in existing_ids
            ]
            db.add_all(new_vacancies)
        await db.commit()


async def calculate_max_pages(
    query: str, city: str = None, salary: int = None, page_size: int = 2
) -> int:
    async with async_session_maker() as session:
        async with session.begin():
            stmt = select(JobVacancy).where(
                or_(
                    JobVacancy.name.like(f"%{query}%"),
                    JobVacancy.requirement.like(f"%{query}%"),
                ),
                JobVacancy.city == city,
                JobVacancy.salary.like(f"%{salary}%"),
            )
            result = await session.execute(stmt)
            total = len(result.scalars().all())
            return (total // page_size) + 1 if total % page_size else total // page_size
