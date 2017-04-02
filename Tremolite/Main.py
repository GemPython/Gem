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
    require_gem('Tremolite.Core')
    require_gem('Tremolite.Name')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.CreateMatch')


    @share
    def main():
        identifier = NAME('identifier', ANY_OF('A-Z', '_', 'a-z') + ZERO_OR_MORE(ANY_OF('0-9', 'A-Z', '_', 'a-z')))

        #MATCH('test', PRINTABLE_MINUS("'", '\\'))

        FULL_MATCH('name_match', identifier)
        create_match_code('../Tremolite/Match.gpy', '2017 Amit Green', 'Tremolite.Match')
