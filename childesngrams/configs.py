from pathlib import Path


class Dirs:
    root = Path(__file__).parent.parent
    src = Path(__file__).parent
    corpora = root / 'corpora'
    output = root / 'output'


class Fig:
    ax_fontsize = 20
    leg_fontsize = 12
    dpi = 163
    fig_size = (6, 6)
