#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Build')
def gem():
    require_gem('Tremolite.Core')


    from Gem import execute


    exact_map   = {}
    find_exact  = exact_map.__getitem__
    store_exact = exact_map.__setitem__


    @execute
    def execute():
        is_special_character = FrozenSet(r'$()*+.?[\]^{}').__contains__


        for i in iterate_range(ordinal(' '), ordinal('~') + 1):
            c = character(i)

            store_exact(c, '\\' + c   if is_special_character(c) else   c)


    class TremoliteExact(Object):
        __slots__ = ((
            'pattern',          #   String
            'singular',         #   Boolean
            'exact',            #   String
        ))


        def __init__(t, pattern, singular, exact):
            t.pattern  = pattern
            t.singular = singular
            t.exact    = exact


        def __str__(t):
            return arrange('EXACT(%r)', t.exact)


    def EXACT(s):
        assert length(s) >= 1

        return TremoliteExact(
                   intern_string(''.join(find_exact(c)   for c in s)),
                   length(s) == 1,
                   intern_string(s),
               )

    line('%s', EXACT(r'\r'))
