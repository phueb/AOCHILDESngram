import random
from typing import List
from functools import reduce
from operator import iconcat

from childesngrams import configs


def load_tokens(corpus_name: str,
                shuffle_docs: bool = False,
                shuffle_seed: int = 20,
                ) -> List[str]:

    """
    A "document" has type string. It is not tokenized.

    WARNING:
    Always use a seed for random operations.
    For example when loading tags and words using this function twice, they won't align if no seed is set

    WARNING:
    shuffling the documents does not remove all age-structure,
    because utterances associated with teh same age are still clustered within documents.
    """

    p = configs.Dirs.corpora / f'{corpus_name}.txt'
    text_in_file = p.read_text()

    docs = text_in_file.split('\n')

    num_docs = len(docs)
    print(f'Loaded {num_docs} documents from {corpus_name}')

    if shuffle_docs:
        random.seed(shuffle_seed)
        print('Shuffling documents')
        random.shuffle(docs)

    tokenized_docs = [d.split() for d in docs]
    res = reduce(iconcat, tokenized_docs, [])  # flatten list of lists

    return res
