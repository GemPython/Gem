#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Expression')
def gem():
    require_gem('Sapphire.Token')


    @share
    class ExpressionBinaryBase(Object):
        __slots__ = ((
            'left',                     #   Expression
            'operator',                 #   Operator*
            'right',                    #   Expression
        ))


        def __init__(t, left, operator, right):
            t.left     = left
            t.operator = operator
            t.right    = right


        def __repr__(t):
            return arrange('<%s %r %r %r>', t.__class__.__name__, t.left, t.operator, t.right)


    @share
    class ExpressionComma(ExpressionBinaryBase):
        __slots__ = (())


    @share
    class ExpressionDot(ExpressionBinaryBase):
        __slots__ = (())


    @share
    class SingleQuote(Token):
        __slots__ = (())


        def __repr__(t):
            return arrange('<%s>', t.s)


    @share
    class Symbol(Token):
        __slots__ = (())


        def __repr__(t):
            return arrange('<$%s>', t.s)


    [
            conjure_symbol, lookup_symbol,
    ] = produce_cache_functions('Sapphire.symbol_cache', produce_conjure = true, produce_lookup = true)


    share(
        #
        #   Functions
        #
        'lookup_symbol',    lookup_symbol,


        #
        #   Values
        #
        'keyword_define',       conjure_symbol('def',    KeywordDefine),
        'keyword_from',         conjure_symbol('from',   KeywordFrom),
        'keyword_import',       conjure_symbol('import', KeywordImport),
        'keyword_return',       conjure_symbol('return', KeywordReturn),
        'operator_at_sign',     conjure_symbol('@',      OperatorAtSign),
    )
