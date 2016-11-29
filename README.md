# scrapy-corenlp

[![PyPI](https://img.shields.io/pypi/v/scrapy-corenlp.svg?style=flat-square)]()
[![PyPI](https://img.shields.io/pypi/pyversions/scrapy-corenlp.svg?style=flat-square)]()

A [Scrapy][scrapy] middleware to perform Named Entity Recognition (NER) on response with Stanford CoreNLP.

## Settings

| Option                        | Value                                                         | Example Value                                                                               |
|-------------------------------|---------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| STANFORD_NER_ENABLED          | Boolean                                                       | `True`                                                                                      |
| STANFORD_NER_CLASSIFIER       | absolute path to `CRFClassifier`                              | `'/home/jithesh/stanford-ner-2015-12-09/classifiers/english.muc.7class.distsim.crf.ser.gz'` |
| STANFORD_NER_JAR              | absolute path to `stanford-ner.jar` file                      | `'/home/jithesh/stanford-ner-2015-12-09/stanford-ner.jar'`                                  |
| STANFORD_NER_FIELD_TO_PROCESS | A field or list of Item text fields to use for classification | `['title', 'description']`                                                                  |
| STANFORD_NER_FIELD_OUTPUT     | scrapy item field to update the result with                   | `'result'`                                                                                  |

In your `settings.py` file, add the previously described settings and add `CoreNLP` to your `SPIDER_MIDDLEWARES`, e.g.

```python
SPIDER_MIDDLEWARES = {
    'scrapy_corenlp.middlewares.CoreNLP': 543,
}
```

An example value of the `STANFORD_NER_FIELD_OUTPUT` field after recognising the entities is:

```json
{"result": {"DATE": ["1963", "2009", "1979", "1663", "1982"], "ORGANIZATION": ["Royal Society", "US National Academy of Science", "University of California", "Home Home About Stephen The Computer Stephen", "the University of Cambridge", "Sally Tsui Wong-Avery Director of Research", "Theoretical Physics", "Leiden University", "Baby Universe", "Department of Applied Mathematics", "Cambridge Lectures Publications Books Images Films", "Briefer History of Time", "ESA", "NASA", "Brief History of Time", "CBE", "Caius College", "The Universe"], "PERSON": ["P. Oesch", "Einstein", "D. Magee", "Stephen Hawking", "George", "Annie", "Isaac Newton", "G. Illingworth", "Dennis Stanton Avery", "R. Bouwens"], "LOCATION": ["London", "Santa Cruz", "Einstein", "Cambridge", "Gonville"]}}
```

[scrapy]: https://scrapy.org/
