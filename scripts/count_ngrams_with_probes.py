"""
Count the number of n-grams that contains a probe word in the first and second half of the corpus.
"""
from tabulate import tabulate

from aochildes.dataset import AOChildesDataSet

from aochildesngrams.utils import get_sliding_windows


PROBES = ['cat', 'dog']
NGRAM_SIZES = [1, 2, 3, 4, 5, 6, 7]

tokens = AOChildesDataSet().load_tokens()
tokens1 = tokens[:len(tokens) // 2]
tokens2 = tokens[-len(tokens) // 2:]

probes_in_tokens1 = [token for token in tokens1 if token in PROBES]
probes_in_tokens2 = [token for token in tokens2 if token in PROBES]

rows = []
for ngram_size in NGRAM_SIZES:
    print(ngram_size)

    ngrams1 = get_sliding_windows(ngram_size, tokens1)
    ngrams2 = get_sliding_windows(ngram_size, tokens2)
    num_ngrams1 = len(ngrams1)
    num_ngrams2 = len(ngrams2)

    unique_probe_ngrams1 = set([ngram for ngram in ngrams1 if any([t in PROBES for t in ngram])])
    unique_probe_ngrams2 = set([ngram for ngram in ngrams2 if any([t in PROBES for t in ngram])])
    ngram_probes_set_len1 = len(unique_probe_ngrams1)
    ngram_probes_set_len2 = len(unique_probe_ngrams2)
    probes_set_len1 = len(set(probes_in_tokens1))
    probes_set_len2 = len(set(probes_in_tokens2))
    ngram_set_len_by_probe_set_len1 = ngram_probes_set_len1 / probes_set_len2
    ngram_set_len_by_probe_set_len2 = ngram_probes_set_len2 / probes_set_len1
    rows.append((f'{ngram_size}-gram types with probes / Probe Types',
                 ngram_set_len_by_probe_set_len1, ngram_set_len_by_probe_set_len2))

    num_total_probes1 = len(probes_in_tokens1)
    num_total_probes2 = len(probes_in_tokens2)
    num_ngrams_by_probe_count1 = num_ngrams1 / num_total_probes1
    num_ngrams_by_probe_count2 = num_ngrams2 / num_total_probes2
    rows.append((f'{ngram_size}-gram tokens with probes / Probe Tokens',
                 num_ngrams_by_probe_count1, num_ngrams_by_probe_count2))

# print table
headers = ['Percentage Type', 'partition 1', 'partition 2']
print(tabulate(rows,
               headers=headers,
               tablefmt='simple'))