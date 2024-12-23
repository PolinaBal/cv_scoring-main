import requests
from bs4 import BeautifulSoup

# Функция для получения HTML-страницы
def get_html(url: str):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/58.0.3029.110 Safari/537.36"
                )
            },
        )
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise ValueError(f"Error fetching the URL: {url}. Details: {e}")

# Функция для извлечения данных о кандидате
def extract_candidate_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def safe_find(tag, attrs, default="N/A"):
        element = soup.find(tag, attrs)
        return element.text.strip() if element else default

    name = safe_find("h2", {"data-qa": "bloko-header-1"})
    location = safe_find("span", {"data-qa": "resume-personal-address"})
    job_title = safe_find("span", {"data-qa": "resume-block-title-position"})
    skills_section = soup.find("div", {"data-qa": "skills-table"})
    skills = [
        skill.text.strip()
        for skill in skills_section.find_all("span", {"data-qa": "bloko-tag__text"})
    ] if skills_section else []

    markdown = f"""
# {name}

**Местоположение:** {location}  
**Должность:** {job_title}  

---

## Ключевые навыки
{', '.join(skills) if skills else 'N/A'}
"""
    return markdown.strip()

# Функция для извлечения данных о вакансии
def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def safe_find(tag, attrs, default="N/A"):
        element = soup.find(tag, attrs)
        return element.text.strip() if element else default

    title = safe_find("h1", {"data-qa": "vacancy-title"})
    salary = safe_find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    description = safe_find("div", {"data-qa": "vacancy-description"})

    markdown = f"""
# {title}

**Зарплата:** {salary}  

---

## Описание вакансии
{description}
"""
    return markdown.strip()

# Функция для получения данных о кандидате
def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)

# Функция для получения данных о вакансии
def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)





