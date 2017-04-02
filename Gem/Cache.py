#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Cache')
def gem():
    @export
    def produce_cache_functions(
            name,
            produce_cache   = false,
            produce_conjure = false,
            produce_find    = false,
            produce_insert  = false,
            produce_lookup  = false,
    ):
        result = []
        append = result.append

        cache = {}

        if (produce_conjure) or (produce_insert):
            provide = cache.setdefault

        if (produce_conjure) or (produce_lookup):
            lookup = cache.get

        if (produce_find) or (produce_insert):
            find = cache.__getitem__

        if produce_cache:
            append(cache)

        if produce_conjure:
            def conjure(k, meta):
                return (lookup(k)) or (provide(k, meta(k)))


            append(conjure)

        if produce_find:
            append(find)

        if produce_insert:
            contains = cache.__contains__


            if __debug__:
                def insert(k, v):
                    if contains(k):
                        raise_runtime_error('cache %s: attempt to insert key %r with value %r (already has value %r)',
                                            name, k, v, find(k))

                    return provide(k, v)


                append(insert)
            else:
                append(provide)

        if produce_lookup:
            append(lookup)

        return Tuple(result)
