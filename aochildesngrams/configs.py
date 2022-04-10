from pathlib import Path


class Dirs:
    root = Path(__file__).parent.parent
    src = Path(__file__).parent
    corpora = root / 'corpora'
    bi_grams = root / 'bi_grams'
    tmp = root / 'tmp'


class Fig:
    ax_fontsize = 18
    leg_fontsize = 12
    dpi = 200
    fig_size = (6, 6)
