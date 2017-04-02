#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Expression')
def gem():
    require_gem('Sapphire.Elemental')
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
    class Number(Token):
        __slots__ = (())


        def __repr__(t):
            return t.s


    @share
    class SingleQuote(Token):
        __slots__ = (())


        def __repr__(t):
            return arrange('<%s>', t.s)
