from re import sub


def is_content_equals(expected, actual):
    return sub('\s+', '', expected) == sub('\s+', '', actual)
