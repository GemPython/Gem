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


    @share
    class UnknownLine(Token):
        pass
