import collections
import datetime
import timeit
import argparse
from turtle import position

import numpy as np

from performance.reference.util import mloc as mloc_ref
from performance.reference.util import immutable_filter as immutable_filter_ref
from performance.reference.util import name_filter as name_filter_ref
from performance.reference.util import shape_filter as shape_filter_ref
from performance.reference.util import column_2d_filter as column_2d_filter_ref
from performance.reference.util import column_1d_filter as column_1d_filter_ref
from performance.reference.util import row_1d_filter as row_1d_filter_ref
from performance.reference.util import resolve_dtype as resolve_dtype_ref
from performance.reference.util import resolve_dtype_iter as resolve_dtype_iter_ref
from performance.reference.util import dtype_from_element as dtype_from_element_ref
from performance.reference.util import array_deepcopy as array_deepcopy_ref
from performance.reference.util import isna_element as isna_element_ref
from performance.reference.util import get_new_indexers_and_screen as get_new_indexers_and_screen_ref

from performance.reference.array_go import ArrayGO as ArrayGOREF

from arraykit import mloc as mloc_ak
from arraykit import immutable_filter as immutable_filter_ak
from arraykit import name_filter as name_filter_ak
from arraykit import shape_filter as shape_filter_ak
from arraykit import column_2d_filter as column_2d_filter_ak
from arraykit import column_1d_filter as column_1d_filter_ak
from arraykit import row_1d_filter as row_1d_filter_ak
from arraykit import resolve_dtype as resolve_dtype_ak
from arraykit import resolve_dtype_iter as resolve_dtype_iter_ak
from arraykit import dtype_from_element as dtype_from_element_ak
from arraykit import array_deepcopy as array_deepcopy_ak
from arraykit import isna_element as isna_element_ak
from arraykit import get_new_indexers_and_screen as get_new_indexers_and_screen_ak

from arraykit import ArrayGO as ArrayGOAK


class Perf:
    FUNCTIONS = ('main',)
    NUMBER = 500_000

#-------------------------------------------------------------------------------
class MLoc(Perf):

    def __init__(self):
        self.array = np.arange(100)

    def main(self):
        self.entry(self.array)

class MLocAK(MLoc):
    entry = staticmethod(mloc_ak)

class MLocREF(MLoc):
    entry = staticmethod(mloc_ref)

#-------------------------------------------------------------------------------
class ImmutableFilter(Perf):

    def __init__(self):
        self.array = np.arange(100)

    def main(self):
        a2 = self.entry(self.array)
        a3 = self.entry(a2)

class ImmutableFilterAK(ImmutableFilter):
    entry = staticmethod(immutable_filter_ak)

class ImmutableFilterREF(ImmutableFilter):
    entry = staticmethod(immutable_filter_ref)

#-------------------------------------------------------------------------------
class NameFilter(Perf):

    def __init__(self):
        self.name1 = ('foo', None, ['bar'])
        self.name2 = 'foo'

    def main(self):
        try:
            self.entry(self.name1)
        except TypeError:
            pass
        self.entry(self.name2)

class NameFilterAK(NameFilter):
    entry = staticmethod(name_filter_ak)

class NameFilterREF(NameFilter):
    entry = staticmethod(name_filter_ref)

#-------------------------------------------------------------------------------
class ShapeFilter(Perf):

    def __init__(self):
        self.array1 = np.arange(100)
        self.array2 = self.array1.reshape(20, 5)

    def main(self):
        self.entry(self.array1)
        self.entry(self.array2)

class ShapeFilterAK(ShapeFilter):
    entry = staticmethod(shape_filter_ak)

class ShapeFilterREF(ShapeFilter):
    entry = staticmethod(shape_filter_ref)

#-------------------------------------------------------------------------------
class Column2DFilter(Perf):

    def __init__(self):
        self.array1 = np.arange(100)
        self.array2 = self.array1.reshape(20, 5)

    def main(self):
        self.entry(self.array1)
        self.entry(self.array2)

class Column2DFilterAK(Column2DFilter):
    entry = staticmethod(column_2d_filter_ak)

class Column2DFilterREF(Column2DFilter):
    entry = staticmethod(column_2d_filter_ref)


#-------------------------------------------------------------------------------
class Column1DFilter(Perf):

    def __init__(self):
        self.array1 = np.arange(100)
        self.array2 = self.array1.reshape(100, 1)

    def main(self):
        self.entry(self.array1)
        self.entry(self.array2)

class Column1DFilterAK(Column1DFilter):
    entry = staticmethod(column_1d_filter_ak)

class Column1DFilterREF(Column1DFilter):
    entry = staticmethod(column_1d_filter_ref)

#-------------------------------------------------------------------------------
class Row1DFilter(Perf):

    def __init__(self):
        self.array1 = np.arange(100)
        self.array2 = self.array1.reshape(1, 100)

    def main(self):
        self.entry(self.array1)
        self.entry(self.array2)

class Row1DFilterAK(Row1DFilter):
    entry = staticmethod(row_1d_filter_ak)

class Row1DFilterREF(Row1DFilter):
    entry = staticmethod(row_1d_filter_ref)


#-------------------------------------------------------------------------------
class ResolveDType(Perf):

    def __init__(self):
        self.dtype1 = np.arange(100).dtype
        self.dtype2 = np.array(('a', 'b')).dtype

    def main(self):
        self.entry(self.dtype1, self.dtype2)

class ResolveDTypeAK(ResolveDType):
    entry = staticmethod(resolve_dtype_ak)

class ResolveDTypeREF(ResolveDType):
    entry = staticmethod(resolve_dtype_ref)


#-------------------------------------------------------------------------------
class ResolveDTypeIter(Perf):

    FUNCTIONS = ('iter10', 'iter100000')
    NUMBER = 1000

    def __init__(self):
        self.dtypes10 = [np.dtype(int)] * 9 + [np.dtype(float)]
        self.dtypes100000 = (
                [np.dtype(int)] * 50000 +
                [np.dtype(float)] * 49999 +
                [np.dtype(bool)]
                )

    def iter10(self):
        self.entry(self.dtypes10)

    def iter100000(self):
        self.entry(self.dtypes100000)

class ResolveDTypeIterAK(ResolveDTypeIter):
    entry = staticmethod(resolve_dtype_iter_ak)

class ResolveDTypeIterREF(ResolveDTypeIter):
    entry = staticmethod(resolve_dtype_iter_ref)


#-------------------------------------------------------------------------------
class ArrayDeepcopy(Perf):
    FUNCTIONS = ('memo_new', 'memo_shared')
    NUMBER = 500

    def __init__(self):
        self.array1 = np.arange(100_000)
        self.array2 = np.full(100_000, None)
        self.array2[0] = [np.nan] # add a mutable
        self.memo = {}

    def memo_new(self):
        memo = {}
        self.entry(self.array1, memo)
        self.entry(self.array2, memo)

    def memo_shared(self):
        self.entry(self.array1, self.memo)
        self.entry(self.array2, self.memo)

class ArrayDeepcopyAK(ArrayDeepcopy):
    entry = staticmethod(array_deepcopy_ak)

class ArrayDeepcopyREF(ArrayDeepcopy):
    entry = staticmethod(array_deepcopy_ref)


#-------------------------------------------------------------------------------
class ArrayGOPerf(Perf):
    NUMBER = 1000

    def __init__(self):
        self.array = np.arange(100).astype(object)

    def main(self):
        ag = self.entry(self.array)
        for i in range(1000):
            ag.append(i)
            if i % 50:
                _ = ag.values

class ArrayGOPerfAK(ArrayGOPerf):
    entry = staticmethod(ArrayGOAK)

class ArrayGOPerfREF(ArrayGOPerf):
    entry = staticmethod(ArrayGOREF)


#-------------------------------------------------------------------------------
class DtypeFromElementPerf(Perf):
    NUMBER = 1000

    def __init__(self):
        NT = collections.namedtuple('NT', tuple('abc'))

        self.values = [
                np.longlong(-1), np.int_(-1), np.intc(-1), np.short(-1), np.byte(-1),
                np.ubyte(1), np.ushort(1), np.uintc(1), np.uint(1), np.ulonglong(1),
                np.half(1.0), np.single(1.0), np.float_(1.0), np.longfloat(1.0),
                np.csingle(1.0j), np.complex_(1.0j), np.clongfloat(1.0j),
                np.bool_(0), np.str_('1'), np.unicode_('1'), np.void(1),
                np.object(), np.datetime64('NaT'), np.timedelta64('NaT'), np.nan,
                12, 12.0, True, None, float('NaN'), object(), (1, 2, 3),
                NT(1, 2, 3), datetime.date(2020, 12, 31), datetime.timedelta(14),
        ]

        # Datetime & Timedelta
        for precision in ['ns', 'us', 'ms', 's', 'm', 'h', 'D', 'M', 'Y']:
            for kind, ctor in (('m', np.timedelta64), ('M', np.datetime64)):
                self.values.append(ctor(12, precision))

        for size in (1, 8, 16, 32, 64, 128, 256, 512):
            self.values.append(bytes(size))
            self.values.append('x' * size)

    def main(self):
        for _ in range(40):
            for val in self.values:
                self.entry(val)

class DtypeFromElementPerfAK(DtypeFromElementPerf):
    entry = staticmethod(dtype_from_element_ak)

class DtypeFromElementPerfREF(DtypeFromElementPerf):
    entry = staticmethod(dtype_from_element_ref)


#-------------------------------------------------------------------------------
class IsNaElementPerf(Perf):
    NUMBER = 1000

    def __init__(self):
        class FloatSubclass(float): pass
        class ComplexSubclass(complex): pass

        self.values = [
                # Na-elements
                np.datetime64('NaT'), np.timedelta64('NaT'), None, float('NaN'), -float('NaN'),

                # Non-float, Non-na elements
                1, 'str', np.datetime64('2020-12-31'), datetime.date(2020, 12, 31), False,
        ]

        nan = np.nan
        complex_nans = [
                complex(nan, 0),
                complex(-nan, 0),
                complex(0, nan),
                complex(0, -nan),
        ]

        float_classes = [float, np.float16, np.float32, np.float64, FloatSubclass]
        if hasattr(np, 'float128'):
            float_classes.append(np.float128)

        cfloat_classes = [complex, np.complex64, np.complex128, ComplexSubclass]
        if hasattr(np, 'complex256'):
            cfloat_classes.append(np.complex256)

        # Append all the different types of nans across dtypes
        for ctor in float_classes:
            self.values.append(ctor(nan))
            self.values.append(ctor(-nan))

        for ctor in cfloat_classes:
            for complex_nan in complex_nans:
                self.values.append(ctor(complex_nan))

        # Append a wide range of float values, with different precision, across types
        for val in (
                1e-1000, 1e-309, 1e-39, 1e-16, 1e-5, 0.1, 0., 1.0, 1e5, 1e16, 1e39, 1e309, 1e1000,
            ):
            for ctor in float_classes:
                self.values.append(ctor(val))
                self.values.append(ctor(-val))

            for ctor in cfloat_classes:
                self.values.append(ctor(complex(val, val)))
                self.values.append(ctor(complex(-val, val)))
                self.values.append(ctor(complex(val, -val)))
                self.values.append(ctor(complex(-val, -val)))

    def main(self):
        for _ in range(10):
            for val in self.values:
                self.entry(val)

class IsNaElementPerfAK(IsNaElementPerf):
    entry = staticmethod(isna_element_ak)

class IsNaElementPerfREF(IsNaElementPerf):
    entry = staticmethod(isna_element_ref)


#-------------------------------------------------------------------------------
class GetNewIndexersAndScreenPerf(Perf):
    NUMBER = 5_000

    def __init__(self):
        NUMBERS = np.arange(500_000)
        POSITIONS = np.arange(500_000)

        np.random.seed(0)

        self.cases = []

        for scale in (5, 50, 500, 5_000, 50_000):
            tiled_ordered = np.tile(NUMBERS[:scale], len(NUMBERS) // scale)
            repeated_ordered = np.repeat(NUMBERS[:scale], len(NUMBERS) // scale)
            tiled_unordered = tiled_ordered.copy()
            repeated_unordered = repeated_ordered.copy()
            np.random.shuffle(tiled_unordered)
            np.random.shuffle(repeated_unordered)

            increment = scale
            while increment < len(NUMBERS):
                self.cases.extend(
                    [
                        (f"tiled_ordered,      {scale}, {increment}", tiled_ordered,      POSITIONS[:increment]),
                        (f"tiled_ordered,      {scale}, {increment}", tiled_ordered,      POSITIONS[:increment]),
                        (f"repeated_ordered,   {scale}, {increment}", repeated_ordered,   POSITIONS[:increment]),
                        (f"tiled_unordered,    {scale}, {increment}", tiled_unordered,    POSITIONS[:increment]),
                        (f"repeated_unordered, {scale}, {increment}", repeated_unordered, POSITIONS[:increment]),
                    ]
                )
                increment *= 10

    def main(self):
        for case, positions in self.cases:
            self.entry(array=case, positions=positions)


class GetNewIndexersAndScreenPerfAK(GetNewIndexersAndScreenPerf):
    entry = staticmethod(get_new_indexers_and_screen_ak)


class GetNewIndexersAndScreenPerfREF(GetNewIndexersAndScreenPerf):
    entry = staticmethod(get_new_indexers_and_screen_ref)


#-------------------------------------------------------------------------------

def get_arg_parser():

    p = argparse.ArgumentParser(
        description='ArrayKit performance tool.',
        )
    p.add_argument("--names",
        nargs='+',
        help='Provide one or more performance tests by name.')
    return p


def main():
    options = get_arg_parser().parse_args()
    match = None if not options.names else set(options.names)

    records = [('cls', 'func', 'ak', 'ref', 'ref/ak')]
    for cls_perf in Perf.__subclasses__(): # only get one level
        cls_map = {}
        if match and cls_perf.__name__ not in match:
            continue
        print(cls_perf)
        for cls_runner in cls_perf.__subclasses__():
            if cls_runner.__name__.endswith('AK'):
                cls_map['ak'] = cls_runner
            elif cls_runner.__name__.endswith('REF'):
                cls_map['ref'] = cls_runner
        for func_attr in cls_perf.FUNCTIONS:
            results = {}
            for key, cls_runner in cls_map.items():
                runner = cls_runner()
                if hasattr(runner, 'pre'): #TEMP, for branches
                    raise RuntimeError('convert your pre() method to __init__()')
                f = getattr(runner, func_attr)
                results[key] = timeit.timeit('f()',
                        globals=locals(),
                        number=cls_runner.NUMBER)
            records.append((cls_perf.__name__, func_attr, results['ak'], results['ref'], results['ref'] / results['ak']))

    width = 24
    for record in records:
        print(''.join(
            (r.ljust(width) if isinstance(r, str) else str(round(r, 8)).ljust(width)) for r in record
            ))

if __name__ == '__main__':
    main()
