#
#   Copyright 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Match')
def gem():
    require_gem('Gem.System')
    require_gem('Tremolite.Compile')


    from Gem import python_version
    from Tremolite import compile_regular_expression


    if python_version == '2.7.12 (default, Nov 19 2016, 06:48:10) \n[GCC 5.4.0 20160609]':
        C = ((
            #
            #<copyright>
            #   The following is generated from calling python's standard library:
            #
            #       1.  'sre_parse.py', function parse; and
            #       2.  'sre_compile.py', function '_code'
            #
            #   then saving the result; and is thus possibly:
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
            0,

            #
            #   r'[A-Z_a-z][0-9A-Z_a-z]*\Z'
            #
            ((
                17, 14, 4, 1, 0, 10, 0, 0, 2281701374, 134217726, 0, 0, 0, 0, 0, 15, 11, 10, 0, 0, 2281701374,
                134217726, 0, 0, 0, 0, 0, 29, 16, 0, Long(4294967295), 15, 11, 10, 0, 67043328, 2281701374, 134217726,
                0, 0, 0, 0, 0, 1, 6, 7, 1,
            )),
            #</copyright>
        )).__getitem__


        def M(regular_expression, code, groups = 0, flags = 0):
            return compile_regular_expression(regular_expression, C(code), C(groups), C(flags)).match


    else:
        require_gem('Tremolite.Parse')


        from Tremolite import parse_ascii_regular_expression


        def M(regular_expression, code, groups = 0, flags = 0):
            return compile_regular_expression(
                regular_expression,
                *parse_ascii_regular_expression(regular_expression)#,
            ).match


    #
    #   identifier = ANY_OF('A-Z', '_', 'a-z') + ZERO_OR_MORE(ANY_OF('0-9', 'A-Z', '_', 'a-z'))
    #


    #
    #   name_match
    #
    #       identifier + END_OF_PATTERN
    #
    name_match = M(
        r'[A-Z_a-z][0-9A-Z_a-z]*\Z',
        1,
    )


    export(
        'name_match',   name_match,
    )
