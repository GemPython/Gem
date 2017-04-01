#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Tremolite.Match')
def gem():
    require_gem('Tremolite.Build')
    require_gem('Tremolite.Core')


    class TremoliteMatch(Object):
        __slots__ = ((
            'name',                     #   String
            'pattern',                  #   TremoliteBase+
        ))


        def __init__(t, name, pattern):
            t.name    = name
            t.pattern = pattern


        def __repr__(t):
            return arrange('<TremoliteMatch %s %r>', t.name, t.pattern)


    [cache, insert] = produce_cache_and_insert_function('tremolite.match')


    @export
    def MATCH(name, pattern):
        assert (type(name) is String) and (length(name) > 0)

        if type(pattern) is String:
            pattern = INVISIBLE_EXACT(pattern)

        name = intern_string(name)

        return insert(name, TremoliteMatch(name, pattern))


    @export
    def create_match_code(path, copyright, module_name):
        notice        = []
        append_notice = notice.append
        found         = 0

        for s in read_text_from_path('../Tremolite/LicenseTemplate.txt').splitlines():
            if s == '#':
                found = 1
            elif s == '<generated-output-goes-here />':
                found = 2

            if found is 1:
                append_notice(s)

        with create_DelayedFileOutput(path) as f:
            f.line('#')
            f.line('#   Copyright %s.  All rights reserved.', copyright)
            f.line('#')
            f.line('@gem(%r)', module_name)
            
            with f.indent('def gem():'):
                f.line('require_gem(%r)', 'Gem.System')
                f.line('require_gem(%r)', 'Tremolite.Compile')
                f.blank2()
                f.line('from Gem import python_version')
                f.line('from Tremolite import compile_regular_expression')
                f.blank2()

                with f.indent(arrange('if python_version == %s:', portray_string(python_version))):
                    with f.indent('C = ((', ')).__getitem__'):
                        for s in notice:
                            f.line(s)

                        f.line('0,')

                        for v in iterate_values_sorted_by_key(cache):
                            [code, groups, flags] = parse_ascii_regular_expression(v.pattern.regular_expression)

                            f.blank()
                            f.line('#')
                            f.line('#   %s', portray_string(v.pattern.regular_expression))
                            f.line('#')

                            if type(code) is String:
                                f.line('%s,', portray_string(code))
                            else:
                                with f.indent('((', ')),'):
                                    data     = none
                                    position = 0

                                    for w in code:
                                        if (is_python_2) and (type(w) is Long):
                                            s = arrange('Long(%d)', w)
                                        else:
                                            s = arrange('%d', w)

                                        s_total = length(s)

                                        if (position is not 0) and (position + s_total + 2) > 120:
                                            f.line(data)
                                            position = 0

                                        if position is 0:
                                            data     = s + ','
                                            position = f.prefix_total + s_total + 1
                                        else:
                                            data     += ' ' + s + ','
                                            position += 1 + s_total + 1

                                    f.line(data)

                            if groups is not 0:
                                f.line('%s,', portray(groups))

                            if flags is not 0:
                                f.line('%d,', flags)

                        f.line('#</copyright>')

                    f.blank2()

                    with f.indent('def M(regular_expression, code, groups = 0, flags = 0):'):
                        f.line('return compile_regular_expression(regular_expression, C(code), C(groups), C(flags)).match')

                f.blank2()

                with f.indent('else:'):
                    f.line('require_gem(%r)', 'Tremolite.Parse')
                    f.blank2()
                    f.line('from Tremolite import parse_ascii_regular_expression')
                    f.blank2()

                    with f.indent('def M(regular_expression, code, groups = 0, flags = 0):'):
                        with f.indent('return compile_regular_expression(', ').match'):
                            f.line('regular_expression,')
                            f.line('*parse_ascii_regular_expression(regular_expression)#,')

                f.blank2()

                index = 1

                for v in iterate_values_sorted_by_key(cache):
                    [code, groups, flags] = parse_ascii_regular_expression(v.pattern.regular_expression)

                    f.blank()
                    f.line('#')
                    f.line('#   %s', v.name)
                    f.line('#')
                    f.line('#       %s', v.pattern)
                    f.line('#')

                    with f.indent(
                            arrange('%s = M(', v.name),
                            ')',
                    ):
                        f.line('%s,', portray_string(v.pattern.regular_expression))
                        f.line('%d,', index)
                        index += 1

                        if groups is not 0:
                            f.line('%d,', index)
                            index += 1
                        elif flags is not 0:
                            f.line('0,')

                        if flags is not 0:
                            f.line('%d,', index)
                            index += 1

                f.blank2()

                total = maximum(length(v.name)    for v in iterate_values_sorted_by_key(cache))
                total = (total + 8) &~ 3

                with f.indent(
                    'export(',
                    ')',
                ):
                    for v in iterate_values_sorted_by_key(cache):
                        f.line('%*s%s,', -total, arrange('%r,', v.name), v.name)

            data = f.finish()

        if 0:
            for s in data.splitlines():
                line(s)
