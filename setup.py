from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'sspipe', 'version.py')) as f:
    exec(f.read())
    
setup(
    name='sspipe',
    version=__version__,
    description='Simple Smart Pipe Operator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://sspipe.github.io/',
    project_urls={
        'Source': 'https://github.com/sspipe/sspipe',
    },
    author='Mohammad Hossein Sekhavat',
    author_email='sekhavat17@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='pipe helper tool magrittr data science',
    packages=find_packages(exclude=[]),
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
    install_requires=[
        'pipe',
    ]
)
