from arraykit import array_to_duplicated_hashable
import numpy as np

class PO:
    def __init__(self, v) -> None:
        self.v = v
    def __repr__(self) -> str:
        return f'PO<{self.v}>'

def iterate_1d(array, axis, reverse, is_dupe, process_value_func, set_obj, dict_obj):
    if reverse:
        iterator = reversed(array)
    else:
        iterator = array

    size = len(array)

    for i, value in enumerate(iterator):
        if reverse:
            i = size - i - 1

        process_value_func(i, value, is_dupe, set_obj, dict_obj)


def iterate_2d(array, axis, reverse, is_dupe, process_value_func, set_obj, dict_obj):
    size = array.shape[axis]

    if axis == 0:
        iterator = array
    else:
        iterator = array.T

    if reverse:
        iterator = reversed(iterator)

    for i, value in enumerate(map(tuple, iterator)):
        if reverse:
            i = size - i - 1

        process_value_func(i, value, is_dupe, set_obj, dict_obj)


def handle_value_one_boundary(i, value, is_dupe, set_obj, dict_obj):
    seen = set_obj
    assert dict_obj == None

    if value not in seen:
        seen.add(value)
    else:
        is_dupe[i] = True


def handle_value_exclude_boundaries(i, value, is_dupe, set_obj, dict_obj):
    duplicates = set_obj
    first_unique_locations = dict_obj

    if value not in first_unique_locations:
        first_unique_locations[value] = i
    else:
        is_dupe[i] = True

        # Second time seeing a duplicate
        if value not in duplicates:
            is_dupe[first_unique_locations[value]] = True

        # always update last
        duplicates.add(value)


def handle_value_include_boundaries(i, value, is_dupe, set_obj, dict_obj):
    seen = set_obj
    last_duplicate_locations = dict_obj

    if value not in seen:
        seen.add(value)
    else:
        is_dupe[i] = True

        # always update last
        last_duplicate_locations[value] = i


def new(
        array: np.ndarray,
        axis: int = 0,
        exclude_first: bool = False,
        exclude_last: bool = False,
    ) -> np.ndarray:
    '''
    Algorithm for finding duplicates in unsortable arrays for hashables. This will always be an object array.

    Note:
        np.unique fails under the same conditions that sorting fails, so there is no need to try np.unique: must go to set drectly.
    '''
    size = array.shape[axis]

    reverse = not exclude_first and exclude_last

    if array.ndim == 1:
        iterate_func = iterate_1d
    else:
        iterate_func = iterate_2d

    is_dupe = np.full(size, False)

    set_obj = set()
    if exclude_first ^ exclude_last:
        dict_obj = None
        process_value_func = handle_value_one_boundary

    elif not exclude_first and not exclude_last:
        dict_obj = dict()
        process_value_func = handle_value_exclude_boundaries

    else:
        dict_obj = dict()
        process_value_func = handle_value_include_boundaries

    iterate_func(array, axis, reverse, is_dupe, process_value_func, set_obj, dict_obj)

    if exclude_first and exclude_last:
        is_dupe[list(dict_obj.values())] = False

    return is_dupe


def test(*args, **kwargs):
    assert (new(*args, **kwargs) == array_to_duplicated_hashable(*args, **kwargs)).all(), (args, kwargs)


arr = np.array([1, PO(1), 2, 3, 1, PO(1), 2, 3, 2, -1, -233, 'aslkj', 'df', 'df', True, True, None, 1])
#array_to_duplicated_hashable(np.arange(5))
#array_to_duplicated_hashable(np.arange(5), 213)
#array_to_duplicated_hashable(np.arange(5), 1)
#array_to_duplicated_hashable(np.arange(5), 1, True)
#array_to_duplicated_hashable(np.arange(5), 1, 123)
#array_to_duplicated_hashable(np.arange(5), 1, True)

if False:
    test(arr, 0, True, False)
    test(arr, 0, False, False)
    test(arr, 0, False, True)
    test(arr, 0, True, True)


array_to_duplicated_hashable(np.arange(20).reshape(4, 5).astype(object), 0)
print()
array_to_duplicated_hashable(np.arange(20).reshape(4, 5).astype(object), 1)
print()
print()


array_to_duplicated_hashable(np.arange(20).reshape(4, 5).astype(object).T, 0)
print()
array_to_duplicated_hashable(np.arange(20).reshape(4, 5).astype(object).T, 1)
print()


print('Done')
