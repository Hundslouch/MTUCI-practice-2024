import asyncio
from aiohttp import ClientSession, TCPConnector


async def fetch_region_id(city: str):
    connector = TCPConnector(ssl=False)
    async with ClientSession(connector=connector) as session:
        response = await session.get("https://api.hh.ru/areas")
        areas = await response.json()
        for country in areas:
            if country["name"] == city:
                return country["id"]
            for region in country.get("areas", []):
                if region["name"] == city:
                    return region["id"]
                for city_ in region.get("areas", []):
                    if city_["name"] == city:
                        return city_["id"]


async def fetch_vacancies_data(
    query, per_page: int = 100, city: str = None, salary: int = None
) -> list[dict]:
    connector = TCPConnector(ssl=False)
    url = f"https://api.hh.ru/vacancies?per_page={per_page}&text={query}&only_with_salary=true"
    if salary:
        url += f"&salary={salary}"
    if city:
        if city_id := await fetch_region_id(city):
            url += f"&area={city_id}"
    async with ClientSession(connector=connector) as session:
        tasks = [session.get(url + f"&page={page}") for page in range(1, 10)]
        responses = await asyncio.gather(*tasks)
        results = [await response.json() for response in responses]
        return [item for result in results for item in result.get("items", [])]


def process_vacancy(vacancy):
    salary = vacancy.get("salary")
    salary_info = "не указана"
    if salary:
        salary_from = salary.get("from", "")
        salary_to = salary.get("to", "")
        salary_info = (
            f"от {salary_from}"
            if salary_from
            else f"до {salary_to}" if salary_to else "не указана"
        )
    return {
        "hh_id": int(vacancy["id"]),
        "name": vacancy["name"],
        "city": vacancy["area"]["name"],
        "experience": vacancy["experience"]["name"],
        "employment": vacancy["employment"]["name"],
        "requirement": vacancy["snippet"]["requirement"],
        "responsibility": vacancy["snippet"]["responsibility"],
        "salary": salary_info.split(" ")[1],
        "link": f"https://hh.ru/vacancy/{vacancy['id']}?from=applicant_recommended&hhtmFrom=main",
    }


async def search_vacancies(
    query: str, city: str = None, salary: int = None, per_page: int = 100
) -> list[dict]:
    vacancies_data = await fetch_vacancies_data(
        query, city=city, salary=salary, per_page=per_page
    )
    return [process_vacancy(data) for data in vacancies_data]


if __name__ == "__main__":
    query = "Python"
    city = "Москва"
    salary = 100000
    vacancies = asyncio.run(search_vacancies(query, city=city, salary=salary))
    print(vacancies)
