from typing import Tuple

from company.models import Company


def create_company(
        name: str,
        description: str,
        industry: str,
        exchange: str,
        country: str,
) -> Tuple[Company, bool]:
    company, created = Company.objects.get_or_create(
        name=name,
        description=description,
        industry=industry,
        exchange=exchange,
        country=country,
    )
    s = 'created' if created else 'already exists'
    print(f'    + Company \'{company.name}\' ({company.id}) {s}')
    return company, created
