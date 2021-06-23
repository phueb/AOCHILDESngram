"""
Count the number of n-gram types and tokens in the first and second half of the corpus.
"""
from tabulate import tabulate

from childesngrams.io import load_tokens
from childesngrams.utils import get_sliding_windows


CORPUS_NAME = 'childes-20201026'
NGRAM_SIZES = [1, 2, 3]

tokens = load_tokens(CORPUS_NAME)
tokens1 = tokens[:len(tokens) // 2]
tokens2 = tokens[-len(tokens) // 2:]

rows = []
for ngram_size in NGRAM_SIZES:
    ngrams1 = get_sliding_windows(ngram_size, tokens1)
    ngrams2 = get_sliding_windows(ngram_size, tokens2)
    num_ngrams1 = len(ngrams1)
    num_ngrams2 = len(ngrams2)
    rows.append((f'{ngram_size}-gram Tokens', num_ngrams1, num_ngrams2))

    unique_ngrams1 = set(ngrams1)
    unique_ngrams2 = set(ngrams2)
    ngram_set_len1 = len(unique_ngrams1)
    ngram_set_len2 = len(unique_ngrams2)
    rows.append((f'{ngram_size}-gram Types', ngram_set_len1, ngram_set_len2))

    print('num n-grams in 1 also in 2:')
    print(len([ngram for ngram in unique_ngrams1 if ngram in unique_ngrams2]))
    print()

# print table
headers = ['Count Type', 'partition 1', 'partition 2']
print(tabulate(rows,
               headers=headers,
               tablefmt='simple'))