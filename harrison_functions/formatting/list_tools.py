import itertools


# Functions included in this file:
# # move_list_item_to_end
# # pairwise
# # renumerate
# # peek


def move_list_item_to_end(input_list: list, item):
    """Example usage:
    move_list_item_to_end([1, 2, 3, 4, 5], 3)
    [1, 2, 4, 5, 3]
    """
    output_list = input_list + [input_list.pop(input_list.index(item))]
    return output_list


def pairwise(iterable):
    """See: https://docs.python.org/3/library/itertools.html#recipes
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = itertools.tee(iterable)
    next(b, None)
    return list(zip(a, b))


def renumerate(sequence):
    """reverse enumerate"""
    n = len(sequence)-1
    for elem in sequence:
        yield n, elem
        n -= 1


def peek(stack): 
    if stack:
        return stack[-1] 
    return None
