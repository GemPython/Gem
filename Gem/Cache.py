#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Cache')
def gem():
    if __debug__:
        @export
        def produce_cache_and_insert_function(name):
            cache    = {}
            contains = cache.__contains__
            find     = cache.__getitem__
            provide  = cache.setdefault

            def insert(k, v):
                if contains(k):
                    raise_runtime_error('cache %s: attempt to insert key %r with value %r (already has value %r)',
                                        name, k, v, find(k))

                return provide(k, v)


            return ((
                       cache,
                       insert,
                   ))
    else:
        @export
        def produce_cache_and_insert_function(name):
            cache = {}

            return ((
                       cache,
                       cache.setdefault,
                   ))
