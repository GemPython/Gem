#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RawString')
def gem():
    require_gem('Gem.Ascii')


    if __debug__:
        is_1_3_4_5_or_7 = FrozenSet([1, 3, 4, 5, 7]).__contains__
        is_2_3_5_6_or_7 = FrozenSet([2, 3, 5, 6, 7]).__contains__
        is_3_5_or_7     = FrozenSet([3, 5, 7      ]).__contains__

    is_1_or_4   = FrozenSet([ 1,  4]).__contains__
    is_2_or_6   = FrozenSet([ 2,  6]).__contains__
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
        #
        if saw is 0:
            if favorite >= 0:
                return "r'" + s + "'"

            return 'r"' + s + '"'

        #
        #   1 = saw a '
        #   4 = saw a '''
        #
        if is_1_or_4(saw):
            return 'r"' + s + '"'

        #
        #   2 = saw a "
        #   6 = saw a """
        #
        if is_2_or_6(saw):
            return "r'" + s + "'"

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
        #   5 = saw a ''' & "
        #
        if saw is 5:
            return 'r"""' + s + '"""'

        #
        #   7 = saw a """ & '
        #
        assert saw is 7

        return "r'''" + s + "'''"
