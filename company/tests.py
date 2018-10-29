from django.db import IntegrityError
from django.test import TestCase

from company.models import Company


# Create your tests here.
class CompanyTestCase(TestCase):
    def test_create_company(self):
        company = Company.objects.create(
            name='Name',
            industry='Industry',
            description='Description',
            exchange='Exchange',
            country='US',
        )
        self.assertEqual(Company.objects.count(), 1)
        self.assertIsNotNone(company.id)
        self.assertEqual(company.name, 'Name')
        self.assertEqual(company.industry, 'Industry')
        self.assertEqual(company.description, 'Description')
        self.assertCountry(company, 'United States of America', 'US', 'USA', 840)

    def test_create_company_without_name(self):
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            industry='Industry',
            description='Description',
            exchange='Exchange',
            country='US',
        )

    def test_create_company_without_industry(self):
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name='Name',
            description='Description',
            exchange='Exchange',
            country='US',
        )

    def test_create_company_without_description(self):
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name='Name',
            industry='Industry',
            exchange='Exchange',
            country='US',
        )

    def test_create_company_without_exchange(self):
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name='Name',
            industry='Industry',
            description='Description',
            country='US',
        )

    def test_create_company_without_country(self):
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name='Name',
            industry='Industry',
            description='Description',
            exchange='Exchange',
        )

    def test_create_duplicate_company(self):
        Company.objects.create(
            name='Name',
            industry='Industry',
            description='Description',
            exchange='Exchange',
            country='US',
        )
        self.assertRaises(
            IntegrityError,
            Company.objects.create,
            name='Name',
            industry='Industry',
            description='Description',
            exchange='Exchange',
            country='US',
        )

    def assertCountry(self, company: Company, name: str, code: str, alpha3: str, numeric: int):
        self.assertIsNotNone(company.country)
        self.assertEqual(company.country.name, name)
        self.assertEqual(company.country.code, code)
        self.assertEqual(company.country.alpha3, alpha3)
        self.assertEqual(company.country.numeric, numeric)
