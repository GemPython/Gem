#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Topaz.Core')
def gem():
    require_gem('Gem.Exception')
    require_gem('Gem.Map')


    from Gem import raise_runtime_error, raise_value_error, values_tuple_sorted_by_key


    share(
        #
        #   Imported functions
        #
        'raise_runtime_error',          raise_runtime_error,
        'raise_value_error',            raise_value_error,
        'values_tuple_sorted_by_key',   values_tuple_sorted_by_key,
    )
