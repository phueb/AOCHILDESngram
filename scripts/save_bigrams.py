from collections import Counter
import numpy as np

from aochildes.dataset import AOChildesDataSet

from aochildesngrams import configs
from aochildesngrams.utils import get_sliding_windows


tokens = AOChildesDataSet().load_tokens()

ngram2f = Counter(get_sliding_windows(2, tokens))
unique_fs, counts = np.unique([v for v in ngram2f.values()], return_counts=True)
num_total = counts.sum()
print(len(unique_fs), len(counts), num_total)

print(unique_fs)
p = configs.Dirs.bi_grams / 'bi-grams.txt'
with p.open('w') as f:
    for ng, freq in sorted(ngram2f.items(), key=lambda i: i[1], reverse=True):

        idx = np.where(unique_fs <= freq)[0]
        num_words_less_frequent = counts[idx].sum()
        percentile = num_words_less_frequent / num_total * 100

        f.write(f'{freq} {ng[0]} {ng[1]} {percentile}\n')
