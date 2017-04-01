#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Name')
def gem():
    class TremoliteMatch(Object):
        __slots__ = ((
            'name',                     #   String
            'pattern',                  #   TremoliteBase+
        ))


        def __init__(t, name, pattern):
            t.name    = name
            t.pattern = pattern


        def __repr__(t):
            return arrange('<TremoliteMatch %s %r>', t.name, t.pattern)


    [match_cache, match_insert] = produce_cache_and_insert_function('tremolite.match')


    @export
    def MATCH(name, pattern):
        assert (type(name) is String) and (length(name) > 0)

        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        name = intern_string(name)

        return match_insert(name, TremoliteMatch(name, pattern))


    share(
        'match_cache',  match_cache,
    )
