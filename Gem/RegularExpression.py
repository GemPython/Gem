#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RegularExpression')
def gem():
    require_gem('Gem.Import')


    PythonRegularExpression    = import_module('re')
    compile_regular_expression = PythonRegularExpression.compile


    @export
    def make_match_function(pattern):
        return compile_regular_expression(pattern).match
