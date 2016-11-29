from collections import defaultdict
from itertools import groupby
from operator import itemgetter
from nltk.tokenize import StanfordTokenizer
from nltk.tag.stanford import StanfordNERTagger
from six import string_types

from scrapy import Item
from scrapy.exceptions import NotConfigured


class CoreNLP(object):

    def __init__(self, classifier, jar_file, field_to_process, output_field):
        self.classifier = classifier
        self.jar_file = jar_file
        self.field_to_process = field_to_process
        self.output_field = output_field
        self.tokenizer = StanfordTokenizer(path_to_jar=self.jar_file).tokenize

    @classmethod
    def from_crawler(cls, crawler):
        if (not crawler.settings.get('STANFORD_NER_ENABLED') or
                not crawler.settings.get('STANFORD_NER_CLASSIFIER') or
                not crawler.settings.get('STANFORD_NER_JAR') or
                not crawler.settings.get('STANFORD_NER_FIELD_TO_PROCESS') or
                not crawler.settings.get('STANFORD_NER_FIELD_OUTPUT')):
            raise NotConfigured

        classifier = crawler.settings.get('STANFORD_NER_CLASSIFIER')
        jar_file = crawler.settings.get('STANFORD_NER_JAR')
        field_to_process = crawler.settings.get('STANFORD_NER_FIELD_TO_PROCESS')
        output_field = crawler.settings.get('STANFORD_NER_FIELD_OUTPUT')

        corenlp_settings = cls(classifier, jar_file, field_to_process,
                               output_field)

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
                    ' '.join(tokens[index] for index in indices)
                )
        recognised.pop('O', None)

        return dict(recognised)

    def process_spider_output(self, response, result, spider):
        for element in result:
            if isinstance(element, (Item, dict)):
                if isinstance(self.field_to_process, list):
                    text = ' '.join(
                        [element[field] for field in self.field_to_process]
                    )
                elif isinstance(self.field_to_process, string_types):
                    text = element[self.field_to_process]
                else:
                    yield element

                tagger = StanfordNERTagger(
                    model_filename=self.classifier,
                    path_to_jar=self.jar_file
                )
                token_entity_pairs = tagger.tag(
                    tokens=self.tokenizer(s=text)
                )
                accumulated = self.accumulate(token_entity_pairs)
                element.setdefault(self.output_field, accumulated)
                yield element
            else:
                yield element
