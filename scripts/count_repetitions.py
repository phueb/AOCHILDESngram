"""
Research question:
1. Are n-grams in partition 1 of AO-CHILDES repeated more often on average compared to partition 2?
"""

from tabulate import tabulate

from aochildes.dataset import AOChildesDataSet

from aochildesngrams.utils import get_sliding_windows


NGRAM_SIZES = [1, 2, 3, 4, 5, 6, 7]

tokens = AOChildesDataSet().load_tokens()
tokens1 = tokens[:len(tokens) // 2]
tokens2 = tokens[-len(tokens) // 2:]

rows = []
for ngram_size in NGRAM_SIZES:
    ngrams1 = get_sliding_windows(ngram_size, tokens1)
    ngrams2 = get_sliding_windows(ngram_size, tokens2)
    num_ngrams1 = len(ngrams1)
    num_ngrams2 = len(ngrams2)

    unique_ngrams1 = set(ngrams1)
    unique_ngrams2 = set(ngrams2)
    ngram_set_len1 = len(unique_ngrams1)
    ngram_set_len2 = len(unique_ngrams2)

    y1 = (ngram_set_len1 + num_ngrams1) / ngram_set_len1
    y2 = (ngram_set_len2 + num_ngrams2) / ngram_set_len2
    rows.append((ngram_size, y1, y2))

# print table
headers = ['N-gram size', 'partition 1', 'partition 2']
print(tabulate(rows,
               headers=headers,
               floatfmt='.2f'))