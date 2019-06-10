from uuid import uuid4

from django.test import TestCase
from django.utils.timezone import now

from mock_api_gateway.news.models import News


# Create your tests here.
class NewsTestCase(TestCase):
    def test_create_news(self):
        company_id = uuid4()
        title = 'Title'
        date_time = now()
        snippet = 'Snippet'
        url = 'https://example.com'

        news = News.objects.create(
            company_id=company_id,
            title=title,
            date_time=date_time,
            snippet=snippet,
            url=url
        )

        self.assertEqual(News.objects.count(), 1)
        self.assertIsNotNone(news)
        self.assertIsNotNone(news.news_id)
        self.assertEqual(news.company_id, company_id)
        self.assertEqual(news.title, title)
        self.assertEqual(news.date_time, date_time)
        self.assertEqual(news.snippet, snippet)
        self.assertEqual(news.url, url)
