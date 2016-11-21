# scrapy-corenlp

A [Scrapy][scrapy] middleware to perform Named Entity Recognition (NER) on response with Stanford CoreNLP.

## Settings
| Option Name     | Value                                                                                                            | Example Value                                                                |
|-----------------|------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| `CORENLP_ENABLED` | Boolean                                                                                                          | `TRUE`                                                                         |
| `NER_CLASSIFIER`  | Classifier to use                                                                                                | `'./stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz'` |
| `NER_JAR`         | JAR file to use                                                                                                  | `'./scrapy-ner/stanford-ner-2015-12-09/stanford-ner.jar'`                       |
| `NER_FIELD`       | The field where the NER output will be stored                                                                    | `'entities'`                                                                    |
| `PTB_TOKENIZER`   | Boolean (PTBTokenizer location must be set in the `CLASSPATH` environment variable. Defaults to `nltk.tokenize.word_tokenize` if not set.) | `TRUE`                                                                         |

In your `settings.py` file, add the previously described settings and add `CoreNLP` to your `SPIDER_MIDDLEWARES`, e.g.

```python
SPIDER_MIDDLEWARES = {
    'scrapy_corenlp.middlewares.CoreNLP': 543,
}
```

[scrapy]: https://scrapy.org/
