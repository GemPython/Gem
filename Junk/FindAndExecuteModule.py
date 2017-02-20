#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Gem.FindAndExecuteModule')
def gem():
    #
    #   Python values
    #
    python_modules = PythonSystem.modules


    if is_python_2:
        PythonOldImport = import_module('imp')
        find_module     = PythonOldImport.find_module
        load_module     = PythonOldImport.load_module


        dot_path = ['.']


        @export
        def find_and_execute_module__or__none(module_name):
            module_name = intern_string(module_name)

            #
            #   CAREFUL here:
            #       We *MUST* close 'f' if any exception is thrown.
            #
            #       So ASAP use 'f' within a 'with' clause (this ensures 'f' is always closed, whether
            #       an exception is thrown or not)
            #
            f = none

            with catch_ImportError() as e:
                [f, pathname, description] = find_module(module_name, dot_path)

            if f is not none:
                with f:
                    module = load_module(module_name, f, pathname, description)
            else:
                #
                #   Check if an exception thrown.  NOTE: Done after the 'with f' above, to make sure
                #   the 'with f' is done ASAP.
                #
                if e:
                    return none

                module = load_module(module_name, f, pathname, description)

            #
            #   discard the module, it is no longer needed
            #
            del python_modules[module_name]

            return module


    else:
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
