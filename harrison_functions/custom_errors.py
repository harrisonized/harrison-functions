# Objects:
# # EmptyListError
# # ItemNotFoundError
# # MethodNotFoundError


class EmptyListError(KeyError):
    pass


class ItemNotFoundError(KeyError):
    pass


class MethodNotFoundError(KeyError):
    pass
