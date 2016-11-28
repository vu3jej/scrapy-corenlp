from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from lxml.html.clean import Cleaner
from nltk.tokenize import StanfordTokenizer
from nltk.tag.stanford import StanfordNERTagger

from scrapy import Item
from scrapy.exceptions import NotConfigured


class CoreNLP(object):

    def __init__(self, classifier, jar_file, output_field):
        self.classifier = classifier
        self.jar_file = jar_file
        self.output_field = output_field
        self.tokenizer = StanfordTokenizer(path_to_jar=self.jar_file).tokenize

    @classmethod
    def from_crawler(cls, crawler):
        if (not crawler.settings.get('STANFORD_NER_ENABLED') or
                not crawler.settings.get('STANFORD_NER_CLASSIFIER') or
                not crawler.settings.get('STANFORD_NER_JAR') or
                not crawler.settings.get('STANFORD_NER_FIELD_OUTPUT')):
            raise NotConfigured

        classifier = crawler.settings.get('STANFORD_NER_CLASSIFIER')
        jar_file = crawler.settings.get('STANFORD_NER_JAR')
        output_field = crawler.settings.get('STANFORD_NER_FIELD_OUTPUT')

        corenlp_settings = cls(classifier, jar_file, output_field)

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
        tagger = StanfordNERTagger(model_filename=self.classifier,
                                   path_to_jar=self.jar_file)
        token_entity_pairs = tagger.tag(tokens=self.tokenizer(s=cleaned_text))
        entities = self.accumulate(token_entity_pairs)

        for element in result:
            if isinstance(element, (Item, dict)):
                element.setdefault(self.output_field, entities)
            yield element
