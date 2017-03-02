#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RawString_2')
def gem():
    require_gem('Gem.Ascii')
    require_gem('Gem.Exception')


    class PortrayStringState(Object):
        __slots__ = ((
            'name',                     #   String

            'apostrophe',               #   PortrayStringState
            'backslash',                #   PortrayStringState
            'normal',                   #   PortrayStringState
            'quotation_mark',           #   PortrayStringState

            'finish',                   #   Function -> String
        ))


        def __init__(t, name):
            t.name = name


        def setup(t, apostrophe, backslash, normal, quotation_mark, finish):
            t.apostrophe     = apostrophe
            t.backslash      = backslash
            t.normal         = normal
            t.quotation_mark = quotation_mark

            t.finish = finish


    state = PortrayStringState


    def r_incomplete(s, favorite):
        raise_runtime_error('portray_raw_string: incomplete state on %r',  s)


    def r_invalid(s, favorite):
        raise_runtime_error('portray_raw_string: invalid state on %r',  s)


    incomplete = state('incomplete')
    invalid    = state('invalid')

    incomplete.setup(incomplete, incomplete, incomplete,  incomplete,  r_incomplete)
    invalid   .setup(invalid,    invalid,    invalid,     invalid,     r_invalid)


    def r_apostrophe(s, favorite):
        return "r'" + s + "'"


    def r_3_apostrophe(s, favorite):
        if s[0] == "'":
            return portray(s)

        return "r'''" + s + "'''"


    def r_3_quote(s, favorite):
        if s[0] == '"':
            return portray(s)

        return 'r"""' + s + '"""'


    def r_normal(s, favorite):
        if favorite >= 0:
            return "r'" + s + "'"

        return 'r"' + s + '"'


    def r_3_normal(s, favorite):
        s0 = s[0]

        if ((favorite >= 0) and (s0 != "'")) or (s0 == '"'):
            return "r'''" + s + "'''"

        return 'r"""' + s + '"""'


    def r_portray(s, favorite):
        return portray(s)


    def r_quote(s, favorite):
        return 'r"' + s + '"'


    def r_start(s, favorite):
        assert s == ''

        return r"r''"


    start = state('state')
    dual3 = state('dual3')
    X     = state('X')

    A_A   = state('A_A')
    A_B   = state('A_B')
    A_F   = state('A_F')
    A_K   = state('A_K')
    A_N   = state('A_N')

    AQ_A  = state('AQ_A')
    AQ_B  = state('AQ_B')
    AQ_E  = state('AQ_E')
    AQ_F  = state('AQ_F')
    AQ_K  = state('AQ_K')
    AQ_N  = state('AQ_N')
    AQ_Q  = state('AQ_Q')
    AQ_R  = state('AQ_R')

    AS_A  = state('AS_A')
    AS_B  = state('AS_B')
    AS_E  = state('AS_E')
    AS_K  = state('AS_K')
    AS_N  = state('AS_N')

    C_F   = state('C_F')
    C_K   = state('C_K')
    C_N   = state('C_N')

    CQ_F  = state('CQ_F')
    CQ_K  = state('CQ_K')
    CQ_N  = state('CQ_N')
    CQ_Q  = state('CQ_Q')
    CQ_R  = state('CQ_R')

    N_E   = state('N_E')
    N_F   = state('N_F')
    N_K   = state('N_K')
    N_N   = state('N_N')

    Q_E   = state('Q_E')
    Q_K   = state('Q_K')
    Q_N   = state('Q_N')
    Q_Q   = state('Q_Q')
    Q_R   = state('Q_R')

    S_E   = state('S_E')
    S_K   = state('S_K')
    S_N   = state('S_N')

    start.setup(A_A,   N_K,   N_N,   Q_Q,   r_start)
    dual3.setup(dual3, dual3, dual3, dual3, r_portray)
    X    .setup(X,     X,     X,     X,     r_portray)

    #
    #   A = '
    #   B = ''
    #   C = '''
    #
    #   E = ends in \'
    #   F = ends in \"
    #   K = ends in \
    #   N = normal
    #
    #   Q = "
    #   R = ""
    #   S = """
    #
    A_A .setup(A_B,   A_K,   A_N,   AQ_Q,  r_quote)
    A_B .setup(C_N,   A_K,   A_N,   AQ_Q,  r_quote)
    A_F .setup(A_N,   A_K,   A_N,   AQ_Q,  r_3_apostrophe)        #   Shouldn't if begins with apostrope
    A_K .setup(A_N,   A_N,   A_N,   A_F,   r_portray)
    A_N .setup(A_A,   A_K,   A_N,   AQ_Q,  r_quote)

    AQ_A.setup(AQ_B,  AQ_K,  AQ_N,  AQ_Q,  r_3_quote)             #   Shouldn't if begins with quote
    AQ_B.setup(CQ_N,  AQ_K,  AQ_N,  AQ_Q,  r_3_quote)             #   Shouldn't if begins with quote
    AQ_E.setup(AQ_A,  AQ_K,  AQ_N,  AQ_Q,  r_3_quote)             #   Shouldn't if begins with quote
    AQ_F.setup(AQ_A,  AQ_K,  AQ_N,  AQ_Q,  r_3_apostrophe)        #   Shouldn't if begins with apostrophe
    AQ_K.setup(AQ_E,  AQ_N,  AQ_N,  AQ_F,  r_portray)
    AQ_N.setup(AQ_A,  AQ_K,  AQ_N,  AQ_Q,  r_3_normal)
    AQ_Q.setup(AQ_A,  AQ_K,  AQ_N,  AQ_R,  r_3_apostrophe)        #   Shouldn't if begins with apostrope
    AQ_R.setup(AQ_A,  AQ_K,  AQ_N,  AS_N,  r_3_apostrophe)        #   Shouldn't if begins with apostrope

    AS_A.setup(AS_B,  AS_K,  AS_N,  AS_N,  r_portray)
    AS_B.setup(dual3, AS_K,  AS_N,  AS_N,  r_portray)
    AS_E.setup(AS_A,  AS_K,  AS_N,  AS_N,  r_portray)
    AS_K.setup(AS_E,  AS_N,  AS_N,  AS_N,  r_portray)
    AS_N.setup(AS_A,  AS_K,  AS_N,  AS_N,  r_3_apostrophe)        #   Shouldn't if begins with quote

    C_F .setup(C_N,   C_K,   C_N,   CQ_Q,  r_portray)
    C_K .setup(C_N,   C_N,   C_N,   C_N,   r_portray)
    C_N .setup(C_N,   C_K,   C_N,   CQ_Q,  r_quote)

    CQ_F.setup(CQ_N,  CQ_K,  CQ_N,  CQ_Q,  r_portray)
    CQ_K.setup(CQ_N,  CQ_N,  CQ_N,  CQ_F,  r_portray)
    CQ_N.setup(CQ_N,  CQ_K,  CQ_N,  CQ_Q,  r_3_quote)
    CQ_Q.setup(CQ_N,  CQ_K,  CQ_N,  CQ_R,  r_portray)
    CQ_R.setup(CQ_N,  CQ_K,  CQ_N,  dual3, r_portray)

    N_E .setup(A_A,   N_K,   N_N,   Q_Q,   r_quote)
    N_F .setup(A_A,   N_K,   N_N,   Q_Q,   r_apostrophe)
    N_K .setup(N_E,   N_N,   N_N,   N_F,   r_portray)
    N_N .setup(A_A,   N_K,   N_N,   Q_Q,   r_normal)

    Q_E .setup(AQ_A,  Q_K,   Q_N,   Q_Q,   r_3_quote)
    Q_K .setup(Q_E,   Q_N,   Q_N,   Q_N,   r_portray)
    Q_N .setup(AQ_A,  Q_K,   Q_N,   Q_Q,   r_apostrophe)
    Q_Q .setup(AQ_A,  Q_K,   Q_N,   Q_R,   r_apostrophe)
    Q_R .setup(AQ_A,  Q_K,   Q_N,   S_N,   r_apostrophe)

    S_E .setup(AS_N,  S_K,   S_N,   S_N,   r_portray)
    S_K .setup(S_E,   S_N,   S_N,   S_N,   r_portray)
    S_N .setup(AS_N,  S_K,   S_N,   S_N,   r_apostrophe)


    @export
    def portray_raw_string(s):
        favorite = 0
        state    = start
        iterator = iterate(s)

        #line('s: %r', s)

        for c in iterator:
            if state is incomplete:
                raise_runtime_error('incomplete: %r @ %r', s, c + ''.join(iterator))

            if state is invalid:
                raise_runtime_error('invalid: %r @ %r', s, c + ''.join(iterator))

            old = state.name
            a   = lookup_ascii(c, unknown_ascii)

            if a.is_portray_special:
                if a.is_backslash:
                    state = state.backslash
                    #line('%s: %r, %s', old, c, state.name)
                    continue

                if a.is_double_quote:
                    state = state.quotation_mark
                    favorite += 1
                    #line('%s: %r, %s', old, c, state.name)
                    continue

                if a.is_single_quote:
                    state = state.apostrophe
                    favorite -= 1
                    #line('%s: %r, %s', old, c, state.name)
                    continue

                assert not a.is_printable

                state = X
                #line('%s: %r, %s', old, c, state.name)
                continue

            state = state.normal
            #line('%s: %r, %s', old, c, state.name)

        #line('final state: %s', state.name)

        return state.finish(s, favorite)
