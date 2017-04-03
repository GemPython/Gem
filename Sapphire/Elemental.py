#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Token')
def gem():
    require_gem('Sapphire.Token')


    class KeywordAndOperatorBase(Token):
        is_comma             = false
        is_right_parenthesis = false


        def __repr__(t):
            return arrange('<%s>', t.s)


    @export
    class KeywordAs(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = 'as'


    @export
    class KeywordDefine(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = 'def'


    @export
    class KeywordFrom(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = 'from'


    @export
    class KeywordImport(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = 'import'


    @export
    class KeywordReturn(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = 'return'


    @export
    class OperatorAtSign(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = '@'


    @export
    class OperatorComma(KeywordAndOperatorBase):
        __slots__ = (())
        is_comma  = true
        keyword   = ','


    @export
    class OperatorDot(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = '.'


    @export
    class OperatorLeftParenthesis(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = '('             #   )


    @export
    class OperatorLeftSquareBracket(KeywordAndOperatorBase):
        __slots__ = (())
        keyword   = '['             #   ]


    @export
    class OperatorRightParenthesis(KeywordAndOperatorBase):
        __slots__            = (())
        is_right_parenthesis = true
        #  ([
        keyword              = ')'


    @export
    class OperatorRightSquareBracket(KeywordAndOperatorBase):
        __slots__ = (())
        #   [
        keyword   = ']'


    @share
    class Symbol(Token):
        __slots__ = (())


        def __repr__(t):
            return arrange('<$%s>', t.s)


    [
            conjure_symbol, find_symbol, lookup_symbol,
    ] = produce_cache_functions(
            'Sapphire.symbol_cache',

            produce_conjure = true,
            produce_find    = true,
            produce_lookup  = true,
        )


    share(
        #
        #   Values
        #
        'keyword_define',       conjure_symbol('def',    KeywordDefine),
        'keyword_from',         conjure_symbol('from',   KeywordFrom),
        'keyword_import',       conjure_symbol('import', KeywordImport),
        'keyword_return',       conjure_symbol('return', KeywordReturn),
        'operator_at_sign',     conjure_symbol('@',      OperatorAtSign),
        'operator_comma',       conjure_symbol(',',      OperatorComma),
        'operator_dot',         conjure_symbol('.',      OperatorDot),
    )
