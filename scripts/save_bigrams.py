from collections import Counter
import attr
import numpy as np
from functools import reduce
from operator import iconcat

from preppy import PartitionedPrep as TrainPrep

from childesngrams import configs
from childesngrams.params import PrepParams
from childesngrams.io import load_tokens
from childesngrams.utils import get_sliding_windows

# /////////////////////////////////////////////////////////////////

CORPUS_NAME = 'childes-20191206'

docs = load_docs(CORPUS_NAME)

params = PrepParams()
prep = TrainPrep(docs, **attr.asdict(params))

# /////////////////////////////////////////////////////////////////

# use all tokens in text file instead of tokens which are pruned
tokenized_docs = [d.split() for d in docs]
tokens = reduce(iconcat, tokenized_docs, [])

ngram2f = Counter(get_sliding_windows(2, tokens))
unique_fs, counts = np.unique([v for v in ngram2f.values()], return_counts=True)
num_total = counts.sum()
print(len(unique_fs), len(counts), num_total)

print(unique_fs)
p = configs.Dirs.root / 'bi-grams.txt'
with p.open('w') as f:
    for ng, freq in sorted(ngram2f.items(), key=lambda i: i[1], reverse=True):

        idx = np.where(unique_fs <= freq)[0]
        num_words_less_frequent = counts[idx].sum()
        percentile = num_words_less_frequent / num_total * 100

        f.write(f'{freq} {ng[0]} {ng[1]} {percentile}\n')
