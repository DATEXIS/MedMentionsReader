import os
import re
import logging
from enum import Enum
from typing import List

from tqdm import tqdm

logger = logging.getLogger(__name__)
logging.basicConfig(level='INFO')  # TODO remove me


class Annotation:
    def __init__(self, tokens):
        self.begin = int(tokens[1])
        self.end = int(tokens[2])
        self.text = tokens[3]
        self.semantic_type = tokens[4]
        self.umls_id = tokens[5]

    def get_begin(self):
        return self.begin

    def get_end(self):
        return self.end

    def get_text(self):
        return self.text

    def get_semantic_type(self):
        return self.semantic_type

    def get_umls_id(self):
        return self.umls_id


class Document:
    def __init__(self, id):
        self.id = id
        self.annotations = []
        self.title = None
        self.abstract = None

    def set_title(self, title: str):
        self.title = title

    def set_abstract(self, abstract: str):
        self.abstract = abstract

    def add_annotation(self, annotation: Annotation):
        self.annotations.append(annotation)

    def get_annotations(self) -> List[Annotation]:
        return self.annotations

    def get_text(self) -> str:
        """
        Get a concatenation of MedMentions title and abstract that is compatible with all of the annotation offsets.
        :return: Fulltext of the MedMentions document.
        """
        return self.title + self.abstract

    def __eq__(self, other):
        return self.id == other.id


class MedMentionsReader:

    def __init__(self, path):
        """
        Initializes the reader and starts the parsing.
        :param path: Path to MedMentions data files (most likely ../MedMentions/full/data)
        """
        logger.info("Initialising MedMentionsReader for path {}".format(path))
        self.path = path
        self.documents_all = {}
        self.documents_train = {}
        self.documents_test = {}
        self.documents_dev = {}
        self.__parse_dataset__()
        self.__parse_datasplits__()

    def __parse_dataset__(self):
        logger.info('Parsing corpus_pubtator...')
        with open(os.path.join(self.path, 'corpus_pubtator.txt'), 'r') as f:
            for line in tqdm(f, desc="Parsing corpus_pubtator.txt"):
                line_type = get_line_type(line)
                if line_type == LineType.DOCSEP:
                    continue
                pmid = line[0:8]
                if len(str(pmid)) != 8:
                    raise ValueError('Unexpected length of PMID {}'.format(pmid))
                if pmid not in self.documents_all.keys():
                    self.documents_all[pmid] = Document(pmid)
                document = self.documents_all[pmid]
                if line_type == LineType.TITLE:
                    document.title = line[11:]
                if line_type == LineType.ABSTRACT:
                    document.abstract = line[11:]
                if line_type == LineType.MENTION:
                    tokens = re.split('[\t\n|]', line)[:-1]
                    document.add_annotation(Annotation(tokens))

    def __parse_datasplits__(self):
        logger.info('Parsing datasplit files...')

        def lines2list_of_ids(f):
            return [id.strip() for id in f.readlines() if len(id.strip()) > 0]

        with open(os.path.join(self.path, 'corpus_pubtator_pmids_trng.txt'), 'r') as f_train:
            for pmid in lines2list_of_ids(f_train):
                self.documents_train[pmid] = self.documents_all.get(pmid)
            logger.info("Found {} ids for train set.".format(len(self.documents_train.keys())))
        with open(os.path.join(self.path, 'corpus_pubtator_pmids_test.txt'), 'r') as f_test:
            for pmid in lines2list_of_ids(f_test):
                self.documents_test[pmid] = self.documents_all.get(pmid)
            logger.info("Found {} ids for test set.".format(len(self.documents_test.keys())))
        with open(os.path.join(self.path, 'corpus_pubtator_pmids_dev.txt'), 'r') as f_dev:
            for pmid in lines2list_of_ids(f_dev):
                self.documents_dev[pmid] = self.documents_all.get(pmid)
            logger.info("Found {} ids for dev set.".format(len(self.documents_dev.keys())))

    def get_all(self) -> dict:
        return self.documents_all

    def get_train(self) -> dict:
        return self.documents_train

    def get_test(self) -> dict:
        return self.documents_test

    def get_dev(self) -> dict:
        return self.documents_dev

    def get_document_by_id(self, pmid) -> Document:
        return self.documents_all.get(pmid, None)


class LineType(Enum):
    TITLE = 1
    ABSTRACT = 2
    MENTION = 3
    DOCSEP = 4


def get_line_type(line: str) -> LineType:
    tokens = re.split('[\t\n|]', line)[:-1]  # remove trailing newline
    if tokens[0] == '' and len(tokens) == 1:
        return LineType.DOCSEP
    if tokens[1] == 'a':
        return LineType.ABSTRACT
    if tokens[1] == 't':
        return LineType.TITLE
    if len(tokens) == 6:
        return LineType.MENTION
    raise Exception('Unexpected line type in dataset.')
