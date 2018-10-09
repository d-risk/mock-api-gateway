from setuptools import setup, find_packages


def _license():
    with open('LICENSE') as f:
        return f.read()


def _readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='credit-report-service',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='https://github.com/d-risk/credit-report-service',
    license=_license(),
    author='Christopher Zhong',
    author_email='christopher.zhong@d-risk.tech',
    description='D-Risk\'s Credit Report Service',
    long_description=_readme(),
    install_requires=[
        'graphene',
        'django',
        'graphene_django',
    ],
    keywords='api graphene credit-rating risk-assessment graphql',
    # test_suite='nose.collector',
    # tests_require=['nose'], install_requires=['graphene']
)
