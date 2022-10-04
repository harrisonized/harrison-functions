import collections

# Functions
# # build_nested_dict
# # merge_dict_with_subdicts


def build_nested_dict(keys: list, val):
    """
    | Iterative solution to building a nested dictionary from inside out
    | See: https://stackoverflow.com/questions/40401886/how-to-create-a-nested-dictionary-from-a-list-in-python
    
    .. code-block:: python
    
       >>> build_nested_dict(['grandparents', 'parents'], 'children')
       {'grandparents': {'parents': 'children'}}
       
    """
    nested_dict = {}
    nested_dict[keys[-1]] = val
    for key in reversed(keys[0:-1]):
        nested_dict = {key: nested_dict}

    return nested_dict


def merge_dict_with_subdicts(main_dict: dict, sub_dict: dict) -> dict:
    """
    | Merge two nested dictionaries
    | See: https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries
    """
    queue = collections.deque([(main_dict, sub_dict)])

    while len(queue) > 0:
        d1, d2 = queue.pop()
        for key, val in d2.items():
            if key in d1 and isinstance(d1[key], dict) and isinstance(val, dict):
                queue.append((d1[key], val))
            else:
                d1[key] = val

    return main_dict
