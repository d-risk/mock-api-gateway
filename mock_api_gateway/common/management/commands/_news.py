from datetime import datetime, timezone
from random import choice
from typing import List

from mock_api_gateway.company.models import Company
from mock_api_gateway.news.models import News


def create_news(
        company: Company,
        title: str,
        date_time: datetime,
        snippet: str,
        url: str,
) -> News:
    news = News.objects.create(
        company_id=company.company_id,
        title=title,
        date_time=date_time,
        snippet=snippet,
        url=url,
    )
    print(f"        + News '{news.news_id}' ({news.date_time}) created", )
    return news


def random_news(nouns: List[str], company: Company, date_time: datetime, ) -> News:
    news = create_news(
        company=company,
        title=f"{choice(nouns)} {choice(nouns)} {choice(nouns)}",
        date_time=date_time,
        snippet="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere massa et ligula "
                "semper, sed efficitur felis tincidunt. Etiam pellentesque dui vel feugiat porta. Nullam "
                "mauris urna, dictum quis neque vel, rhoncus cursus tortor. Mauris at dignissim metus. Nam "
                "ac eros sed turpis cursus tristique."
                "\n"
                "Nam auctor commodo justo, sed volutpat risus "
                "elementum quis. Orci varius natoque penatibus et magnis dis parturient montes, "
                "nascetur ridiculus mus. Pellentesque lacinia nulla non erat blandit ultrices. Aenean "
                "pharetra a eros vel varius. Quisque vitae ipsum sed neque tempor maximus. Vestibulum quis "
                "leo fringilla, cursus tortor ac, finibus arcu.",
        url=f"https://example.com/{choice(nouns)}-{choice(nouns)}-{choice(nouns)}-{choice(nouns)}",
    )
    return news


def random_news_list(nouns: List[str], company: Company, from_year: int, to_year: int) -> List[News]:
    news_lists: List[News] = []
    for year in range(from_year, to_year + 1):
        for x in [1, 6, 12, ]:
            date_time = datetime(year=year, month=x, day=x, tzinfo=timezone.utc, )
            news = random_news(nouns=nouns, company=company, date_time=date_time, )
            news_lists.append(news, )
    return news_lists
