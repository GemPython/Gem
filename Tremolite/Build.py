#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Build')
def gem():
    require_gem('Tremolite.Core')
    require_gem('Tremolite.Compile')
    require_gem('Tremolite.Parse')
    require_gem('Tremolite.Match')


    class TremoliteBase(Object):
        __slots__ = ((
            'regular_expression',       #   String
            'portray',                  #   String
        ))


        is_tremolite_or = false


        #def __init__(t, regular_expression, portray):
        #    t.regular_expression = regular_expression
        #    t.portray            = portray


        def __add__(t, that):
            if type(that) is String:
                that = INVISIBLE_EXACT(that)
            elif that.is_tremolite_or:
                that = wrap_parenthesis(that)

            return TremoliteAdd(
                       t.regular_expression + that.regular_expression,
                       t.portray + ' + ' + that.portray,
                       ((t, that)),
                   )


        def __or__(t, that):
            if type(that) is String:
                that = INVISIBLE_EXACT(that)
            else:
                assert not that.is_tremolite_or

            return TremoliteOr(
                       t.regular_expression + '|' + that.regular_expression,
                       t.portray + ' | ' + that.portray,
                       ((t, that)),
                   )


        def __radd__(t, that):
            return INVISIBLE_EXACT(that) + t


        def __ror__(t, that):
            return INVISIBLE_EXACT(that) | t


        def __str__(t):
            return t.portray


        def compile_ascii_regular_expression(t):
            return compile_regular_expression(
                       t.regular_expression,
                       *parse_ascii_regular_expression(t.regular_expression)
                   )


    class TremoliteAdd(TremoliteBase):
        __slots__ = ((
            'many',                     #   Tuple of TremoliteBase+
        ))


        repeatable = true
        singular   = false


        def __init__(t, regular_expression, portray, many):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.many               = many


        def __repr__(t):
            return arrange('<TremoliteAdd %s %s>',
                           portray_string(t.regular_expression),
                           ' '.join((portray_string(v)   if type(v) is String else   portray(v))  for v in t.many))


        def __add__(t, that):
            if type(that) is String:
                that = INVISIBLE_EXACT(that)
            elif that.is_tremolite_or:
                that = wrap_parenthesis(that)

            return TremoliteAdd(
                       t.regular_expression + that.regular_expression,
                       t.portray + ' + ' + that.portray,
                       t.many + ((that,)),
                   )


    class TremoliteAnyOf(TremoliteBase):
        __slots__ = ((
            'many',                     #   Tuple of String
        ))


        repeatable = true
        singular   = true


        def __init__(t, regular_expression, portray, many):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.many               = many


        def __repr__(t):
            return arrange('<TremoliteAnyOf %s %s>',
                           portray_string(t.regular_expression),
                           ' '.join(portray_string(v)  for v in t.many))


    class TremoliteExact(TremoliteBase):
        __slots__ = ((
            'exact',                    #   String
            'singular',                 #   Boolean
        ))


        repeatable = true


        def __init__(t, regular_expression, portray, exact, singular):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.exact              = exact
            t.singular           = singular


        def __repr__(t):
            suffix = ('; singular'    if t.singular else    '')

            if t.regular_expression is t.exact:
                return arrange('<TremoliteExact %s%s>', portray_string(t.regular_expression), suffix)

            return arrange('<TremoliteExact %s %s%s>',
                           portray_string(t.regular_expression),
                           portray_string(t.exact),
                           suffix)


    class TremoliteGroup(TremoliteBase):
        __slots__ = ((
            'group_name',               #   String
            'inside',                   #   String
        ))


        repeatable = true
        singular   = true


        def __init__(t, regular_expression, portray, group_name, inside):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.group_name         = group_name
            t.inside             = inside


        def __repr__(t):
            return arrange('<TremoliteGroup %s %r>', t.group_name, t.inside)


    class TremoliteOr(TremoliteBase):
        __slots__ = ((
            'many',                     #   Tuple of TremoliteBase+
        ))


        is_tremolite_or = true
        repeatable      = true
        singular        = false


        def __init__(t, regular_expression, portray, many):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.many               = many


        def __repr__(t):
            return arrange('<TremoliteOr %s %s>',
                           portray_string(t.regular_expression),
                           ' '.join((portray_string(v)   if type(v) is String else   portray(v))  for v in t.many))


        def __add__(t, that):
            return wrap_parenthesis(t) + that


        def __or__(t, that):
            if type(that) is String:
                that = INVISIBLE_EXACT(that)

            return TremoliteOr(
                       t.regular_expression + '|' + that.regular_expression,
                       t.portray + ' | ' + that.portray,
                       t.many + ((that,)),
                   )


    class TremoliteParenthesis(TremoliteBase):
        __slots__ = ((
            'inside',                   #   String
        ))


        repeatable = true
        singular   = true


        def __init__(t, regular_expression, portray, inside):
            assert inside.repeatable

            t.regular_expression = regular_expression
            t.portray            = portray
            t.inside             = inside


        def __repr__(t):
            return arrange('<TremoliteParenthesis %s %r>', portray_string(t.regular_expression), t.inside)


    class TremoliteRepeat(TremoliteBase):
        __slots__ = ((
            'repeated',                 #   String
        ))


        repeatable = false
        singular   = true


        def __init__(t, regular_expression, portray, repeated):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.repeated           = repeated


        def __repr__(t):
            return arrange('<TremoliteRepeat %s %r>', portray_string(t.regular_expression), t.repeated)


    class TremoliteSpecial(TremoliteBase):
        __slots__ = ((
            'repeatable',               #   Boolean
            'singular',                 #   Boolean
        ))


        def __init__(t, regular_expression, portray, repeatable, singular):
            t.regular_expression = intern_string(regular_expression)
            t.portray            = intern_string(portray)
            t.repeatable         = repeatable
            t.singular           = singular


        def __repr__(t):
            if t.repeatable:
                if t.singular:
                    suffix = '; repeatable & singular'
                else:
                    suffix = '; repeatable'
            else:
                if t.singular:
                    suffix = '; singular'                   #   Can't happen -- here for completeness
                else:
                    suffix = ''

            return arrange('<TremoliteSpecial %s %s%s>', portray_string(t.regular_expression), t.portray, suffix)


    def create_exact(s):
        assert length(s) >= 1

        many   = []
        append = many.append

        for c in s:
            a = lookup_ascii(c)

            if not a.is_printable:
                raise_runtime_error('invalid character <%s> passed to EXACT(%s)', portray_string(c), portray_string(s))

            append(a.pattern)

        return intern_string(''.join(many))


    def create_repeat(name, inside, m, n, question_mark = ''):
        if type(inside) is String:
            inside = INVISIBLE_EXACT(inside)
        else:
            assert inside.repeatable

        prefix = (inside.regular_expression   if inside.singular else   '(?:' + inside.regular_expression + ')')

        if n is none:
            assert m >= 2

            return TremoliteRepeat(
                       intern_arrange('%s{%d}%s', suffix, m, question_mark),
                       arrange('%s(%s, %d)', name, inside, m),
                       inside,
                   )

        if n == -7:
            assert m >= 0

            if m is 0:
                suffix = arrange('{,}%s', question_mark)
            else:
                suffix = arrange('{%d,}%s', m, question_mark)

            return TremoliteRepeat(
                       intern_string(prefix + suffix),
                       arrange('%s(%s, %d)', name, inside, m),
                       inside,
                   )

        assert 0 <= m < n

        if m is 0:
            suffix = arrange('{,%d}%s', n, question_mark)
        else:
            suffix = arrange('{%d,%d}%s', m, n, question_mark)

        return TremoliteRepeat(
                   intern_string(prefix + suffix),
                   arrange('%s(%s, %d, %d)', name, inside, m, n),
                   inside,
               )


    def create_simple_repeat(name, inside, suffix):
        if type(inside) is String:
            inside = INVISIBLE_EXACT(inside)
        else:
            assert inside.repeatable

        return TremoliteRepeat(
                   (
                       intern_string(inside.regular_expression + suffix)
                           if inside.singular else
                               intern_arrange('(?:%s)%s', inside.regular_expression, suffix)
                   ),
                   arrange('%s(%s)', name, inside),
                   inside,
               )


    def wrap_parenthesis(inside, invisible = false):
        assert not inside.singular

        return TremoliteParenthesis(
                   intern_arrange('(?:%s)', inside.regular_expression),
                   (inside.portray   if invisible else   intern_arrange('(%s)', inside.portray)),
                   inside,
               )


    @export
    def ANY_OF(*arguments):
        assert length(arguments) > 0

        many   = ['[']
        append = many.append

        for s in arguments:
            if length(s) is 1:
                assert lookup_ascii(s).is_printable

                many.append(s)
            else:
                assert (length(s) is 3) and (s[1] is '-')

                a0 = lookup_ascii(s[0])
                a2 = lookup_ascii(s[2])

                if not a0.is_printable:
                    raise_runtime_error('invalid character <%s> passed to ANY_OF(%s)', portray_string(s[0]), portray_string(s))

                if not a2.is_printable:
                    raise_runtime_error('invalid character <%s> passed to ANY_OF(%s)', portray_string(s[2]), portray_string(s))

                many.append(a0.pattern + '-' + a2.pattern)

        many.append(']')

        return TremoliteAnyOf(
                   intern_string(''.join(many)),
                   intern_arrange('ANY_OF(%s)', ', '.join(portray_string(s)   for s in arguments)),
                   Tuple(intern_string(s)   for s in arguments)
               )


    @export
    def EXACT(s):
        assert length(s) >= 1

        return TremoliteExact(
                   create_exact(s), intern_arrange('EXACT(%s)', portray_string(s)), intern_string(s), length(s) is 1,
               )


    @export
    def GROUP(group_name, inside):
        if type(inside) is String:
            inside = INVISIBLE_EXACT(inside)

        if group_name_match(group_name) is none:
            raise_runtime_error('GROUP: invalid group name: %s (expected a python identifier)', group_name)

        return TremoliteGroup(
                   intern_arrange('(?P<%s>%s)', group_name, inside.regular_expression),
                   arrange('GROUP(%s, %s)', portray_string(group_name), inside),
                   group_name,
                   inside,
               )


    @export
    def INVISIBLE_EXACT(s):
        assert (type(s) is String) and (length(s) >= 1)

        return TremoliteExact(
                   create_exact(s), intern_string(portray_string(s)), intern_string(s), length(s) is 1,
               )


    @export
    def MINIMUM_OF_ONE_OR_MORE(inside):
        return create_simple_repeat('MINIMUM_OF_ONE_OR_MORE', inside, '+?')


    @export
    def MINIMUM_OF_OPTIONAL(inside):
        return create_simple_repeat('MINIMUM_OF_OPTIONAL', inside, '??')


    @export
    def MINIMUM_OF_REPEAT(inside, m, n = none):
        return create_repeat('MINIMUM_OF_REPEAT', inside, m, n, '?')


    @export
    def MINIMUM_OF_REPEAT_OR_MORE(inside, m):
        return create_repeat('MINIMUM_OF_REPEAT_OR_MORE', inside, m, -7, '?')


    @export
    def MINIMUM_OF_ZERO_OR_MORE(inside):
        return create_simple_repeat('MINIMUM_OF_ZERO_OR_MORE', inside, '*?')


    @export
    def ONE_OR_MORE(inside):
        return create_simple_repeat('ONE_OR_MORE', inside, '+')


    @export
    def OPTIONAL(inside):
        return create_simple_repeat('OPTIONAL', inside, '?')


    @export
    def REPEAT_OR_MORE(inside, m):
        return create_repeat('REPEAT_OR_MORE', inside, m, -7)


    @export
    def REPEAT(inside, m, n = none):
        return create_repeat('REPEAT', inside, m, n)


    def SPECIAL(regular_expression, portray, repeatable = false, singular = false):
        if not repeatable:
            assert not singular

        return TremoliteSpecial(intern_string(regular_expression), intern_string(portray), repeatable, singular)


    @export
    def ZERO_OR_MORE(inside):
        return create_simple_repeat('ZERO_OR_MORE', inside, '*')


    export(
        'EMPTY',            SPECIAL('',    'EMPTY'),
        'END_OF_PATTERN',   SPECIAL(r'\Z', 'END_OF_PATTERN'),
    )
