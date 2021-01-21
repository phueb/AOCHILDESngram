from cytoolz import itertoolz




def get_sliding_windows(window_size, tokens):
    res = list(itertoolz.sliding_window(window_size, tokens))
    return res

