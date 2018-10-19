from typing import Tuple

from company.models import Company


def create_company(
        name: str,
        description: str = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere massa et ligula '
                           'semper, sed efficitur felis tincidunt. Etiam pellentesque dui vel feugiat porta. Nullam '
                           'mauris urna, dictum quis neque vel, rhoncus cursus tortor. Mauris at dignissim metus. Nam '
                           'ac eros sed turpis cursus tristique. Nam auctor commodo justo, sed volutpat risus '
                           'elementum quis. Orci varius natoque penatibus et magnis dis parturient montes, '
                           'nascetur ridiculus mus. Pellentesque lacinia nulla non erat blandit ultrices. Aenean '
                           'pharetra a eros vel varius. Quisque vitae ipsum sed neque tempor maximus. Vestibulum quis '
                           'leo fringilla, cursus tortor ac, finibus arcu.'
                           ''
                           'Cras ex velit, lobortis quis malesuada quis, dignissim vitae eros. Praesent arcu nibh, '
                           'porttitor eget dui sed, convallis venenatis justo. Donec a quam non velit fermentum '
                           'suscipit. Duis ultrices iaculis mauris, at malesuada odio feugiat ac. Nullam et accumsan '
                           'nibh. Proin libero magna, tempus sit amet tincidunt sit amet, venenatis eget dui. Cras '
                           'dignissim, felis et consectetur bibendum, tellus elit dignissim velit, sed faucibus enim '
                           'ipsum eget lectus. Vestibulum lobortis rhoncus nulla. Vestibulum hendrerit lorem orci, '
                           'id hendrerit lorem accumsan vel. Nunc elementum tortor quam, id lacinia turpis aliquam a. '
                           'Sed vel vestibulum augue. Donec vulputate et justo vel tincidunt.',
        industry: str = 'industry',
) -> Tuple[Company, bool]:
    company, created = Company.objects.get_or_create(
        defaults={
            'description': description,
            'industry': industry,
        },
        name=name,
    )
    s = 'created' if created else 'already exists'
    print(f'    + Company \'{company.name}\' ({company.id}) {s}')
    return company, created
