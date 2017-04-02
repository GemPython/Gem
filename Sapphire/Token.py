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
            return t.keyword


    class KeywordDefine(KeywordBase):
        __slots__ = (())


        keyword = 'def'


    class KeywordReturn(KeywordBase):
        __slots__ = (())


        keyword = 'return'


    class OperatorAtSign(KeywordBase):
        __slots__ = (())


        keyword = '@'


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


    @share
    class UnknownLine(Token):
        pass


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
        'keyword_return',       conjure_symbol('return', KeywordReturn),
        'operator_at_sign',     conjure_symbol('@',      OperatorAtSign),
    )
