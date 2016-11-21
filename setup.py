from setuptools import setup


setup(
    name='scrapy-corenlp',
    version='0.1',
    description='Scrapy spider middleware :: Stanford CoreNLP Named Entity Recognition',
    url='https://github.com/vu3jej/scrapy-corenlp',
    author='Jithesh E J',
    author_email='mail@jithesh.net',
    license='BSD',
    packages=['scrapy_corenlp'],
    classifiers=[
        'Development Status :: Alpha',
        'Programming Language :: Python :: 3.4',
        'Topic :: Natural Language Processing :: Named Entity Recognition',
    ]
)
