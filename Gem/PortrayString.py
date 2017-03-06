#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.RawString_3')
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

            'finish_normal',            #   Function -> String
            'finish_other',             #   Function -> String
        ))


        def __init__(t, name):
            t.name = name


        def setup(t, apostrophe, backslash, normal, quotation_mark, finish_normal, finish_other):
            t.apostrophe     = apostrophe
            t.backslash      = backslash
            t.normal         = normal
            t.quotation_mark = quotation_mark

            t.finish_normal = finish_normal
            t.finish_other  = finish_other


    state = PortrayStringState


    #
    #   states
    #
    #       A = '
    #       B = ''
    #       C = ''
    #
    #       K = \
    #       N = normal
    #       M = normal -- might end in ", "", ', or ''
    #
    #       Q = "
    #       R = ""
    #       S = """
    #
    #       X = non-ascii
    #
    start  = state('start')
    X      = state('X')

    A_A    = state('A_A')       #   Has '; ends in '
    A_B    = state('A_B')       #   Has '; ends in ''
    A_N    = state('A_N')       #   Has '

    AK_A   = state('AK_A')      #   Has ' & \; ends in '
    AK_B   = state('AK_B')      #   Has ' & \; ends in ''
    AK_K   = state('AK_K')      #   Has ' & \; ends in \
    AK_N   = state('AK_N')      #   Has ' & \

    AKQ_A  = state('AKQ_A')     #   Has ', \, & "; ends in '
    AKQ_B  = state('AKQ_B')     #   Has ', \, & "; ends in ''
    AKQ_K  = state('AKQ_K')     #   Has ', \, & "; ends in \
    AKQ_N  = state('AKQ_N')     #   Has ', \, & "
    AKQ_Q  = state('AKQ_Q')     #   Has ', \, & "; ends in "
    AKQ_R  = state('AKQ_R')     #   Has ', \, & "; ends in ""

    AKS_A  = state('AKS_A')     #   Has ', \, & """; ends in '
    AKS_B  = state('AKS_B')     #   Has ', \, & """; ends in ''
    AKS_K  = state('AKS_K')     #   Has ', \, & """; ends in \
    AKS_M  = state('AKS_M')     #   Has ', \, & """; might end in " or ""

    AQ_A   = state('AQ_A')      #   Has ' & "; ends in '
    AQ_B   = state('AQ_b')      #   Has ' & "; ends in ''
    AQ_N   = state('AQ_N')      #   Has ' & "
    AQ_Q   = state('AQ_Q')      #   Has ' & "; ends in "
    AQ_R   = state('AQ_R')      #   Has ' & "; ends in ""

    AS_A   = state('AS_A')      #   Has ' & """; ends in '
    AS_B   = state('AS_B')      #   Has ' & """; ends in ''
    AS_M   = state('AS_M')      #   Has ' & """; might end in " or ""

    C_M    = state('C_M')       #   Has '''; might end in ' or ""

    CK_K   = state('CK_K')      #   Has ''' & \; ends in \
    CK_M   = state('CK_M')      #   Has ''' & \; might end in ' or ''

    CKQ_K  = state('CKQ_K')     #   Has ''', \, & "; ends in \
    CKQ_M  = state('CKQ_M')     #   Has ''', \, & "; might end in ' or ''
    CKQ_Q  = state('CKQ_Q')     #   Has ''', \, & "; ends in "
    CKQ_R  = state('CKQ_R')     #   Has ''', \, & "; ends in ""

    CQ_M   = state('CQ_M')      #   Has ''' & "; might end in ' or ''
    CQ_Q   = state('CQ_Q')      #   Has ''' & "; ends in "
    CQ_R   = state('CQ_R')      #   Has ''' & "; ends in ""

    K_K    = state('K_K')       #   Has \; ends in \
    K_N    = state('K_N')       #   Has \

    KQ_K   = state('KQ_K')      #   Has \ & "; ends in \
    KQ_N   = state('KQ_N')      #   Has \ & "
    KQ_Q   = state('KQ_Q')      #   Has \ & "; ends in "
    KQ_R   = state('KQ_R')      #   Has \ & "; ends in ""

    KS_K   = state('KS_K')      #   Has \ & """: ends in \
    KS_M   = state('KS_N')      #   Has \ & """; might end in " or ""

    N_N    = state('N_N')       #   totally normal, nothing to see here

    Q_N    = state('N_N')       #   Has "
    Q_Q    = state('N_N')       #   Has "; ends in "
    Q_R    = state('N_N')       #   Has "; ends in " in ""

    S_M    = state('N_N')       #   Has """; might end in " or ""


    #
    #   Results
    #
    def portray_raw_string_empty(s):
        assert (s == '') and (r"r''" is intern_string(r"r''"))

        return r"r''"


    def portray_raw_string_with_apostrophe(s):
        return "r'" + s + "'"


    if __debug__:
        def portray_raw_string_invalid(s):
            raise_runtime_error('portray_raw_string_invalid called on %r', s)


    def portray_raw_string_with_quotation_mark(s):
        return 'r"' + s + '"'


    portray_string = String.__repr__


    def portray_raw_string_with_triple_apostrophe(s):
        return "r'''" + s + "'''"


    def portray_raw_string_with_triple_quotation_mark(s):
        return 'r"""' + s + '"""'


    A = portray_raw_string_with_apostrophe
    C = portray_raw_string_with_triple_apostrophe
    I = portray_raw_string_empty
    Q = portray_raw_string_with_quotation_mark
    P = portray_string
    S = portray_raw_string_with_triple_quotation_mark
    _ = (portray_raw_string_invalid  if __debug__ else   portray_string)


    #           '       \       N_N     "       N   O
    start.setup(A_A,    K_K,    N_N,    Q_Q,    I,  _)
    X    .setup(X,      X,      X,      X,      P,  P)

    #           '       \       N_N     "       N   O
    A_A  .setup(A_B,    AK_N,   A_N,    AQ_Q,   _,  Q)
    A_B  .setup(C_M,    AK_N,   A_N,    AQ_Q,   _,  Q)
    A_N  .setup(A_A,    AK_N,   A_N,    AQ_Q,   _,  Q)

    #           '       \       N_N     "       N   O
    AK_A .setup(AK_N,   AK_K,   AK_N,   AKQ_Q,  Q,  Q)
    AK_B .setup(KS_M,   AK_K,   AK_N,   AKQ_Q,  Q,  Q)
    AK_K .setup(AK_N,   AK_N,   AK_N,   AKQ_Q,  P,  P)
    AK_N .setup(AK_N,   AK_K,   AK_N,   AKQ_Q,  Q,  Q)

    #           '       \       N_N     "       N   O
    AKQ_A.setup(AKQ_B,  AKQ_K,  AKQ_N,  AKQ_Q,  S,  S)
    AKQ_B.setup(CKQ_M,  AKQ_K,  AKQ_N,  AKQ_Q,  S,  S)
    AKQ_K.setup(AKQ_N,  AKQ_N,  AKQ_N,  AKQ_N,  P,  P)
    AKQ_N.setup(AKQ_A,  AKQ_K,  AKQ_N,  AKQ_Q,  C,  S)
    AKQ_Q.setup(AKQ_A,  AKQ_K,  AKQ_N,  AKQ_R,  C,  C)
    AKQ_R.setup(AKQ_A,  AKQ_K,  AKQ_N,  AKS_M,  C,  C)

    #           '       \       N_N     "       N   O
    AKS_A.setup(AKS_B,  AKS_K,  AKS_M,  AKS_M,  P,  P)
    AKS_B.setup(X,      AKS_K,  AKS_M,  AKS_M,  P,  P)
    AKS_K.setup(AKS_M,  AKS_M,  AKS_M,  AKS_M,  P,  P)
    AKS_M.setup(AKS_A,  AKS_K,  AKS_M,  AKS_M,  C,  C)

    #           '       \       N_N     "       N   O
    AQ_A .setup(AQ_B,   AKQ_K,  AQ_N,   AQ_Q,   S,  S)
    AQ_B .setup(CQ_M,   AKQ_K,  AQ_N,   AQ_Q,   S,  S)
    AQ_N .setup(AQ_A,   AKQ_K,  AQ_N,   AQ_Q,   C,  S)
    AQ_Q .setup(AQ_A,   AKQ_K,  AQ_N,   AQ_R,   C,  C)
    AQ_R .setup(AQ_A,   AKQ_K,  AQ_N,   AS_M,   C,  C)

    #           '       \       N_N     "       N   O
    AS_A .setup(AS_B,   AKS_K,  AS_M,   AS_M,   P,  P)
    AS_B .setup(X,      AKS_M,  AS_M,   AS_M,   P,  P)
    AS_M .setup(AS_A,   AKS_K,  AS_M,   AS_M,   C,  C)

    #           '       \       N_N     "       N   O
    C_M  .setup(C_M,    CK_K,   C_M,    CQ_Q,   Q,  Q)

    #           '       \       N_N     "       N   O
    CK_K .setup(CK_M,   CK_M,   CK_M,   CK_M,   P,  P)
    CK_M .setup(CK_M,   CK_K,   CK_M,   CKQ_Q,  Q,  Q)

    #           '       \       N_N     "       N   O
    CKQ_K.setup(CKQ_M,  CKQ_M,  CKQ_M,  CKQ_M,  P,  P)
    CKQ_M.setup(CKQ_M,  CKQ_K,  CKQ_M,  CKQ_Q,  S,  S)
    CKQ_Q.setup(CKQ_M,  CKQ_K,  CKQ_M,  CKQ_R,  P,  P)
    CKQ_R.setup(CKQ_M,  CKQ_K,  CKQ_M,  X,      P,  P)

    #           '       \       N_N     "       N   O
    CQ_M .setup(CQ_M,   CKQ_K,  CQ_M,   CQ_Q,   S,  S)
    CQ_Q .setup(CQ_M,   CKQ_K,  CQ_M,   CQ_R,   P,  P)
    CQ_R .setup(CQ_M,   CKQ_K,  CQ_M,   X,      P,  P)

    #           '       \       N_N     "       N   O
    K_K  .setup(K_N,    K_N,    K_N,    K_N,    P,  P)
    K_N  .setup(AK_A,   K_K,    K_N,    KQ_Q,   A,  Q)

    #           '       \       N_N     "       N   O
    KQ_K .setup(KQ_N,   KQ_N,   KQ_N,   KQ_N,   P,  P)
    KQ_N .setup(AKQ_A,  KQ_K,   KQ_N,   KQ_Q,   A,  A)
    KQ_Q .setup(AKQ_A,  KQ_K,   KQ_N,   KQ_R,   A,  A)
    KQ_R .setup(AKQ_A,  KQ_K,   KQ_N,   KS_M,   A,  A)

    #           '       \       N_N     "       N   O
    KS_K .setup(KS_M,   KS_M,   KS_M,   KS_M,   P,  P)
    KS_M .setup(AKS_A,  KS_K,   KS_M,   KS_M,   A,  A)

    #           '       \       N_N     "       N   O
    N_N  .setup(A_A,    K_K,    N_N,    Q_Q,    A,  _)

    #           '       \       N_N     "       N   O
    Q_N  .setup(AQ_A,   KQ_K,   Q_N,    Q_Q,    A,  _)
    Q_Q  .setup(AQ_A,   KQ_K,   Q_N,    Q_R,    A,  _)
    Q_R  .setup(AQ_A,   KQ_K,   Q_N,    S_M,    A,  _)

    #           '       \       N_N     "       N   O
    S_M  .setup(AS_A,   KS_M,   S_M,    S_M,    A,  _)


    del PortrayStringState.__init__, PortrayStringState.setup


    @export
    def portray_raw_string(s):
        favorite = 0
        state    = start
        iterator = iterate(s)

        #line('s: %r', s)

        for c in iterator:
            #old = state.name
            a = lookup_ascii(c, unknown_ascii)

            if a.is_portray_boring:
                state = state.normal
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_backslash:
                state = state.backslash
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_double_quote:
                favorite += 1
                state = state.quotation_mark
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_single_quote:
                favorite -= 1
                state = state.apostrophe
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            assert not a.is_printable

            return portray_string(s)

        #line('final: %d,%s,%s', favorite, state.name, last.name)

        if favorite >= 0:
            return state.finish_normal(s)

        return state.finish_other(s)
