from datetime import datetime
from random import choice
from typing import List

from company.models import Company
from news.models import News


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
    print(f'        + News \'{news.news_id}\' ({news.date_time}) created', )
    return news


def random_news(nouns: List[str], company: Company, date_time: datetime) -> News:
    news = create_news(
        company=company,
        title=choice(nouns),
        date_time=date_time,
        snippet='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere massa et ligula '
                'semper, sed efficitur felis tincidunt. Etiam pellentesque dui vel feugiat porta. Nullam '
                'mauris urna, dictum quis neque vel, rhoncus cursus tortor. Mauris at dignissim metus. Nam '
                'ac eros sed turpis cursus tristique. Nam auctor commodo justo, sed volutpat risus '
                'elementum quis. Orci varius natoque penatibus et magnis dis parturient montes, '
                'nascetur ridiculus mus. Pellentesque lacinia nulla non erat blandit ultrices. Aenean '
                'pharetra a eros vel varius. Quisque vitae ipsum sed neque tempor maximus. Vestibulum quis '
                'leo fringilla, cursus tortor ac, finibus arcu.',
        url=f'https://example.com/{choice(nouns)}-{choice(nouns)}-{choice(nouns)}-{choice(nouns)}'
    )
    return news
