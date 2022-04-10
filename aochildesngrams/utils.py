from cytoolz import itertoolz


def human_format(num, pos):  # pos is required
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format(num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def get_sliding_windows(window_size, tokens):
    res = list(itertoolz.sliding_window(window_size, tokens))
    return res

