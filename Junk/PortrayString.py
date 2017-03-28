    if __debug__:
        def portray_raw_string_invalid(s):
            raise_runtime_error('portray_raw_string_invalid called on %r', s)

    #       L = unprintable [AKA: "Lemon"]
    L_A  = state('L_A')         #   Lemon; ends in '
    L_B  = state('L_B')         #   Lemon; ends in ''
    L_C  = state('L_C')         #   Lemon; ends in '''
    L_N  = state('L_N')         #   Lemon
    L_Q  = state('L_Q')         #   Lemon; ends in "
    L_R  = state('L_R')         #   Lemon; ends in ""
    L_S  = state('L_S')         #   Lemon; ends in """

    #           '     \     N     "
    L_A  .setup(L_B,  L_N,  L_N,  L_Q,  _, _)                       #   Lemon; ends in '
    L_B  .setup(L_C,  L_N,  L_N,  L_Q,  _, _)                       #   Lemon; ends in ''
    L_C  .setup(L_A,  L_N,  L_N,  L_Q,  _, _, F3 = -1)              #   Lemon; ends in '''
    L_N  .setup(L_A,  L_N,  L_N,  L_Q,  _, _)                       #   Lemon
    L_Q  .setup(L_A,  L_N,  L_N,  L_R,  _, _)                       #   Lemon; ends in "
    L_R  .setup(L_A,  L_N,  L_N,  L_S,  _, _)                       #   Lemon; ends in ""
    L_S  .setup(L_A,  L_N,  L_N,  L_Q,  _, _, F3 = 1)               #   Lemon; ends in """

