#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Token')
def gem():
    @share
    class Token(Object):
        __slots__ = ((
            's',
        ))


        is_keyword = false


        def __init__(t, s):
            t.s = s


        def __repr__(t):
            return arrange('<%s %s>', t.__class__.__name__, portray_string(t.s))


    class KeywordBase(Token):
        __slots__ = ((
            'parse_line',                   #   Function
        ))


        is_keyword = true


        def __repr__(t):
            return arrange('<%s>', t.s)


    @export
    class KeywordAs(KeywordBase):
        __slots__ = (())


        keyword = 'as'


    @export
    class KeywordDefine(KeywordBase):
        __slots__ = (())


        keyword = 'def'


    @export
    class KeywordFrom(KeywordBase):
        __slots__ = (())


        keyword = 'from'


    @export
    class KeywordImport(KeywordBase):
        __slots__ = (())


        keyword = 'import'


    @export
    class KeywordReturn(KeywordBase):
        __slots__ = (())


        keyword = 'return'


    @export
    class OperatorComma(KeywordBase):
        __slots__ = (())


        keyword = ','


    @export
    class OperatorAtSign(KeywordBase):
        __slots__ = (())


        keyword = '@'


    @share
    class UnknownLine(Token):
        pass
