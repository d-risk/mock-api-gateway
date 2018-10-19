from datetime import datetime

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
        company_id=company.id,
        title=title,
        date_time=date_time,
        snippet=snippet,
        url=url,
    )
    print(
        f'        + News \'{news.id}\' ({news.date_time}) created', )
    return news
