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
            'is_apostrophe',            #   Boolean
            'is_backslash',             #   Boolean
            'is_portray_boring',        #   Boolean
            'is_printable',             #   Boolean
            'is_quotation_mark',        #   Boolean
        ))


        def __init__(
                t, c, portray,

                is_apostrophe     = false,
                is_backslash      = false,
                is_printable      = false,
                is_quotation_mark = false,
        ):
            t.c       = c
            t.portray = portray

            t.is_apostrophe = is_apostrophe
            t.is_backslash  = is_backslash

            t.is_portray_boring = not (
                                         is_backslash
                                      or is_quotation_mark
                                      or not is_printable
                                      or is_apostrophe
                                  )

            t.is_printable      = is_printable
            t.is_quotation_mark = is_quotation_mark


        if __debug__:
            def __repr__(t):
                other = ''

                if t.is_apostrophe:        other += ' is_apostrophe'
                if t.is_backslash:         other += ' is_backslash'
                if t.is_portray_boring:    other += ' is_portray_boring'
                if t.is_printable:         other += ' is_printable'
                if t.is_quotation_mark:    other += ' is_quotation_mark'

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
                store_ascii(c, Ascii(c, c_portray, is_quotation_mark = true, is_printable = true))
                continue

            if c == '\\':
                store_ascii(c, Ascii(c, c_portray, is_backslash = true, is_printable = true))
                continue

            if c == "'":
                store_ascii(c, Ascii(c, c_portray, is_printable = true, is_apostrophe = true))
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
