#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Statement')
def gem():
    require_gem('Sapphire.Token')


    @share
    class AsFragment(Object):
        __slots__ = ((
            'left_name',                    #   String+
            'keyword_as',                   #   KeywordAs
            'right_name',                   #   String+
        ))


        def __init__(t, left_name, keyword_as, right_name):
            t.left_name  = left_name
            t.keyword_as = keyword_as
            t.right_name = right_name


        def __repr__(t):
            return arrange('<AsFragment %s %s %s>', t.left_name, t.keyword_as, t.right_name)


    @share
    class Comment(Token):
        __slots__ = (())


    @share
    class DecoratorHeader(Object):
        __slots__ = ((
            'operator_decorator',           #   OperatorAtSign
            'expresssion',                  #   Any
        ))


        def __init__(t, operator_decorator, expresssion):
            t.operator_decorator = operator_decorator
            t.expresssion        = expresssion


        def  __repr__(t):
            return arrange('<DecoratorHeader %r %r>', t.operator_decorator, t.expresssion)


    @share
    class DefineHeader(Object):
        __slots__ = ((
            'keyword_define',               #   KeywordDefine
            'name',                         #   String
            'parameters_colon',             #   Parameter_0 | Parameter_1
        ))


        def __init__(t, keyword_define, name, parameters_colon):
            t.keyword_define   = keyword_define
            t.name             = name
            t.parameters_colon = parameters_colon


        def  __repr__(t):
            return arrange('<DefineHeader %s %s %r>', t.keyword_define, t.name, t.parameters_colon)


    class EmptyComment(Token):
        __slots__ = (())


        @static_method
        def __repr__():
            return '<EmptyComment>'


    @share
    class EmptyLine(Token):
        __slots__ = (())


        def __repr__(t):
            if t.s is '':
                return '<EmptyLine>'

            return arrange('<EmptyLine %r>', t.s)


    @share
    class IndentedComment(Token):
        __slots__ = ((
            'indented',                     #   String
        ))


        def __init__(t, indented, s):
            t.indented = indented
            t.s        = s


        def __repr__(t):
            if t.s is '':
                return arrange('<+# %r #>', t.indented)

            return arrange('<+# %r # %s>', t.indented, portray_string(t.s))


    @share
    class ParameterColon_0(Token):
        pass


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
    class StatementFromImport(Object):
        __slots__ = ((
            'keyword_from',                 #   KeywordFrom
            'module',                       #   String+
            'keyword_import',               #   KeywordImport
            'imported',                     #   String+ | AsFragment
        ))


        def __init__(t, keyword_from, module, keyword_import, imported):
            t.keyword_from   = keyword_from
            t.module         = module
            t.keyword_import = keyword_import
            t.imported       = imported


        def __repr__(t):
            return arrange('<StatementFrom %r %r %r %r>', t.keyword_from, t.module, t.keyword_import, t.imported)


    @share
    class StatementImport(Object):
        __slots__ = ((
            'keyword_import',               #   KeywordImport
            'module',                       #   String+
        ))


        def __init__(t, keyword_import, module):
            t.keyword_import = keyword_import
            t.module         = module


        def __repr__(t):
            return arrange('<StatementImport %r %r>', t.keyword_import, t.module)


    @share
    class StatementReturnExpression(Token):
        __slots__ = ((
            'keyword_return',               #   String
            'expression',                   #   String
        ))


        def __init__(t, keyword_return, expression):
            t.keyword_return = keyword_return
            t.expression     = expression


        def  __repr__(t):
            return arrange('<Return %r %s>', t.keyword_return, t.expression)


    share(
        'empty_comment',        EmptyComment(''),
        'empty_line',           EmptyLine(''),
    )
