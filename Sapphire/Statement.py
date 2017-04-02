#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Statement')
def gem():
    @share
    class ParameterColon_1(Object):
        __slots__ = ((
            'left_parenthesis',             #   String
            'argument_1',                   #   String
            'right_parenthesis__colon',     #   String
        ))


        def __init__(t, left_parenthesis, argument_1, right_parenthesis__colon):
            t.left_parenthesis         = left_parenthesis
            t.argument_1               = argument_1
            t.right_parenthesis__colon = right_parenthesis__colon


        def  __repr__(t):
            return arrange('<ParameterColon_1 %s %s %s>',
                           portray_string(t.left_parenthesis),
                           t.argument_1,
                           portray_string(t.right_parenthesis__colon))


    @share
    class DefineHeader(Object):
        __slots__ = ((
            'keyword_define',               #   String
            'name',                         #   String
            'parameters_colon',             #   Parameter_0 | Parameter_1
        ))


        def __init__(t, keyword_define, name, parameters_colon):
            t.keyword_define   = keyword_define
            t.name             = name
            t.parameters_colon = parameters_colon


        def  __repr__(t):
            return arrange('<DefineHeader %s %s %r>', portray_string(t.keyword_define), t.name, t.parameters_colon)
