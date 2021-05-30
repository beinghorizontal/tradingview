from setuptools import setup,find_packages

find_packages()

packs = ['selenium==3.141.0', 'chromedriver_autoinstaller==0.2.2', 'pandas==1.2.3',
         'beautifulsoup4==4.9.3', 'websocket_client==1.0.1']

setup(
    name='tradingviewscraper',
    version='1.1.0',
    packages=packs,
    install_requires=packs,
    url='https://www.github.com/beinghorizontal',
    license='MIT',
    author='alex1',
    author_email='',
    description='Scrape data from Trading View'

)
