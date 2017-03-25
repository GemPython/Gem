#
#   Copyright 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Match')
def gem():
    require_gem('Tremolite.Compile')


    from Tremolite import compile_regular_expression


    def M(regular_expression, code, groups = 0, flags = 0):
        return compile_regular_expression(regular_expression, code, groups, flags).match


    C = (
        #
        #<copyright>
        #   The following is produced from python's standard library
        #   'sre_compile.py', function 'compile' and is thus:
        #
        #       Copyright (c) 1998-2001 by Secret Labs AB.  All rights reserved.
        #
        #       This version of the SRE library can be redistributed under CNRI's
        #       Python 1.6 license.  For any other use, please contact Secret Labs
        #       AB (info@pythonware.com).
        #
        #   (Currently the same copyright is used for both python 2.7 & 3.5 versions)
        #
        #   P.S.:  To make things simple, all *changes* to the original code below are dual licensed under
        #          both (1) the MIT License that the rest of Gem is licensed; and (2) under the exact same
        #          "CNRI's Python 1.6" license as the original code.
        #
        #   NOTE:  Dual copyright only applies to the changes, not to the original code which is obviously
        #          only licensed under the original license.
        #

        #
        #   r'[a-z][0-9a-z_]*\Z'
        #
        (17, 8, 4, 1, 0, 27, 97, 122, 0, 15, 5, 27, 97, 122, 0, 29, 16, 0, 4294967295L, 15, 11, 10, 0, 67043328, 2147483648, 134217726, 0, 0, 0, 0, 0, 1, 6, 7, 1),

        #</copyright>
    ).__getitem__

    #
    #   group_name_match
    #
    #       ANY_OF('a-z') + ZERO_OR_MORE(ANY_OF('0-9', 'a-z', '_')) + END_OF_PATTERN
    #
    group_name_match = M(
        r'[a-z][0-9a-z_]*\Z',
        C(0),
    )


    export(
        'group_name_match',     group_name_match,
    )
