#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.Import')
def gem():
    #
    #   Python values
    #
    python_modules = PythonSystem.modules


    #
    #   import_module
    #
    if is_python_2:
        @export
        def import_module(module_name):
            module_name = intern_string(module_name)

            __import__(module_name)

            return python_modules[module_name]
    else:
        PythonImportLibrary = __import__('importlib')

        import_module = PythonImportLibrary.import_module


        #
        #   NOTE:
        #       Do not use 'export(import_module)' as this will *CHANGE* it's global scope to be
        #       GEM's scope -- which fails miserably since it can't find '_bootstrap' in the Gem scope.
        #
        #       Instead use two arguments, so its export without having its global scope changed.
        #
        export(
            'import_module',    import_module,
        )


    if is_python_2:
        PythonOldImport = import_module('imp')
        find_module     = PythonOldImport.find_module
        load_module     = PythonOldImport.load_module


        dot_path = ['.']


        @export
        def find_and_execute_module__or__none(module_name):
            module_name = intern_string(module_name)

            with catch_ImportError() as e:
                [f, pathname, description] = find_module(module_name, dot_path)

            if e.caught is not none:
                return none

            #
            #   CAREFUL here:
            #       We *MUST* close 'f' if any exception is thrown.
            #
            #       So ASAP use 'f' within a 'with' clause (this ensures 'f' is always closed, whether
            #       an exception is thrown or not)
            #
            if f is not none:
                with f:
                    module = load_module(module_name, f, pathname, description)
            else:
                module = load_module(module_name, f, pathname, description)

            #
            #   discard the module, it is no longer needed
            #
            del python_modules[module_name]

            return module


    else:
        #
        #   Can't use import_module on importlib.*, due to internal limitations of importlib.
        #
        PythonImportMachinery            = import_module('importlib.machinery')
        PythonImportUtility              = import_module('importlib.util')
        lookup_module_blueprint__by_path = PythonImportMachinery.PathFinder.find_spec
        create_module_from_blueprint     = PythonImportUtility.module_from_spec

        print(import_module('os.path'))


        @export
        def find_and_execute_module__or__none(module_name):
            module_name = intern_string(module_name)

            blueprint = lookup_module_blueprint__by_path(module_name, '.')

            if blueprint is none:
                return none

            module = create_module_from_blueprint(blueprint)

            blueprint.loader.exec_module(module)

            return module


    if 0:
        export(
            'python_modules',       python_modules,
        )
