#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Import')
def gem():
    require_gem('Gem.CatchException')


    PythonImport = __import__('imp')
    find_module  = PythonImport.find_module
    load_module  = PythonImport.load_module


    @export
    def find_and_import_module__or__none(name, path = none):
        with catch_ImportError() as e:
            [f, pathname, description] = find_module(name, path)

        if e.caught is not none:
            return none

        if f is none:
            return load_module(name, f, pathname, description)

        with f:
            return load_module(name, f, pathname, description)
