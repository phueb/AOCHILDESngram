"""
Plot number of seen and novel n-grams.
"""
import numpy as np
import pyprind
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from aochildes.dataset import AOChildesDataSet

from aochildesngrams import configs
from aochildesngrams.utils import human_format
from aochildesngrams.utils import get_sliding_windows


NUM_BINS = 32
NGRAM_SIZES = [2, 3]

tokens = AOChildesDataSet().load_tokens()


def make_novel_xys(n_grams):
    """
    Return a list of (x, y) coordinates for plotting
    """
    # trajectories
    seen = set()
    num_ngrams = len(n_grams)
    pbar = pyprind.ProgBar(num_ngrams, stream=2, title='Tracking seen and novel n-grams')
    trajectory = []
    for ng in n_grams:
        if ng not in seen:
            trajectory.append(1)
            seen.add(ng)
        else:
            trajectory.append(np.nan)
        pbar.update()
    # res
    ns = np.where(np.array(trajectory) == 1)[0]
    hist, b = np.histogram(ns, bins=NUM_BINS, range=[0, num_ngrams])
    res = (b[:-1], hist)
    return res


# size2novel_xys
num_ngram_sizes = len(NGRAM_SIZES)
size2novel_xys1 = {}
size2novel_xys2 = {}
for ngram_size in NGRAM_SIZES:
    ngram_range = (ngram_size, ngram_size)
    ngrams = get_sliding_windows(ngram_size, tokens)
    xys1 = make_novel_xys(ngrams)
    xys2 = make_novel_xys(ngrams[::-1])
    size2novel_xys1[ngram_size] = xys1
    size2novel_xys2[ngram_size] = xys2

# fig
fig, axs = plt.subplots(num_ngram_sizes, 1, sharex='all', dpi=configs.Fig.dpi, figsize=None)
if num_ngram_sizes == 1:
    axs = [axs]
for ax, ngram_size in zip(axs, NGRAM_SIZES):
    if ax == axs[-1]:
        ax.tick_params(axis='both', which='both', top=False, right=False)
        ax.set_ylabel('Corpus Location', fontsize=configs.Fig.ax_fontsize)
    else:
        ax.tick_params(axis='both', which='both', top=False, right=False, bottom='off')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_major_formatter(FuncFormatter(human_format))
    ax.set_ylabel('Novel {}-grams'.format(ngram_size), fontsize=configs.Fig.ax_fontsize)
    # ax.yaxis.grid(True)
    # plot
    ax.plot(*size2novel_xys1[ngram_size], linestyle='-', label='age-ordered')
    ax.plot(*size2novel_xys2[ngram_size], linestyle='-', label='reverse age-ordered')
plt.legend(loc='best', frameon=False, fontsize=configs.Fig.leg_fontsize)
plt.tight_layout()
plt.show()


