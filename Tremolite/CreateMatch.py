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

        for s in read_text_from_path('../Tremolite/Parse.py').splitlines():
            if s == '        #<copyright>':
                found = 3
            elif s[:9] != '        #':
                found = 0
            elif found > 1:
                found -= 1

            if found is 1:
                append_notice(s[8:])

        with create_DelayedFileOutput(path) as f:
            f.line('#')
            f.line('#   Copyright %s.  All rights reserved.', copyright)
            f.line('#')
            f.line('@gem(%r)', module_name)
            
            with f.indent('def gem():'):
                f.line('require_gem(%r)', 'Tremolite.Compile')
                f.blank2()
                f.line('from Tremolite import compile_regular_expression')

                f.blank2()
                with f.indent('def M(regular_expression, code, groups = 0, flags = 0):'):
                    f.line('return compile_regular_expression(regular_expression, code, groups, flags).match')
                f.blank2()

                with f.indent('C = (', ').__getitem__'):
                    f.line('#')
                    f.line('#<copyright>')
                    f.line("#   The following is produced from python's standard library")
                    f.line("#   'sre_compile.py', function 'compile' and is thus:")

                    for s in notice:
                        f.line(s)

                    for v in iterate_values_sorted_by_key(cache):
                        [code, groups, flags] = parse_ascii_regular_expression(v.pattern.regular_expression)

                        f.blank()
                        f.line('#')
                        f.line('#   %s', portray_string(v.pattern.regular_expression))
                        f.line('#')
                        f.line('%s,', portray_string(code)   if type(code) is String else   portray(code))

                        if groups is not 0:
                            f.line('%s,', portray(groups))

                        if flags is not 0:
                            f.line('%d,', flags)

                    f.blank()
                    f.line('#</copyright>')

                index = 0

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
                        f.line('C(%d),', index)
                        index += 1

                        if groups is not 0:
                            f.line('C(%d),', index)
                            index += 1
                        elif flags is not 0:
                            f.line('0,')

                        if flags is not 0:
                            f.line('C(%d),', index)
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

        for s in data.splitlines():
            line(s)
