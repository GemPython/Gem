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
        @built_in
        def import_module(module_name):
            module_name = intern_string(module_name)

            __import__(module_name)

            return python_modules[module_name]
    else:
        PythonImportLibrary = __import__('importlib')

        import_module = PythonImportLibrary.import_module


        #
        #   NOTE:
        #       Do not use 'built_in(import_module)' as this will *CHANGE* it's global scope to be
        #       Gem's shared scope -- which fails miserably since it can't find '_bootstrap' in the Gem scope.
        #
        #       Instead use two arguments, so its exported without having its global scope changed.
        #
        built_in(
            'import_module',    import_module,
        )
