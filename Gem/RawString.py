#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RawString')
def gem():
    require_gem('Gem.CatchException')
    require_gem('Gem.Map')


    from Gem import execute


    ascii_map   = {}
    lookup_ascii = ascii_map.get


    class Ascii(Object):
        __slots__ = ((
            'c',                        #   String
            'portray',                  #   String
            'is_backslash',             #   Boolean
            'is_double_quote',          #   Boolean
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

            t.is_backslash    = is_backslash
            t.is_double_quote = is_double_quote
            t.is_printable    = is_printable
            t.is_single_quote = is_single_quote


        if __debug__:
            def __repr__(t):
                other = ''

                if t.is_backslash:         other += ' is_backslash'
                if t.is_double_quote:      other += ' is_double_quote'
                if t.is_printable:         other += ' is_printable'
                if t.is_single_quote:      other += ' is_single_quote'

                return arrange('<Ascii %r %r%s>', t.c, t.portray, other)


    #unknown_ascii = Ascii(none, none, is_unknown = true)


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

        del Ascii.__init__

        if 0:
            for [i, k] in iterate_items_sorted_by_key(ascii_map):
                line('%r: %r', i, k)


    if __debug__:
        is_1_3_4_5_or_7 = FrozenSet([1, 3, 4, 5, 7]).__contains__
        is_2_3_5_6_or_7 = FrozenSet([2, 3, 5, 6, 7]).__contains__
        is_3_5_or_7     = FrozenSet([3, 5, 7      ]).__contains__

    is_0_or_2   = FrozenSet([ 0,  2]).__contains__
    is_4_or_5   = FrozenSet([ 4,  5]).__contains__
    is_6_or_7   = FrozenSet([ 6,  7]).__contains__
    is_9_or_10  = FrozenSet([ 9, 10]).__contains__
    is_11_or_12 = FrozenSet([11, 12]).__contains__


    @export
    def portray_raw_string(s):
        if s == '':
            return "r''"

        #
        #   favorite (counts quotes after a backslash):
        #       >= 0        prefer single quotes
        #       < 0         prefer double quotes
        #
        #   saw
        #       0 = no ' or " seen
        #       1 = saw a '
        #       2 = saw a "
        #       3 = saw a ' & a "
        #       4 = saw a '''
        #       5 = saw a ''' & "
        #       6 = saw a """
        #       7 = saw a """ & '
        #
        #   last
        #       0  = not special
        #       8  = last saw \
        #       9  = last saw "
        #       10 = last saw ""
        #       11 = last saw '
        #       12 = last saw ''
        #
        last = saw = favorite = 0

        for c in s:
            a = lookup_ascii(c)

            if (a is none) or (not a.is_printable):
                #
                #   Non printable ascii character -- can't show this as a raw string
                #
                return portray(s)

            if last is 0:
                if a.is_backslash:
                    last = 8                    #   8 = last saw \
                    continue

                if a.is_double_quote:
                    last = 9                    #   9 = last saw "
                    favorite += 1

                    if saw is 0:                #   0 = no ' or " seen
                        saw = 2                 #   2 = saw a "
                        continue

                    if saw is 1:                #   1 = saw a '
                        saw = 3                 #   3 = saw a ' & a "
                        continue

                    if saw is 4:                #   4 = saw a '''
                        saw = 5                 #   5 = saw a ''' & "
                        continue

                    #
                    #   2 = saw a "
                    #   3 = saw a ' & a "
                    #   5 = saw a ''' & "
                    #   6 = saw a """
                    #   7 = saw a """ & '
                    #
                    assert is_2_3_5_6_or_7(saw)
                    continue

                if a.is_single_quote:
                    last = 11                   #   11 = last saw '
                    favorite -= 1

                    if saw is 0:                #   0 = no ' or " seen
                        saw = 1                 #   1 = saw a '
                        continue

                    if saw is 2:                #   2 = saw a "
                        saw = 3                 #   3 = saw a ' & a "
                        continue

                    if saw is 6:                #   6 = saw a """
                        saw = 7                 #   7 = saw a """ & '
                        continue

                    #
                    #   1 = saw a '
                    #   3 = saw a ' & a "
                    #   4 = saw a '''
                    #   5 = saw a ''' & "
                    #   7 = saw a """ & '
                    #
                    assert is_1_3_4_5_or_7(saw)
                    continue

                continue

            if last is 8:                       #   8  = last saw \
                last = 0

                if a.is_double_quote:
                    favorite += 1
                    continue

                if a.is_single_quote:
                    favorite -= 1
                    continue

                continue

            if a.is_backslash:
                last = 8                        #   8 = last saw \
                continue

            if a.is_double_quote:
                favorite += 1

                if last is 9:                   #   9  = last saw "
                    last = 10                   #   10 = last saw ""
                    assert is_2_3_5_6_or_7(saw)
                    continue

                if last is 10:                  #   10 = last saw ""
                    last = 0

                    if saw is 2:                #   2 = saw a "
                        saw = 6                 #   6 = saw a """
                        continue

                    if saw is 3:                #   3 = saw a ' & a "
                        saw = 7                 #   7 = saw a """ & '
                        continue

                    if saw is 5:                #   5 = saw a ''' & "
                        #
                        #   last saw both ''' & """ -- can't show this as a raw string
                        #
                        return portray(s)

                    #
                    #   0 = no ' or " seen          (not valid -- since have seen a ")
                    #   1 = saw a '                 (not valid -- since have seen a ")
                    #   4 = saw a '''               (not valid -- since have seen a ")
                    #   6 = saw a """
                    #   7 = saw a """ & '
                    #
                    assert is_6_or_7(saw)
                    continue

                assert is_11_or_12(last)        #   11 = last saw '; 12 = last saw ''

                last = 9                        #   9 = last saw "

                if saw is 1:                    #   1 = saw a '
                    saw = 3                     #   3 = saw a ' & a "
                    continue

                if saw is 4:                    #   4 = saw a '''
                    saw = 5                     #   5 = saw a ''' & "
                    continue

                #
                #   0 = no ' or " seen              (not valid -- since have seen a ')
                #   2 = saw a "                     (not valid -- since have seen a ')
                #   3 = saw a ' & a "
                #   5 = saw a ''' & "
                #   6 = saw a """                   (not valid -- since have seen a ')
                #   7 = saw a """ & '
                #
                assert is_3_5_or_7(saw)
                continue

            if a.is_single_quote:
                favorite -= 1

                if is_9_or_10(last):            #   9  = last saw "; 10 = last saw ""
                    last = 11                   #   11 = last saw '

                    if saw is 2:                #   2 = saw a "
                        saw = 3                 #   3 = saw a ' & a "
                        continue

                    if saw is 6:                #   6 = saw a """
                        saw = 7                 #   7 = saw a """ & '
                        continue

                    #
                    #   0 = no ' or " seen      (not valid -- since have seen a ")
                    #   1 = saw a '             (not valid -- since have seen a ")
                    #   3 = saw a ' & a "
                    #   4 = saw a '''           (not valid -- since have seen a ")
                    #   5 = saw a ''' & "
                    #   7 = saw a """ & '
                    #
                    assert is_3_5_or_7(saw)
                    continue

                if last is 11:                  #   11 = last saw '
                    last = 12                   #   12 = last saw ''
                    assert is_1_3_4_5_or_7(saw)
                    continue

                assert last is 12               #   12 = last saw ''

                last = 0

                if saw is 1:                    #   1 = saw a '
                    saw = 4                     #   4 = saw a '''
                    continue

                if saw is 3:                    #   3 = saw a ' & a "
                    saw = 5                     #   5 = saw a ''' & "
                    continue

                if saw is 7:                    #   7 = saw a """ & '
                    #
                    #   last saw both ''' & """ -- can't show this as a raw string
                    #
                    return portray(s)

                #
                #   0 = no ' or " seen          (not valid -- since have seen a ')
                #   2 = saw a "                 (not valid -- since have seen a ')
                #   4 = saw a '''
                #   5 = saw a ''' & "
                #   6 = saw a """               (not valid -- since have seen a ')
                #
                assert is_4_or_5(saw)
                continue

            last = 0
            continue

        line('finished %r: saw %d, last: %d, favorite: %d', s, saw, last, favorite)

        if last is 8:                           #       8  = last saw \
            #
            #   last saw a terminating \ -- can't show this as a raw string
            #
            return portray(s)           

        #
        #   0 = no ' or " seen
        #   2 = saw a "
        #
        if is_0_or_2(saw):
            return "r'" + s + "'"

        #
        #   1 = saw a '
        #
        if saw is 1:
            return 'r"' + s + '"'

        #
        #<special-cases>
        #   Special cases -- handle starts or ends with ' or ", thus forced to use ''' or """:
        #
        if 7 is 7:
            s0 = s[0]

            #
            #   9  = last saw "
            #   10 = last saw ""
            #
            if (s0 == '"') or (is_9_or_10(last)):
                #
                #   4 = saw a '''
                #   5 = saw a ''' & "
                #
                if is_4_or_5(saw):
                    return portray(s)           #   Can't portray with ''' since has internal '''

                return "r'''" + s + "'''"

            #
            #   11 = last saw '
            #   12 = last saw ''
            #
            if (s0 == "'") or (is_11_or_12(last)):
                #
                #   6 = saw a """
                #   7 = saw a """ & '
                #
                if is_6_or_7(saw):
                    return portray(s)           #   Can't portray with """ since has internal """

                return 'r"""' + s + '"""'
        #</special-cases>

        #
        #   3  = saw a ' & a "
        #
        if saw is 3:
            if favorite >= 0:
                return "r'''" + s + "'''"

            return 'r"""' + s + '"""'


        #
        #   4 = saw a '''
        #   5 = saw a ''' & "
        #
        if is_4_or_5(saw):
            return 'r"""' + s + '"""'

        #
        #   6 = saw a """
        #   7 = saw a """ & '
        #
        assert is_6_or_7(saw)

        return "r'''" + s + "'''"
