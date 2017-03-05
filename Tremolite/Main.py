#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
def boot(module_name):
    def execute(f):
        return f()

    return execute


@boot('Boot')
def boot():
    from sys     import path    as module_path
    from os.path import abspath as path_absolute, join as path_join

    module_path.insert(1, path_absolute(path_join(module_path[0], '..')))


    import Gem


@gem('Tremolite.Main')
def gem():
    require_gem('Gem.PortrayString')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.Compile')
    require_gem('Tremolite.Parse')


    from Gem import portray_raw_string


    @share
    def main():
        for [regular_expression, test] in [
                [   r'x\Z',                     'x'         ],
                [   r'x(?P<abc>y)\Z',           'xy'        ],
                [   r'x(?P<abc>y)(?P<z>z)\Z',   'xyz'       ],
        ]:
            parsed   = parse_ascii_regular_expression(regular_expression)
            compiled = compile_regular_expression(regular_expression, parsed)
            #m        = compiled.match(test)

            line('%s:', portray_raw_string(regular_expression))
            line('  %r', parsed)
            #line('  %r %r', m.group(), m.groups())
