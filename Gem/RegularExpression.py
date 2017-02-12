#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RegularExpression')
def gem():
    PythonRegularExpression    = __import__('re')
    compile_regular_expression = PythonRegularExpression.compile


    @export
    def make_match_function(pattern):
        return compile_regular_expression(pattern).match
