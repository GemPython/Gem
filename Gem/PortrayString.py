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
            'triple_apostrophe',        #   PortrayStringState
            'triple_quotation_mark',    #   PortrayStringState

            'finish_apostrope',         #   Function -> String
            'finish_normal',            #   Function -> String
            'finish_other',             #   Function -> String
            'finish_quotation_mark',    #   Function -> String
        ))


        def __init__(t, name):
            t.name = name


        def end(t, apostrophe, backslash, quotation_mark, finish_apostrope, finish_quotation_mark):
            t.setup(
                apostrophe, backslash, none, quotation_mark, none, none,
                finish_apostrope, none, none, finish_quotation_mark,
            )


        def setup(
                t, apostrophe, backslash, normal, quotation_mark, triple_apostrophe, triple_quotation_mark,
                finish_apostrope, finish_normal, finish_other, finish_quotation_mark,
        ):
            t.apostrophe            = apostrophe
            t.backslash             = backslash
            t.normal                = normal
            t.quotation_mark        = quotation_mark
            t.triple_apostrophe     = triple_apostrophe
            t.triple_quotation_mark = triple_quotation_mark

            t.finish_apostrope      = finish_apostrope
            t.finish_normal         = finish_normal
            t.finish_other          = finish_other
            t.finish_quotation_mark = finish_quotation_mark


    state = PortrayStringState


    #
    #   states
    #
    #       A = '
    #       C = '''
    #       E = ''' & "
    #
    #       K = backslash
    #       N = normal
    #
    #       Q = "
    #       R = ""
    #       S = """
    #
    start  = state('state')
    X      = state('X')

    A    = state('A')       #   Has '
    AK   = state('AK')      #   Has ' & \
    AKQ  = state('AKQ')     #   Has ', \, & "
    AKS  = state('AKS')     #   Has ', \, & """
    AQ   = state('AQ')      #   Has ' & "
    AS   = state('AS')      #   Has ' & """

    C    = state('C')       #   Has '''
    CK   = state('CK')      #   Has ''' & \
    CKQ  = state('CKQ')     #   Has ''', \, & "
    CQ   = state('CQ')      #   Has ''' & "

    K    = state('K')       #   Has \
    KQ   = state('KQ')      #   Has \ & "
    KS   = state('KQ')      #   Has \ & """

    N    = state('N')       #   totally normal, nothing to see here
    Q    = state('N')       #   Has "
    S    = state('N')       #   Has """


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


    RA = portray_raw_string_with_apostrophe
    RC = portray_raw_string_with_triple_apostrophe
    RI = portray_raw_string_empty
    RQ = portray_raw_string_with_quotation_mark
    RP = portray_string
    RS = portray_raw_string_with_triple_quotation_mark
    __ = (portray_raw_string_invalid  if __debug__ else   portray_string)


    #           '     \     N     "     '''   """   '    N    O    "
    start.setup(A,    K,    N,    Q,    C,    S,    __,  RI,  __,  __)
    X    .setup(X,    X,    X,    X,    X,    X,    RP,  RP,  RP,  RP)

    #           '     \     N     "     '''   """   '    N    O    "
    A    .setup(A,    AK,   A,    AQ,   C,    AS,   RQ,  __,  RQ,  __)
    AK   .setup(AK,   AK,   AK,   AKQ,  CK,   AKS,  RQ,  __,  RQ,  __)
    AKQ  .setup(AKQ,  AKQ,  AKQ,  AKQ,  CKQ,  AKS,  RS,  RC,  RS,  RC)
    AKS  .setup(AKS,  AKS,  AKS,  AKS,  X,    AKS,  RP,  RC,  RC,  RC)
    AQ   .setup(AQ,   AKQ,  AQ,   AQ,   CQ,   AS,   RS,  RC,  RS,  RC)
    AS   .setup(AS,   AKS,  AS,   AS,   X,    AS,   RP,  RC,  RC,  RC)

    #           '     \     N     "     '''   """   '    N    O    "
    C    .setup(C,    CK,   C,    CQ,   C,    X,    RQ,  __,  RQ,  __)
    CK   .setup(CK,   CK,   CK,   CKQ,  CK,   X,    RQ,  __,  RQ,  __)
    CKQ  .setup(CKQ,  CKQ,  CKQ,  CKQ,  CKQ,  X,    RS,  RS,  RS,  RP)
    CQ   .setup(CQ,   CKQ,  CQ,   CQ,   CQ,   X,    RS,  RS,  RS,  RP)

    #           '     \     N     "     '''   """   '    N    O    "
    K    .setup(AK,   K,    K,    KQ,   CK,   KS,   __,  RA,  __,  __)
    KQ   .setup(AKQ,  KQ,   KQ,   KQ,   CKQ,  KS,   __,  RA,  __,  RA)
    KS   .setup(AKS,  KS,   KS,   KS,   X,    KS,   __,  RA,  __,  RA)

    #           '     \     N     "     '''   """   '    N    O    "
    N    .setup(A,    K,    N,    Q,    C,    KS,   __,  RA,  __,  __)
    Q    .setup(AQ,   KQ,   Q,    Q,    CQ,   KS,   __,  RA,  __,  RA)
    S    .setup(AS,   KS,   S,    S,    X,    KS,   __,  RA,  __,  RA)


    #
    #   End states
    #
    end_A = state('end_A')      #       A = ends in '
    end_B = state('end_B')      #       B = ends in ''
    end_C = state('end_C')      #       C = ends in '''
    end_D = state('end_D')      #       D = ends in \'

    end_K = state('end_K')      #       K = ends in \
    end_N = state('end_N')      #       N = normal

    end_Q = state('end_Q')      #       Q = ends in "
    end_R = state('end_R')      #       R = ends in ""
    end_S = state('end_S')      #       S = ends in """
    end_T = state('end_T')      #       T = ends in \"


    finish_apostrope      = PortrayStringState.finish_apostrope     .__get__
    finish_normal         = PortrayStringState.finish_normal        .__get__
    finish_other          = PortrayStringState.finish_other         .__get__
    finish_quotation_mark = PortrayStringState.finish_quotation_mark.__get__


    def finish_portray(state):
        return portray_string


    end_A.end(end_B, end_K, end_Q, finish_apostrope,      finish_apostrope)
    end_B.end(end_C, end_K, end_Q, finish_apostrope,      finish_apostrope)
    end_C.end(end_C, end_K, end_Q, finish_apostrope,      finish_apostrope)
    end_D.end(end_A, end_K, end_Q, finish_apostrope,      finish_apostrope)

    end_K.end(end_D, end_N, end_T, finish_portray,        finish_portray)
    end_N.end(end_A, end_K, end_Q, finish_normal,         finish_other)

    end_Q.end(end_A, end_K, end_R, finish_quotation_mark, finish_quotation_mark)
    end_R.end(end_A, end_K, end_S, finish_quotation_mark, finish_quotation_mark)
    end_S.end(end_A, end_K, end_S, finish_quotation_mark, finish_quotation_mark)
    end_T.end(end_A, end_K, end_Q, finish_quotation_mark, finish_quotation_mark)


    del PortrayStringState.__init__, PortrayStringState.end, PortrayStringState.setup


    @export
    def portray_raw_string(s):
        favorite = 0
        state    = start
        last     = end_N
        iterator = iterate(s)

        #line('s: %r', s)

        for c in iterator:
            #old = state.name
            a = lookup_ascii(c, unknown_ascii)

            if a.is_portray_boring:
                last  = end_N
                state = state.normal
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_backslash:
                last  = last.backslash
                state = state.backslash
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_double_quote:
                favorite += 1
                last  = last.quotation_mark
                state = (state.triple_quotation_mark   if last is end_S else   state.quotation_mark)
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            if a.is_single_quote:
                favorite -= 1
                last = last.apostrophe
                state = (state.triple_apostrophe   if last is end_C else   state.apostrophe)
                #line('%s: %r, %s, %s', old, c, state.name, last.name)
                continue

            assert not a.is_printable

            return portray_string(s)

        #line('final: %d,%s,%s', favorite, state.name, last.name)

        if favorite >= 0:
            #line('last.finish_apostrophe: %s', last.finish_apostrope)

            return last.finish_apostrope(state)(s)

        return last.finish_quotation_mark(state)(s)
