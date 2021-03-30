import typing as tp

import numpy as np  # type: ignore

_T = tp.TypeVar('_T')

class ArrayGO:

    values: np.array
    def __init__(
        self, iterable: tp.Iterable[object], *, own_iterable: bool = ...
    ) -> None: ...
    def __iter__(self) -> tp.Iterator[tp.Any]: ...
    def __getitem__(self, __key: object) -> tp.Any: ...
    def __len__(self) -> int: ...
    def __getnewargs__(self) -> tp.Tuple[np.ndarray]: ...
    def append(self, __value: object) -> None: ...
    def copy(self: _T) -> _T: ...
    def extend(self, __values: tp.Iterable[object]) -> None: ...

def immutable_filter(__array: np.array) -> np.array: ...
def mloc(__array: np.array) -> int: ...
def name_filter(__name: tp.Hashable) -> tp.Hashable: ...
def shape_filter(__array: np.array) -> np.ndarray: ...
def column_2d_filter(__array: np.array) -> np.ndarray: ...
def column_1d_filter(__array: np.array) -> np.ndarray: ...
def row_1d_filter(__array: np.array) -> np.ndarray: ...
def resolve_dtype(__d1: np.dtype, __d2: np.dtype) -> np.dtype: ...
def resolve_dtype_iter(__dtypes: tp.Iterable[np.dtype]) -> np.dtype: ...
def roll_1d(__array: np.ndarray, __shift: int) -> np.ndarray: ...
def roll_2d(__array: np.ndarray, __shift: int, __axis: int) -> np.ndarray: ...
