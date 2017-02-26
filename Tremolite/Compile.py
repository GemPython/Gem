#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Compile')
def gem():
    require_gem('Tremolite.Core')


    PythonRegularExpressionBedrock             = import_module('_sre')
    python__bedrock_compile_regular_expression = PythonRegularExpressionBedrock.compile


    empty_map = {}


    @export
    def compile_regular_expression(regular_expression, parsed):
        assert regular_expression.__class__ is String


        if not __debug__:
            regular_expression = none

        #
        #<copyright>
        #   Some of this code is from the python standard library 'sre_compile.py', function 'compile' & is thus:
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
        if parsed.__class__ is String:
            return python__bedrock_compile_regular_expression(
                       regular_expression, 0, List(ordinal(c)   for c in parsed),
                       0,
                       empty_map,
                       list_of_single_none,
                   )


        assert type(parsed) is Tuple

        total = length(parsed)

        assert total >= 2

        code  = List(ordinal(c)   for c in parsed[0])
        flags = parsed[1]

        line('flags: %r', flags)

        if flags.__class__ is Integer:
            if total is 2:
                return python__bedrock_compile_regular_expression(
                           regular_expression, flags, code,
                           0,
                           empty_map,
                           list_of_single_none,
                       )

            if total is 3:
                group_1 = parsed[2]

                return python__bedrock_compile_regular_expression(
                           regular_expression, flags, code,
                           1,
                           { group_1 : 1 },
                           [none, group_1],
                       )

            index_group    = List(parsed)
            index_group[0] = none

            del index_group[1]

            return python__bedrock_compile_regular_expression(
                       regular_expression, flags, code,
                       length(parsed) - 1,
                       { k : i - 1   for [i, k] in enumerate(parsed)   if i >= 2 },
                       index_group,
                   )

        if total is 2:
            group_1 = parsed[1]

            return python__bedrock_compile_regular_expression(
                       regular_expression, 0, code,
                       1,
                       { group_1 : 1 },
                       [none, group_1],
                   )

            index_group    = List(parsed)
            index_group[0] = none

            return python__bedrock_compile_regular_expression(
                       regular_expression, 0, code,
                       length(parsed),
                       { k : i   for [i, k] in enumerate(parsed)   if i >= 1 },
                       index_group,
                   )
    #</copyright>
