#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Build')
def gem():
    require_gem('Gem.PortrayString')
    require_gem('Tremolite.Core')


    from Gem import execute, portray_raw_string


    exact_map   = {}
    find_exact  = exact_map.__getitem__
    store_exact = exact_map.__setitem__


    @execute
    def execute():
        is_special_character = FrozenSet(r'$()*+.?[\]^{}').__contains__


        for i in iterate_range(ordinal(' '), ordinal('~') + 1):
            c = character(i)

            store_exact(c, '\\' + c   if is_special_character(c) else   c)


    class TremoliteBase(Object):
        __slots__ = ((
            'pattern',          #   String
        ))


        #def __init__(t, pattern):
        #    t.pattern = pattern


        def __add__(t, that):
            assert that.is_right_side_pattern

            return TremoliteAdd(t.pattern + that.pattern, ((t, that)) )


    class TremoliteAdd(TremoliteBase):
        __slots__ = ((
            'many',             #   Tuple of TremoliteBase+
        ))


        def __init__(t, pattern, many):
            t.pattern = pattern
            t.many    = many



        def __repr__(t):
            return arrange('<TremoliteAdd %s %s>',
                           portray_raw_string(t.pattern),
                           ' '.join(portray(v)   for v in t.many))


        def __str__(t):
            return ' + '.join(String(v)   for v in t.many)


    class TremoliteSpecial(TremoliteBase):
        __slots__ = ((
            'singular',         #   Boolean
            'original',         #   String
        ))


        is_right_side_pattern = true


        def __init__(t, pattern, singular, original):
            t.pattern  = intern_string(pattern)
            t.singular = singular
            t.original = intern_string(original)


        def __repr__(t):
            return arrange('<TremoliteSepcial %s %s %s>', portray_raw_string(t.pattern), t.singular, t.original)


        def __str__(t):
            return t.original

            
    class TremoliteExact(TremoliteBase):
        __slots__ = ((
            'singular',         #   Boolean
            'exact',            #   String
        ))


        is_right_side_pattern = true


        def __init__(t, pattern, singular, exact):
            t.pattern  = intern_string(pattern)
            t.singular = singular
            t.exact    = intern_string(exact)


        def __repr__(t):
            return arrange('<TremoliteExact %s %s %s>',
                           portray_raw_string(t.pattern), t.singular, portray_raw_string(t.exact))


        def __str__(t):
            return arrange('EXACT(%s)', portray_raw_string(t.exact))


    END_OF_STRING = TremoliteSpecial(r'\Z', true, 'END_OF_STRING')


    @export
    def EXACT(s):
        assert length(s) >= 1

        return TremoliteExact(
                   intern_string(''.join(find_exact(c)   for c in s)),
                   length(s) == 1,
                   intern_string(s),
               )

    export(
        'END_OF_STRING',    END_OF_STRING,
    )


    line('%s', EXACT(r'\r') + END_OF_STRING)
    line('%r', EXACT(r'\r') + END_OF_STRING)
