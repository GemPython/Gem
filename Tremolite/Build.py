#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Build')
def gem():
    require_gem('Tremolite.Core')
    require_gem('Tremolite.Compile')
    require_gem('Tremolite.Parse')
    require_gem('Tremolite.Match')


    show = false


    #
    #   TremoliteBase
    #       TremoliteExact
    #       TremoliteGroupBase
    #           TremoliteGroup
    #           TremoliteName
    #           TremoliteNamedGroup
    #           TremoliteOptionalGroup
    #       TremoliteMany
    #           TremoliteAdd
    #           TremoliteAnyOf
    #           TremoliteOr
    #       TremoliteOne
    #           TremoliteParenthesis
    #           TremoliteRepeat
    #       TremoliteSpecial
    #
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


    class TremoliteGroupBase(TremoliteBase):
        __slots__ = ((
            'name',                     #   String
            'pattern',                  #   String
        ))


        def __init__(t, regular_expression, portray, name, pattern):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.name               = name
            t.pattern            = pattern


        def __repr__(t):
            return arrange('<%s %s %r>', t.__class__.__name__, t.name, t.pattern)


    class TremoliteGroup(TremoliteGroupBase):
        __slots__ = (())


        repeatable = true
        singular   = true


    class TremoliteName(TremoliteGroupBase):
        __slots__ = (())


        def __init__(t, name, pattern):
            t.regular_expression = pattern.regular_expression
            t.portray            = t.name = name
            t.pattern            = pattern


        @property
        def repeatable(t):
            return t.pattern.repeatable


        @property
        def singular(t):
            return t.pattern.singular


    class TremoliteNamedGroup(TremoliteGroupBase):
        __slots__ = (())


        @property
        def repeatable(t):
            return t.pattern.repeatable


        singular = repeatable


    class TremoliteOptionalGroup(TremoliteGroupBase):
        __slots__ = (())


        repeatable = false
        singular   = false


    class TremoliteMany(TremoliteBase):
        __slots__ = ((
            'many',                     #   Tuple of TremoliteBase+
        ))


        repeatable = true


        def __init__(t, regular_expression, portray, many):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.many               = many


        def __repr__(t):
            return arrange('<%s %s %s>',
                           t.__class__.__name__,
                           portray_string(t.regular_expression),
                           ' '.join((portray_string(v)   if type(v) is String else   portray(v))  for v in t.many))


    class TremoliteAdd(TremoliteMany):
        __slots__ = (())


        singular = false


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


    class TremoliteAnyOf(TremoliteMany):
        __slots__ = (())


        singular = true


        def __repr__(t):
            return arrange('<TremoliteAnyOf %s %s>',
                           portray_string(t.regular_expression),
                           ' '.join(portray_string(v)  for v in t.many))


    class TremoliteOr(TremoliteMany):
        __slots__ = (())


        is_tremolite_or = true
        singular        = false


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


    class TremoliteOne(TremoliteBase):
        __slots__ = ((
            'pattern',                  #   String
        ))


        def __init__(t, regular_expression, portray, pattern):
            t.regular_expression = regular_expression
            t.portray            = portray
            t.pattern            = pattern


        def __repr__(t):
            return arrange('<%s %s %r>', t.__class__.__name__, portray_string(t.regular_expression), t.pattern)


    class TremoliteNotFollowedBy(TremoliteOne):
        __slots__ = (())


        repeatable = false
        singular   = true


    class TremoliteParenthesis(TremoliteOne):
        __slots__ = (())


        repeatable = true
        singular   = true


        def __init__(t, regular_expression, portray, pattern):
            assert pattern.repeatable

            t.regular_expression = regular_expression
            t.portray            = portray
            t.pattern            = pattern


    class TremoliteRepeat(TremoliteOne):
        __slots__ = (())


        repeatable = false
        singular   = true


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


    [name_cache, name_insert] = produce_cache_functions('Tremolite.name_cache', produce_cache = true, produce_insert = true)


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


    def create_repeat(name, pattern, m, n, question_mark = ''):
        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)
        else:
            assert pattern.repeatable

        prefix = (pattern.regular_expression   if pattern.singular else   '(?:' + pattern.regular_expression + ')')

        if n is none:
            assert m >= 2

            return TremoliteRepeat(
                       intern_arrange('%s{%d}%s', suffix, m, question_mark),
                       arrange('%s(%s, %d)', name, pattern, m),
                       pattern,
                   )

        if n == -7:
            assert m >= 0

            if m is 0:
                suffix = arrange('{,}%s', question_mark)
            else:
                suffix = arrange('{%d,}%s', m, question_mark)

            return TremoliteRepeat(
                       intern_string(prefix + suffix),
                       arrange('%s(%s, %d)', name, pattern, m),
                       pattern,
                   )

        assert 0 <= m < n

        if m is 0:
            suffix = arrange('{,%d}%s', n, question_mark)
        else:
            suffix = arrange('{%d,%d}%s', m, n, question_mark)

        return TremoliteRepeat(
                   intern_string(prefix + suffix),
                   arrange('%s(%s, %d, %d)', name, pattern, m, n),
                   pattern,
               )


    def create_simple_repeat(name, pattern, suffix):
        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)
        else:
            assert pattern.repeatable

        return TremoliteRepeat(
                   (
                       intern_string(pattern.regular_expression + suffix)
                           if pattern.singular else
                               intern_arrange('(?:%s)%s', pattern.regular_expression, suffix)
                   ),
                   arrange('%s(%s)', name, pattern),
                   pattern,
               )


    def wrap_parenthesis(pattern, invisible = false):
        assert not pattern.singular

        return TremoliteParenthesis(
                   intern_arrange('(?:%s)', pattern.regular_expression),
                   (pattern.portray   if invisible else   intern_arrange('(%s)', pattern.portray)),
                   pattern,
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
    def GROUP(name, pattern):
        if name_match(name) is none:
            raise_runtime_error('GROUP: invalid group name: %s (expected a python identifier)', name)

        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        return TremoliteGroup(
                   intern_arrange('(?P<%s>%s)', name, pattern.regular_expression),
                   arrange('GROUP(%s, %s)', portray_string(name), pattern),
                   name,
                   pattern,
               )


    @export
    def INVISIBLE_EXACT(s):
        assert (type(s) is String) and (length(s) >= 1)

        return TremoliteExact(
                   create_exact(s), intern_string(portray_string(s)), intern_string(s), length(s) is 1,
               )


    @export
    def MINIMUM_OF_ONE_OR_MORE(pattern):
        return create_simple_repeat('MINIMUM_OF_ONE_OR_MORE', pattern, '{1,7777777}?')


    @export
    def MINIMUM_OF_OPTIONAL(pattern):
        return create_simple_repeat('MINIMUM_OF_OPTIONAL', pattern, '??')


    @export
    def MINIMUM_OF_REPEAT(pattern, m, n = none):
        return create_repeat('MINIMUM_OF_REPEAT', pattern, m, n, '?')


    @export
    def MINIMUM_OF_REPEAT_OR_MORE(pattern, m):
        return create_repeat('MINIMUM_OF_REPEAT_OR_MORE', pattern, m, 7777777, '?')


    @export
    def MINIMUM_OF_ZERO_OR_MORE(pattern):
        return create_simple_repeat('MINIMUM_OF_ZERO_OR_MORE', pattern, '{,7777777}?')


    @export
    def NAME(name, pattern):
        if name_match(name) is none:
            raise_runtime_error('NAME: invalid name: %s (expected a python identifier)', name)

        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        name = intern_string(name)

        return name_insert(name, TremoliteName(name, pattern))


    @export
    def NAMED_GROUP(name, pattern):
        if name_match(name) is none:
            raise_runtime_error('NAMED_GROUP: invalid name: %s (expected a python identifier)', name)

        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        name = intern_string(name)

        return name_insert(
                   name,
                   TremoliteNamedGroup(
                       intern_arrange('(?P<%s>%s)', name, pattern.regular_expression),
                       name,
                       name,
                       GROUP(name, pattern),
                   ),
               )


    @export
    def NOT_FOLLOWED_BY(pattern):
        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        return TremoliteNotFollowedBy(
                   intern_arrange('(?!%s)', pattern.regular_expression),
                   intern_arrange('NOT_FOLLOWED_BY(%s)', pattern.portray),
                   pattern,
               )


    @export
    def ONE_OR_MORE(pattern):
        return create_simple_repeat('ONE_OR_MORE', pattern, '{1,7777777}')


    @export
    def OPTIONAL(pattern):
        return create_simple_repeat('OPTIONAL', pattern, '?')


    @export
    def OPTIONAL_GROUP(group_name, pattern):
        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)
        else:
            assert pattern.repeatable

        if name_match(group_name) is none:
            raise_runtime_error('GROUP: invalid group name: %s (expected a python identifier)', group_name)

        return TremoliteOptionalGroup(
                   intern_arrange('(?P<%s>%s)?', group_name, pattern.regular_expression),
                   arrange('OPTIONAL_GROUP(%s, %s)', portray_string(group_name), pattern),
                   group_name,
                   pattern,
               )


    #
    #<PRINTABLE_MINUS>
    #
    def raise_invalid_printable_minus_character(c, s):
        raise_runtime_error('invalid character <%s> passed to PRINTABLE_MINUS(%s)',
                            portray_string(c), portray_string(s))


    def raise_already_not_allowed_printable_minus_character(c, s):
        raise_runtime_error('character %r already not allowed in PRINTABLE_MINUS(%s)',
                            portray_string(c), portray_string(s))


    ordinal_space = ordinal(' ')
    ordinal_minus = ordinal('-')
    ordinal_tilde = ordinal('~')


    @export
    def PRINTABLE_MINUS(*arguments):
        assert length(arguments) > 0

        valid = [ordinal_space <= i <= ordinal_tilde   for i in iterate_range(0, 256)]

        for s in arguments:
            if length(s) is 1:
                a = lookup_ascii(s, unknown_ascii)

                if not a.is_printable:
                    raise_invalid_printable_minus_character(s, s)

                if not valid[a.ordinal]:
                    raise_already_not_allowed_printable_minus_character(s, s)

                valid[a.ordinal] = false
                continue

            assert (length(s) is 3) and (s[1] is '-')

            a0 = lookup_ascii(s[0], unknown_ascii)
            a2 = lookup_ascii(s[2], unknown_ascii)

            if not a0.is_printable:
                raise_invalid_printable_minus_character(s[0], s)

            if not a2.is_printable:
                raise_invalid_printable_minus_character(s[2], s)

            if a0.ordinal > a2.ordinal:
                raise_runtime_error('invalid backwards range PRINTABLE_MINUS(%s)', portray_string(s))

            for i in iterate_range(a0.ordinal, a2.ordinal):
                if not valid[i]:
                    raise_already_not_allowed_printable_minus_character(character(i), s)

                valid[i] = false

        many   = ['[']
        append = many.append
        lowest = none


        def add_range(lowest, highest):
            if show:
                line('add_range(%d, %d)', lowest, highest)

            if lowest == ordinal_minus:
                many.insert(0, '-')
                lowest += 1

            if highest == ordinal_minus:
                many.insert(0, '-')
                highest -= 1

            if lowest == highest:
                many.append(lookup_ascii(lowest).pattern)
                return

            if lowest > highest:
                return

            many.append(arrange('%s-%s', lookup_ascii(lowest).pattern, lookup_ascii(highest).pattern))


        for i in iterate_range(0, 256):
            if valid[i]:
                if lowest is none:
                    lowest = i
                    continue
            else:
                if lowest is not none:
                    add_range(lowest, i - 1)
                    lowest = none
        else:
            if lowest is not none:
                add_range(lowest, 255)

        many.append(']')

        return TremoliteAnyOf(
                   intern_string(''.join(many)),
                   intern_arrange('PRINTABLE_MINUS(%s)', ', '.join(portray_string(s)   for s in arguments)),
                   Tuple(intern_string(s)   for s in arguments)
               )
    #</PRINTABLE_MINUS>


    @export
    def REPEAT_OR_MORE(pattern, m):
        return create_repeat('REPEAT_OR_MORE', pattern, m, 7777777)


    @export
    def REPEAT(pattern, m, n = none):
        return create_repeat('REPEAT', pattern, m, n)


    def SPECIAL(regular_expression, portray, repeatable = false, singular = false):
        if not repeatable:
            assert not singular

        return TremoliteSpecial(intern_string(regular_expression), intern_string(portray), repeatable, singular)


    @export
    def ZERO_OR_MORE(pattern):
        return create_simple_repeat('ZERO_OR_MORE', pattern, '{,7777777}')


    share(
        'name_cache',       name_cache,
    )


    export(
        'BACKSLASH',        SPECIAL(r'\\',          'BACKSLASH',    repeatable = true, singular = true),
        'DOT',              SPECIAL('.',            'DOT',          repeatable = true, singular = true),
        'EMPTY',            SPECIAL('(?#empty)',    'EMPTY'),
        'END_OF_PATTERN',   SPECIAL(r'\Z',          'END_OF_PATTERN'),
        'LINEFEED',         SPECIAL(r'\n',          'LINEFEED',     repeatable = true, singular = true),
        'PRINTABLE',        SPECIAL('[ -~]',        'PRINTABLE',    repeatable = true, singular = true),
    )
