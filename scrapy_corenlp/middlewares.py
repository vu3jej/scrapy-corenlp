import os
import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from lxml.html.clean import Cleaner
from nltk.tokenize import StanfordTokenizer, word_tokenize
from nltk.tag.stanford import StanfordNERTagger

from scrapy import Item
from scrapy.exceptions import NotConfigured


class CoreNLP(object):

    def __init__(self, ner_classifier, ner_jar, ner_field, ptb_tokenizer):
        self.ner_classifier = ner_classifier
        self.ner_jar = ner_jar
        self.ner_field = ner_field
        if ptb_tokenizer and os.getenv('CLASSPATH') is not None:
            self.tokenizer = StanfordTokenizer().tokenize
        else:
            self.tokenizer = word_tokenize

    @classmethod
    def from_crawler(cls, crawler):
        if (not crawler.settings.get('CORENLP_ENABLED') or
                not crawler.settings.get('NER_CLASSIFIER') or
                not crawler.settings.get('NER_JAR') or
                not crawler.settings.get('NER_FIELD')):
            raise NotConfigured

        ner_classifier = crawler.settings.get('NER_CLASSIFIER')
        ner_jar = crawler.settings.get('NER_JAR')
        ner_field = crawler.settings.get('NER_FIELD')
        ptb_tokenizer = crawler.settings.get('PTB_TOKENIZER')

        corenlp_settings = cls(ner_classifier, ner_jar, ner_field,
                               ptb_tokenizer)

        return corenlp_settings

    @staticmethod
    def accumulate(list_of_tuples):
        tokens, entities = zip(*list_of_tuples)
        recognised = defaultdict(set)
        duplicates = defaultdict(list)

        for i, item in enumerate(entities):
            duplicates[item].append(i)

        for key, value in duplicates.items():
            for k, g in groupby(enumerate(value), lambda x: x[0] - x[1]):
                indices = list(map(itemgetter(1), g))
                recognised[key].add(
                    ' '.join(tokens[index] for index in indices))
        recognised.pop('O')

        return dict(recognised)

    def process_spider_output(self, response, result, spider):
        cleaner = Cleaner(style=True, remove_unknown_tags=False,
                          allow_tags=str(None))
        cleaned_text = cleaner.clean_html(html=response.text)
        cleaned_text = re.sub(pattern=r'\s+', repl=r' ', string=cleaned_text)
        tagger = StanfordNERTagger(self.ner_classifier, self.ner_jar)
        token_entity_pairs = tagger.tag(self.tokenizer(cleaned_text))
        entities = self.accumulate(token_entity_pairs)

        for element in result:
            if isinstance(element, (Item, dict)):
                element.setdefault(self.ner_field, entities)
            yield element
