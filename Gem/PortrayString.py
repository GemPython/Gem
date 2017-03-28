#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.PortrayString')
def gem():
    require_gem('Gem.Ascii')
    require_gem('Gem.Exception')
    require_gem('Gem.StringIO')


    P = String.__repr__


    class PortrayStringState(Object):
        __slots__ = ((
            'A',                        #   PortrayStringState
            'K',                        #   PortrayStringState
            'N',                        #   PortrayStringState
            'Q',                        #   PortrayStringState

            'kc',                       #   Function -> String
            'ks',                       #   Function -> String

            'pc',                       #   Function -> String
            'ps',                       #   Function -> String

            'ra',                       #   Function -> String
            'rq',                       #   Function -> String


            #
            #   Tracking ''' & """ for normal portray
            #
            'favorite_3',               #   Integer
            'end_C',                    #   Integer
            'end_S',                    #   Integer
        ))


        if __debug__:
            __slots__ = ((
                'name',                 #   String
            )) + __slots__


        if __debug__:
            def __init__(t, name):
                t.name = name
        else:
            def __init__(t, name):
                pass


        if __debug__:
            def __repr__(t):
                return arrange('<PortrayStringState %s>', t.name)

                
        def overall(t, A, K, L, Q, ra = 7, rq = 7, pc = 7, ps = 7, is_K = 0):
            if rq is 7:     rq = ra
            if pc is 7:     pc = rq
            if ps is 7:     ps = pc

            t.A = A
            t.K = K
            t.N = L             #   .N really means .L
            t.Q = Q

            t.ks = t.kc = is_K  #   .kc really means .is_K
            t.pc = pc
            t.ps = ps
            t.ra = ra
            t.rq = rq


        def setup(t, A, K, N, Q, ra = 0, rq = 7, kc = 7, ks = 7, pc = 7, ps = 7, F3 = 0):
            if ra is 0:
                assert rq is 7

            if rq is 7:
                rq = ra

            if kc is 7:
                assert ks is 7

                kc = P

            if ks is 7:
                ks = kc

            if pc is 7:
                assert ps is 7

                pc = P

            if ps is 7:
                ps = pc

            t.A = A
            t.K = K
            t.N = N
            t.Q = Q

            t.kc = (kc) or (P)
            t.ks = (ks) or (kc) or (P)
            t.pc = pc
            t.ps = (ps) or (pc)
            t.ra = ra
            t.rq = (rq) or (ra)

            t.favorite_3 = F3
            t.end_C = (1  if F3 is -1 else   0)
            t.end_S = (1  if F3 is 1  else   0)


    state = PortrayStringState


    #
    #   States (overall)
    #
    #       E = Empty
    #       K = Backslash
    #       L = Lemon
    #       N = Normal
    #       T = Starts with "
    #       U = Starts with '
    #
    E  = state('E')
    K  = state('K')
    L  = state('L')
    N  = state('N')
    TK = state('TK')
    TL = state('TL')
    T  = state('T')
    UK = state('UK')
    UL = state('UL')
    U  = state('U')


    KC = PortrayStringState.kc.__get__
    KS = PortrayStringState.ks.__get__
    PC = PortrayStringState.pc.__get__
    PS = PortrayStringState.ps.__get__
    RA = PortrayStringState.ra.__get__
    RQ = PortrayStringState.rq.__get__
    _  = 7

    #           '   \   L   "   ra  rq  pc  ps
    E .overall (U,  K,  L,  T,  0)
    K .overall (_,  K,  L,  _,  RA, RQ, KC, KS, is_K = 7)
    L .overall (_,  L,  L,  _,  0,  _,  KC, KS)
    N .overall (N,  K,  L,  N,  RA, RQ, PC, PS)
    TK.overall (_,  TK, TL, _,  RA, _,  KC,     is_K = 7)
    TL.overall (_,  TL, TL, _,  0,  _,  KC)
    T .overall (_,  TK, TL, _,  RA, _,  PC)
    UK.overall (_,  UK, UL, _,  RQ, _,  KS,     is_K = 7)
    UL.overall (_,  UL, TL, _,  0,  _,  KS)
    U .overall (_,  UK, UL, _,  RQ, _,  PS)


    #
    #   States ('has' & ending)
    #
    #       A = '
    #       B = ''
    #       C = ''
    #
    #       K = \
    #       N = normal
    #
    #       Q = "
    #       R = ""
    #       S = """
    #
    A_A  = state('A_A')         #   Has '; ends in '
    A_B  = state('A_B')         #   Has '; ends in ''
    A_K  = state('A_K')         #   Has '; ends in \
    A_N  = state('A_N')         #   Has '

    AQ_A = state('AQ_A')        #   Has ' & "; ends in '
    AQ_B = state('AQ_B')        #   Has ' & "; ends in ''
    AQ_K = state('AQ_K')        #   Has ' & "; ends in \
    AQ_N = state('AQ_N')        #   Has ' & "
    AQ_Q = state('AQ_Q')        #   Has ' & "; ends in "
    AQ_R = state('AQ_R')        #   Has ' & "; ends in ""

    AS_A = state('AS_A')        #   Has ' & """; ends in '
    AS_B = state('AS_B')        #   Has ' & """; ends in ''
    AS_K = state('AS_K')        #   Has ' & """; ends in \
    AS_N = state('AS_N')        #   Has ' & """
    AS_Q = state('AS_Q')        #   Has ' & """; ends in "   or \"
    AS_R = state('AS_R')        #   Has ' & """; ends in ""
    AS_S = state('AS_S')        #   Has ' & """; ends in """

    C_A  = state('C_A')         #   Has '''; ends in '
    C_B  = state('C_B')         #   Has '''; ends in ''
    C_C  = state('C_C')         #   Has '''; ends in '''
    C_K  = state('C_K')         #   Has '''; ends in \
    C_N  = state('C_N')         #   Has '''

    CQ_A = state('CQ_A')        #   Has ''' & "; ends in '
    CQ_B = state('CQ_B')        #   Has ''' & "; ends in ''
    CQ_C = state('CQ_C')        #   Has ''' & "; ends in '''
    CQ_K = state('CQ_K')        #   Has ''' & "; ends in \
    CQ_N = state('CQ_N')        #   Has ''' & "
    CQ_Q = state('CQ_Q')        #   Has ''' & "; ends in "
    CQ_R = state('CQ_R')        #   Has ''' & "; ends in ""

    CS_A = state('CS_A')        #   Has ''' & """; ends in '
    CS_B = state('CS_B')        #   Has ''' & """; ends in ''
    CS_C = state('CS_C')        #   Has ''' & """; ends in '''
    CS_N = state('CS_N')        #   Has ''' & """
    CS_Q = state('CS_Q')        #   Has ''' & """; ends in "
    CS_R = state('CS_R')        #   Has ''' & """; ends in ""
    CS_S = state('CS_S')        #   Has ''' & """; ends in """

    N_K  = state('N_K')         #   normal; ends in \
    N_N  = state('N_N')         #   normal

    Q_K  = state('Q_K')         #   Has "; ends in \
    Q_N  = state('Q_N')         #   Has "
    Q_Q  = state('Q_Q')         #   Has "; ends in "
    Q_R  = state('Q_R')         #   Has "; ends in ""

    S_K  = state('S_K')         #   Has """: ends in \
    S_N  = state('S_N')         #   Has """
    S_Q  = state('S_Q')         #   Has """; ends in "
    S_R  = state('S_R')         #   Has """; ends in ""
    S_S  = state('S_S')         #   Has """; ends in """


    #
    #   Results
    #
    portray_inside_triple = {
                                A_B : 0,
                                C_A : intern_string(r"'"),
                                C_B : intern_string(r"'"),
                                C_C : intern_string(r"\'"),
                                C_N : 0,

                                Q_R : 0,
                                S_N : 0,
                                S_Q : intern_string(r'"'),
                                S_R : intern_string(r'"'),
                                S_S : intern_string(r'\"'),
                            }.__getitem__


    portray_last_inside_triple = {
                                     A_B : intern_string(r"'''"),
                                     C_A : intern_string(r"\''''"),
                                     C_B : intern_string(r"\''''"),
                                     C_C : intern_string(r"\''''"),
                                     C_N : intern_string(r"'''"),

                                     Q_R : intern_string(r'"""'),
                                     S_N : intern_string(r'"""'),
                                     S_Q : intern_string(r'\""""'),
                                     S_R : intern_string(r'\""""'),
                                     S_S : intern_string(r'\""""'),
                                 }.__getitem__


    def portray_backslash_string_with_triple_apostrophe(s):
        #line('KC: %r', s)

        f     = create_StringOutput()
        w     = f.write
        state = A_B

        w("'''")

        for c in s:
            a = lookup_ascii(c)

            if a is none:
                if state is not C_N:
                    if state is not A_B:
                        w(portray_inside_triple(state))

                    state = C_N

                w(portray(c)[1:-1])
                continue

            if a.is_apostrophe:
                previous = portray_inside_triple(state)

                if previous is not 0:
                    w(previous)

                state = state.A
                continue

            if state is not C_N:
                if state is not A_B:
                    w(portray_inside_triple(state))

                state = C_N

            w(a.portray)

        w(portray_last_inside_triple(state))

        return f.getvalue()


    def portray_backslash_string_with_triple_quotation_mark(s):
        #line('KS: %r', s)

        f     = create_StringOutput()
        w     = f.write
        state = Q_R

        w('"""')

        for c in s:
            a = lookup_ascii(c)

            if a is none:
                if state is not S_N:
                    if state is not Q_R:
                        w(portray_inside_triple(state))

                    state = S_N

                w(portray(c)[1:-1])
                continue

            if a.is_quotation_mark:
                previous = portray_inside_triple(state)

                if previous is not 0:
                    w(previous)

                state = state.Q
                continue

            if state is not S_N:
                if state is not Q_R:
                    w(portray_inside_triple(state))

                state = S_N

            w(a.portray)

        w(portray_last_inside_triple(state))

        return f.getvalue()


    def portray_raw_string_with_apostrophe(s):
        return "r'" + s + "'"


    def portray_raw_string_with_quotation_mark(s):
        return 'r"' + s + '"'


    def portray_raw_string_with_triple_apostrophe(s):
        return "r'''" + s + "'''"


    def portray_raw_string_with_triple_quotation_mark(s):
        return 'r"""' + s + '"""'


    def portray_string_with_triple_apostrophe(s):
        return "'''" + s + "'''"


    def portray_string_with_triple_quotation_mark(s):
        return '"""' + s + '"""'


    KC = portray_backslash_string_with_triple_apostrophe
    KS = portray_backslash_string_with_triple_quotation_mark

    PC = portray_string_with_triple_apostrophe
    PS = portray_string_with_triple_quotation_mark

    RA = portray_raw_string_with_apostrophe
    RC = portray_raw_string_with_triple_apostrophe
    RQ = portray_raw_string_with_quotation_mark
    RS = portray_raw_string_with_triple_quotation_mark

    _ = 7


    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    A_A  .setup(A_B,  A_K,  A_N,  AQ_Q, RQ, _)                              #   Has '; ends in '
    A_B  .setup(C_C,  A_K,  A_N,  AQ_Q, RQ, _)                              #   Has '; ends in ''
    A_K  .setup(A_N,  A_N,  A_N,  A_N)                                      #   Has '; ends in \
    A_N  .setup(A_A,  A_K,  A_N,  AQ_Q, RQ, _)                              #   Has '

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    AQ_A .setup(AQ_B, AQ_K, AQ_N, AQ_Q, RS, _,  KS, _,  KS, _)              #   Has ' & "; ends in '
    AQ_B .setup(CQ_C, AQ_K, AQ_N, AQ_Q, RS, _,  KS, _,  KS, _)              #   Has ' & "; ends in ''
    AQ_K .setup(AQ_N, AQ_N, AQ_N, AQ_N, 0,  _,  KC, KS, PC, PS)             #   Has ' & "; ends in \
    AQ_N .setup(AQ_A, AQ_K, AQ_N, AQ_Q, RC, RS, KC, KS, PC, PS)             #   Has ' & "
    AQ_Q .setup(AQ_A, AQ_K, AQ_N, AQ_R, RC, _,  KC, _,  KC, _)              #   Has ' & "; ends in "
    AQ_R .setup(AQ_A, AQ_K, AQ_N, AS_S, RC, _,  KC, _,  KC, _)              #   Has ' & "; ends in ""

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    AS_A .setup(AS_B, AS_K, AS_N, AS_Q, 0,  _,  KS, _,  KS, _)              #   Has ' & """; ends in '
    AS_B .setup(CS_C, AS_K, AS_N, AS_Q, 0,  _,  KS, _,  KS, _)              #   Has ' & """; ends in ''
    AS_K .setup(AS_N, AS_N, AS_N, AS_N, 0,  _,  KC, _,  PC, _)              #   Has ' & """; ends in \
    AS_N .setup(AS_A, AS_K, AS_N, AS_Q, RC, _,  KC, _,  PC, _)              #   Has ' & """
    AS_Q .setup(AS_A, AS_K, AS_N, AS_R, RC, _,  KC, _,  KC, _)              #   Has ' & """; ends in "
    AS_R .setup(AS_A, AS_K, AS_N, AS_S, RC, _,  KC, _,  KC, _)              #   Has ' & """; ends in ""
    AS_S .setup(AS_A, AS_K, AS_N, AS_R, RC, _,  KC, _,  KC, _,  F3 = 1)     #   Has ' & """; ends in """

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    C_A  .setup(C_B,  C_K,  C_N,  CQ_Q, RQ, _)                              #   Has '''; ends in '
    C_B  .setup(C_C,  C_K,  C_N,  CQ_Q, RQ, _)                              #   Has '''; ends in ''
    C_C  .setup(C_B,  C_K,  C_N,  CQ_Q, RQ, _,  F3 = -1)                    #   Has '''; ends in '''
    C_K  .setup(C_N,  C_N,  C_N,  C_N)                                      #   Has '''; ends in \
    C_N  .setup(C_A,  C_K,  C_N,  CQ_Q, RQ, _)                              #   Has '''

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    CQ_A .setup(CQ_B, CQ_K, CQ_N, CQ_Q, RS, _,  KS, _,  PS, _)              #   Has ''' & "; ends in '
    CQ_B .setup(CQ_C, CQ_K, CQ_N, CQ_Q, RS, _,  KS, _,  PS, _)              #   Has ''' & "; ends in ''
    CQ_C .setup(CQ_B, CQ_K, CQ_N, CQ_Q, RS, _,  KS, _,  PS, _,  F3 = -1)    #   Has ''' & "; ends in '''
    CQ_K .setup(CQ_N, CQ_N, CQ_N, CQ_N, 0,  _,  KS, _,  PS, _)              #   Has ''' & "; ends in \
    CQ_N .setup(CQ_A, CQ_K, CQ_N, CQ_Q, RS, _,  KS, _,  PS, _)              #   Has ''' & "
    CQ_Q .setup(CQ_A, CQ_K, CQ_N, CQ_R, 0,  _,  KC, _,  KC, _)              #   Has ''' & "; ends in "
    CQ_R .setup(CQ_A, CQ_K, CQ_N, CS_S, 0,  _,  KC, _,  KC, _)              #   Has ''' & "; ends in ""

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    CS_A .setup(CS_B, CS_N, CS_N, CS_Q, 0,  _,  KS, _,  KS, _)              #   Has ''' & """; ends in '
    CS_B .setup(CS_C, CS_N, CS_N, CS_Q, 0,  _,  KS, _,  KS, _)              #   Has ''' & """; ends in ''
    CS_C .setup(CS_B, CS_N, CS_N, CS_Q, 0,  _,  KS, _,  KS, _,  F3 = -1)    #   Has ''' & """; ends in '''
    CS_N .setup(CS_A, CS_N, CS_N, CS_Q, 0,  _,  KC, KS, PC, PS)             #   Has ''' & """
    CS_Q .setup(CS_A, CS_N, CS_N, CS_R, 0,  _,  KC, _,  KC, _)              #   Has ''' & """; ends in "
    CS_R .setup(CS_A, CS_N, CS_N, CS_S, 0,  _,  KC, _,  KC, _)              #   Has ''' & """; ends in ""
    CS_S .setup(CS_A, CS_N, CS_N, CS_R, 0,  _,  KC, _,  KC, _,  F3 = 1)     #   Has ''' & """; ends in """

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    N_K  .setup(N_N,  N_N,  N_N,  N_N)                                      #   normal; ends in \
    N_N  .setup(A_A,  N_K,  N_N,  Q_Q,  RA, RQ)                             #   normal

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    Q_K  .setup(Q_N,  Q_N,  Q_N,  Q_N)                                      #   Has "; ends in \
    Q_N  .setup(AQ_A, Q_K,  Q_N,  Q_Q,  RA, _)                              #   Has "
    Q_Q  .setup(AQ_A, Q_K,  Q_N,  Q_R,  RA, _)                              #   Has "; ends in "
    Q_R  .setup(AQ_A, Q_K,  Q_N,  S_S,  RA, _)                              #   Has "; ends in ""

    #           '     \     N     "     ra  rq  kc  ks  pc  ps
    S_K  .setup(S_N,  S_N,  S_N,  S_N)                                      #   Has """: ends in \
    S_N  .setup(AS_A, S_K,  S_N,  S_Q,  RA, _)                              #   Has """
    S_Q  .setup(AS_A, S_K,  S_N,  S_R,  RA, _)                              #   Has """; ends in "
    S_R  .setup(AS_A, S_K,  S_N,  S_S,  RA, _)                              #   Has """; ends in ""
    S_S  .setup(AS_A, S_K,  S_N,  S_R,  RA, _,  F3 = 1)                     #   Has """; ends in """


    del PortrayStringState.__init__, PortrayStringState.setup


    @export
    def portray_raw_string(s):
        iterator = iterate(s)
        overall  = E

        #
        #   Simple case
        #
        for c in iterator:
            a = lookup_ascii(c, unknown_ascii)

            #line('c: %r, a: %r', c, a)

            if not a.is_portray_boring:
                break

            overall  = N
        else:
            #line('portray_raw_string(%r): simple', s)

            return "r'" + s + "'"

        #
        #   Complex case
        #
        #line('portray_raw_string(%r): %s', s, a)

        if a.is_backslash:
            #line('  %r: backslash: %s, %s', c, N_K.name, N_N.name)

            overall   = K
            favorite  = 0
            raw_state = N_K
            state     = N_N
        else:
            if a.is_apostrophe:
                #line('  %r: %s, %s', c, A_A.name, A_A.name)

                overall   = overall.A
                favorite  = -1
                raw_state = state = A_A
            elif a.is_quotation_mark:
                #line('  %r: %s, %s', c, Q_Q.name, Q_Q.name)

                overall  = overall.Q
                favorite = 1
                raw_state = state = Q_Q
            else:
                #line('  %r: lemon: %s, %s', c, N_N.name, N_N.name)

                overall   = L
                favorite  = 0
                raw_state = state = N_N

        C = S = 0

        for c in iterator:
            a = lookup_ascii(c, unknown_ascii)

            if a.is_portray_boring:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.N.name, state.name, state.N.name)

                raw_state = raw_state.N
                state     = state.N

                continue

            if a.is_apostrophe:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.A.name, state.name, state.A.name)

                raw_state   = raw_state.A
                state       = state.A
                favorite   -= 1
                C          += state.favorite_3
                continue

            if a.is_backslash:
                #line('  %r: backslash: %s => %s, %s => %s', c, raw_state.name, raw_state.K.name, state.name, state.N.name)

                backslash = 7
                overall   = overall.K
                raw_state = raw_state.K
                state     = state.N
                continue

            if a.is_quotation_mark:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.Q.name, state.name, state.Q.name)

                raw_state   = raw_state.Q
                state       = state.Q
                favorite   += 1
                S          -= state.favorite_3
                continue

            assert not a.is_printable

            #line('  %r: lemon: %s => %s, %s => %s', c, raw_state.name, raw_state.N.name, state.name, state.N.name)

            overall   = overall.N       #   .N really means .L
            raw_state = raw_state.N
            state     = state.N

        #line('  final %r: %d/%d/%d; %s, %s, %s', s, favorite, C, S, overall.name, raw_state.name, state.name)

        if (overall.ra is 0) or (raw_state.ra is 0):
            if ( (S == C) and (favorite >= 0) ) or (S > C):
            #if favorite_3 >= 0:
                return overall.pc(state)(s)

            return overall.ps(state)(s)

        if ( (S == C) and (favorite >= 0) ) or (S > C):
            #line('  %r: overall<%s>.ra(raw_state<%s>)<%s>',
            #    s, overall.name, raw_state.name, overall.ra(raw_state))

            return overall.ra(raw_state)(s)

        #line('  %r: overall<%s>.rq(raw_state<%s>)<%s>',
        #    s, overall.name, raw_state.name, overall.rq(raw_state))

        return overall.rq(raw_state)(s)


    @export
    def portray_string(s):
        iterator = iterate(s)
        overall  = E

        #
        #   Simple case
        #
        for c in iterator:
            a = lookup_ascii(c, unknown_ascii)

            #line('c: %r, a: %r', c, a)

            if not a.is_portray_boring:
                break

            overall  = N
        else:
            #line('portray_string(%r): simple', s)

            return "'" + s + "'"

        #
        #   Complex case
        #
        #line('portray_string(%r): %s', s, a)

        if a.is_backslash:
            #line('  %r: backslash: %s, %s', c, N_K.name, N_N.name)

            overall   = K
            favorite  = 0
            raw_state = N_K
            state     = N_N
        else:
            if a.is_apostrophe:
                #line('  %r: %s, %s', c, A_A.name, A_A.name)

                overall   = overall.A
                favorite  = -1
                raw_state = state = A_A
            elif a.is_quotation_mark:
                #line('  %r: %s, %s', c, Q_Q.name, Q_Q.name)

                overall  = overall.Q
                favorite = 1
                raw_state = state = Q_Q
            else:
                #line('  %r: lemon: %s, %s', c, N_N.name, N_N.name)

                overall   = L
                favorite  = 0
                raw_state = state = N_N

        C = S = 0

        for c in iterator:
            a = lookup_ascii(c, unknown_ascii)

            if a.is_portray_boring:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.N.name, state.name, state.N.name)

                raw_state = raw_state.N
                state     = state.N

                continue

            if a.is_apostrophe:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.A.name, state.name, state.A.name)

                raw_state   = raw_state.A
                state       = state.A
                favorite   -= 1
                C          += state.favorite_3
                continue

            if a.is_backslash:
                #line('  %r: backslash: %s => %s, %s => %s', c, raw_state.name, raw_state.K.name, state.name, state.N.name)

                backslash = 7
                overall   = overall.K
                raw_state = raw_state.K
                state     = state.N
                continue

            if a.is_quotation_mark:
                #line('  %r: %s => %s, %s => %s', c, raw_state.name, raw_state.Q.name, state.name, state.Q.name)

                raw_state   = raw_state.Q
                state       = state.Q
                favorite   += 1
                S          -= state.favorite_3
                continue

            assert not a.is_printable

            #line('  %r: lemon: %s => %s, %s => %s', c, raw_state.name, raw_state.N.name, state.name, state.N.name)

            overall   = overall.N       #   .N really means .L
            raw_state = raw_state.N
            state     = state.N

        #line('  final %r: %d/%d/%d; %s, %s, %s', s, favorite, C, S, overall.name, raw_state.name, state.name)

        if (overall.kc is 7) and (raw_state.ra is not 0):
            if ( (S == C) and (favorite >= 0) ) or (S > C):
                #line('  %r: overall<%s>.ra(raw_state<%s>)<%s>', s, overall.name, raw_state.name, overall.ra(raw_state))

                return overall.ra(raw_state)(s)

            #line('  %r: overall<%s>.rq(raw_state<%s>)<%s>', s, overall.name, raw_state.name, overall.rq(raw_state))

            return overall.rq(raw_state)(s)

        if ( (S == C) and (favorite >= 0) ) or (S > C):
            #line('  %r: overall<%s>.pc(state<%s>)<%s>', s, overall.name, state.name, overall.pc(state))

            return overall.pc(state)(s)

        #line('  %r: overall<%s>.ps(state<%s>)<%s>', s, overall.name, state.name, overall.ps(state))

        return overall.ps(state)(s)


    export(
        'N_N',  N_N,                    #   For unit testing
    )
