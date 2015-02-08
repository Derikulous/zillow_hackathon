################################################################################
# Collection utils
################################################################################

def first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return default
