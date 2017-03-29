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
    require_gem('Tremolite.Parse')


    from Tremolite import parse_regular_expression


    @share
    def main():
        parse_regular_expression('x\Z')
        parse_regular_expression('x(?P<abc>y)\Z')
        parse_regular_expression('x(?P<abc>y)(?P<z>z)\Z')
