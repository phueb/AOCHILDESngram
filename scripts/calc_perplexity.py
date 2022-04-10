import kenlm
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt
import numpy as np
import tempfile

from aochildes.dataset import AOChildesDataSet

from aochildesngrams import configs


NGRAM_SIZES = [2, 3]  # must be 2, 3, 4, 5, or 6

# these binaries must be installed by user
LMPLZ_PATH = '/home/ph/kenlm/bin/lmplz'
BINARIZE_PATH = '/home/ph/kenlm/bin/build_binary'

tokens = AOChildesDataSet().load_tokens()
tokens1 = tokens[:len(tokens) // 2]
tokens2 = tokens[-len(tokens) // 2:]


def calc_pps(str1, str2):
    if not configs.Dirs.tmp.exists():
        configs.Dirs.tmp.mkdir()

    result = []
    for s1, s2 in [(str1, str1),  # we train and eval on the same string (first half of corpus)
                   (str2, str2),  # we train and eval on the same string (second half of corpus)
                   ]:

        # train n-gram model
        with tempfile.TemporaryFile('w') as fp:
            fp.write(s1)
            train_process = Popen([LMPLZ_PATH, '-o', str(ngram_size)], stdin=fp, stdout=PIPE)

        # save model
        out_path = configs.Dirs.tmp / f'aochildes_{ngram_size}-grams.arpa'
        if not out_path.exists():
            out_path.touch()
        arpa_file_bytes = train_process.stdout.read()
        assert arpa_file_bytes  # this may be empty if train_process runs out of memory
        out_path.write_text(arpa_file_bytes.decode())

        # binarize model
        klm_file_path = str(out_path).rstrip('arpa') + 'klm'
        binarize_process = Popen([BINARIZE_PATH, str(out_path), klm_file_path])
        binarize_process.wait()

        # load model
        print('Computing perplexity using {}-gram model...'.format(ngram_size))
        model = kenlm.Model(klm_file_path)

        # score
        pp = model.perplexity(s2)
        result.append(pp)
    print(result)
    return result


xys = []
for ngram_size in NGRAM_SIZES:
    y = calc_pps(' '.join(tokens1), ' '.join(tokens2))
    xys.append((y, ngram_size))

# fig
bar_width = 0.35
fig, ax = plt.subplots(dpi=configs.Fig.dpi)
ax.set_title('')
ax.set_ylabel('Perplexity', fontsize=configs.Fig.ax_fontsize)
ax.set_xlabel('N-gram size', fontsize=configs.Fig.ax_fontsize)
# ax.set_ylim([0, 30])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.tick_params(axis='both', which='both', top=False, right=False)
ax.set_xticks(np.array(NGRAM_SIZES) + bar_width / 2)
ax.set_xticklabels(NGRAM_SIZES, fontsize=configs.Fig.ax_fontsize)
# plot
for n, (y, ngram_size) in enumerate(xys):
    x = np.array([ngram_size, ngram_size + bar_width])
    for x_single, y_single, c, label in zip(x, y, ['C0', 'C1'], ['partition 1', 'partition 2']):
        label = label if n == 0 else '_nolegend_'  # label only once
        ax.bar(x_single, y_single, bar_width, color=c, label=label)
plt.legend(loc='best', frameon=False, fontsize=configs.Fig.leg_fontsize)
plt.tight_layout()
fig.show()
