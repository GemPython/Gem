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
    def compile_regular_expression(regular_expression, code, flags = 0, groups = none):
        assert regular_expression.__class__ is String
        assert code              .__class__ is String
        assert flags             .__class__ is Integer


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
        if groups is none:
            return python__bedrock_compile_regular_expression(
                       (regular_expression   if __debug__ else   none),
                       flags,
                       List(ordinal(c)   for c in code),
                       0,
                       empty_map,
                       list_of_single_none,
                   )

        if groups.__class__ is String:
            return python__bedrock_compile_regular_expression(
                       (regular_expression   if __debug__ else   none),
                       flags,
                       List(ordinal(c)   for c in code),
                       1,
                       { groups : 1 },
                       [none, groups],
                   )


        index_group= [none]
        append_index = index_group.append

        for v in groups:
            append_index(v)

        return python__bedrock_compile_regular_expression(
                   (regular_expression   if __debug__ else   none),
                   flags,
                   List(ordinal(c)   for c in code),
                   length(groups),
                   { k : i + 1   for [i, k] in enumerate(groups) },
                   index_group,
               )
        #</copyright>
