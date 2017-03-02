#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Ascii')
def gem():
    require_gem('Gem.Map')


    from Gem import execute


    ascii_map = {}


    class Ascii(Object):
        __slots__ = ((
            'c',                        #   String
            'portray',                  #   String
            'is_backslash',             #   Boolean
            'is_double_quote',          #   Boolean
            'is_portray_special',       #   Boolean
            'is_printable',             #   Boolean
            'is_single_quote',          #   Boolean
        ))


        def __init__(
                t, c, portray,

                is_backslash    = false,
                is_double_quote = false,
                is_printable    = false,
                is_single_quote = false,
        ):
            t.c       = c
            t.portray = portray

            t.is_backslash       = is_backslash
            t.is_double_quote    = is_double_quote
            t.is_portray_special = (is_backslash) or (is_double_quote) or (not is_printable) or (is_single_quote)
            t.is_printable       = is_printable
            t.is_single_quote    = is_single_quote


        if __debug__:
            def __repr__(t):
                other = ''

                if t.is_backslash:         other += ' is_backslash'
                if t.is_double_quote:      other += ' is_double_quote'
                if t.is_portray_special:   other += ' is_portray_special'
                if t.is_printable:         other += ' is_printable'
                if t.is_single_quote:      other += ' is_single_quote'

                return arrange('<Ascii %r %r%s>', t.c, t.portray, other)



    @execute
    def execute():
        store_ascii = ascii_map.__setitem__

        for i in iterate_range(0, 128):
            c         = character(i)
            c_portray = portray(c)[1:-1]

            if not (32 <= i <= 126):
                store_ascii(c, Ascii(c, c_portray))
                continue

            if c == '"':
                store_ascii(c, Ascii(c, c_portray, is_double_quote = true, is_printable = true))
                continue

            if c == '\\':
                store_ascii(c, Ascii(c, c_portray, is_backslash = true, is_printable = true))
                continue

            if c == "'":
                store_ascii(c, Ascii(c, c_portray, is_printable = true, is_single_quote = true))
                continue

            store_ascii(c, Ascii(c, c_portray, is_printable = true))


        if 0:
            for [i, k] in iterate_items_sorted_by_key(ascii_map):
                line('%r: %r', i, k)


    share(
        'lookup_ascii',     ascii_map.get,
        'unknown_ascii',    Ascii(none, none),
    )


    del Ascii.__init__
