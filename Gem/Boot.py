#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#


def gem(module_name):
    def execute(f):
        return f()

    return execute


@gem('Gem.Boot')
def gem():
    #
    #   This really belongs in Gem.Core, but is here since we need it during Boot
    #
    PythonSystem = __import__('sys')
    is_python_2   = PythonSystem.version_info.major is 2
    PythonCore    = __import__('__builtin__'  if is_python_2 else   'builtins')


    #
    #   Python keywords
    #
    none = None

    #
    #   Python Functions
    #
    intern_string = (PythonCore   if is_python_2 else   PythonSystem).intern
    iterate       = PythonCore.iter
    length        = PythonCore.len


    #
    #   Python types
    #
    Module    = PythonCore.__class__
    LiquidSet = PythonCore.set
    String    = PythonCore.str


    #
    #   Python methods
    #
    python_modules      = PythonSystem.modules
    store_python_module = python_modules.__setitem__


    #
    #   Gem
    #       Replace the index in python_modules & also Gem.__name__ with an intern'ed copy of 'Gem'.
    #
    Gem          = python_modules['Gem']
    Gem.__name__ = Gem_name              = intern_string(Gem.__name__)
    gem_scope    = Gem.__dict__

    store_python_module(Gem_name, Gem)


    #
    #   boot
    #
    def boot():
        del Gem.Boot
        del python_modules['Gem.Boot']


    #
    #   export
    #       Exports a function to Gem (Global Execution Module); also the actual function exported
    #       is a copy of the original function -- but with its global scope replaced to be Gem's scope.
    #
    #       Can also be used with multiple arguments to export a list of values (no replacement of
    #       global scope's is done in this case).
    #
    Function = boot.__class__

    if is_python_2:
        function_closure  = Function.func_closure .__get__
        function_code     = Function.func_code    .__get__
        function_defaults = Function.func_defaults.__get__
    else:
        function_closure  = Function.__closure__ .__get__
        function_code     = Function.__code__    .__get__
        function_defaults = Function.__defaults__.__get__

    function_name = Function.__dict__['__name__'].__get__


    def localize(f):
        return Function(
                   function_code(f),
                   gem_scope,                               #   Replace global scope with Gem's scope
                   function_name(f),
                   function_defaults(f),
                   function_closure(f),
               )


    #
    #   Strickly speaking:
    #
    #       We don't really need to localize ourselves ...
    #       (since is never exported or referenced once this function finishes)
    #
    #   However ... might as well ...
    #
    localize = localize(localize)                           #   Localize ourselves :)


    if __debug__:
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonCore)
        NameError       = PythonException.NameError


        @localize
        def arrange(format, *arguments):
            return format % arguments


        @localize
        def forge_export(module):
            module_name    = module.__name__
            module_scope   = module.__dict__
            provide_export = module_scope.setdefault


            def already_exists(name, previous, exporting):
                name_error = arrange("%s.%s already exists (value: %r): can't export %r also",
                                     module_name, name, previous, exporting)

                raise NameError(name_error)


            def export(f, *arguments):
                if length(arguments) is 0:
                    if type(f) is Function:
                        name = function_name(f)

                        exporting = Function(
                                        function_code(f),
                                        module_scope,           #   Replace global scope with module's scope
                                        name,
                                        function_defaults(f),
                                        function_closure(f),
                                    )

                        previous = provide_export(name, exporting)

                        if previous is not exporting:
                            already_exists(name, previous, exporting)

                        return exporting

                    previous = provide_export(f.__name__, f)

                    if previous is not f:
                        already_exists(f.__name__, previous, f)

                    return f

                argument_iterator = iterate(arguments)
                next_argument     = next_method(argument_iterator)

                assert f.__class__ is String

                exporting = next_argument()
                previous  = provide_export(f, exporting)

                if previous is not exporting:
                    already_exists(f, previous, exporting)

                for name in argument_iterator:
                    assert name.__class__ is String

                    exporting = next_argument()
                    previous  = provide_export(name, exporting)

                    if previous is not exporting:
                        already_exists(name, previous, exporting)


            return export


    else:
        @localize
        def forge_export(module):
            module_name    = module.__name__
            module_scope   = module.__dict__
            provide_export = module_scope.setdefault


            def export(f, *arguments):
                if length(arguments) is 0:
                    if type(f) is Function:
                        name = function_name(f)

                        return provide_export(
                                   name,
                                   Function(
                                       function_code(f),
                                       module_scope,           #   Replace global scope with module's scope
                                       name,
                                       function_defaults(f),
                                       function_closure(f),
                                   ),
                               )

                    return provide_export(f.__name__, f)

                argument_iterator = iterate(arguments)
                next_argument     = next_method(argument_iterator)

                assert f.__class__ is String

                provide_export(f, next_argument())

                for name in argument_iterator:
                    assert name.__class__ is String

                    provide_export(name, next_argument())


            return export


    export       = forge_export(Gem)            #   Create export function for Gem
    forge_export = export(forge_export)         #   export forge_export
    export       = export(export)               #   export ourselves :)


    #
    #   next_method
    #       Access the .next method of an iterator
    #
    #       (Deals with the annoyance of .next method named .next in python 2.0, but .__next__ in python 3.0)
    #
    if is_python_2:
        @export
        def next_method(iterator):
            return iterator.next
    else:
        @export
        def next_method(iterator):
            return iterator.__next__


    #
    #   NOTE:
    #       The previous two calls to 'export' did *NOT* have 'next_argument' (used by export) defined ...
    #
    #       That is ok, as they only called 'export' with one argument ... thus not hitting the code path
    #       that uses 'next_argument'
    #
    #       Now that 'next_method' is defined, 'export' can be called with multiple arguments ...
    #


    #
    #   gem
    #
    gem_name = intern_string('gem')


    @export
    def gem(module_gem):
        def execute(f):
            assert f.__name__ == gem_name

            Function(
                function_code(f),
                gem_scope,               #   Replace global scope with Gem's scope
                gem_name,
                function_defaults(f),
                function_closure(f),
            )(
            )

            return gem

        return execute


    #
    #   require_gem
    #
    gem_modules    = LiquidSet()
    add_gem_module = gem_modules.add
    has_gem_module = gem_modules.__contains__

    if is_python_2:
        #
        #   Python 2.0 method of loading a module with 'gem' pre-initialized
        #
        #       This is messy -- see below for the Python 3.0 method which is much cleaner.
        #
        PythonOldImport = __import__('imp')
        find_module     = PythonOldImport.find_module
        load_module     = PythonOldImport.load_module


        @export
        def require_gem(module_name):
            if has_gem_module(module_name):
                return

            module_name = intern_string(module_name)

            add_gem_module(module_name)

            module     = Module(module_name)
            module.gem = gem

            #
            #   Temporarily store our module in 'python_modules[module_name]'.
            #
            #   This is needed in python 2.0, as the way to pass the 'pre-initialized' module to 'load_module'
            #
            #       (In the cleaner python 3.0 version below, we pass the modules directly to 'exec_module'
            #       and thus do not need to store the module in 'python_modules[module_name]').
            #
            #   NOTE:
            #       If this was real import implementation we would need to cleanup
            #       'python_modules[module_name]' When an exception is thrown.
            #
            #       However, this is not a true import mechanism.  If it fails, our program will simply
            #       exit.
            #
            #       Therefore, there is no 'try' clause below to cleanup if 'load_module' throws ImportError
            #
            store_python_module(module_name, module)

            dot_index = module_name.rfind('.')

            if dot_index is -1:
                [f, pathname, description] = find_module(module_name)
            else:
                [f, pathname, description] = find_module(
                                                 module_name[dot_index + 1:],
                                                 python_modules[module_name[:dot_index]].__path__,
                                             )

            #
            #   CAREFUL here:
            #       We *MUST* close 'f' if any exception is thrown.
            #
            #       So ASAP use 'f' within a 'with' clause (this ensures 'f' is always closed, whether
            #       an exception is thrown or not)
            #
            if f is not none:
                with f:
                    load_module(module_name, f, pathname, description)
            else:
                load_module(module_name, f, pathname, description)

            #
            #   discard the module, it is no longer needed
            #
            del python_modules[module_name]


    else:
        #
        #   Python 3.0 method of loading a module with 'gem' pre-initialized
        #
        PythonImportUtility          = __import__('importlib.util').util
        ImportError                  = PythonCore.ImportError
        lookup_module_blueprint      = PythonImportUtility.find_spec
        create_module_from_blueprint = PythonImportUtility.module_from_spec


        @export
        def require_gem(module_name):
            if has_gem_module(module_name):
                return

            module_name = intern_string(module_name)

            add_gem_module(module_name)

            blueprint = lookup_module_blueprint(module_name)

            if blueprint is none:
                raise ImportError("Can't find module %s" % module_name)

            module     = create_module_from_blueprint(blueprint)
            module.gem = gem

            blueprint.loader.exec_module(module)


    require_gem('Gem.Core')


    #
    #   main
    #
    Main = python_modules['__main__']


    @localize
    def main(module_name):
        assert module_name == 'Main'


        def export(f):
            assert f.__name__ == 'main'

            del Main.export

            return forge_export(Main)(f)


        def execute(f):
            assert f.__name__ == 'main'

            f()

            Main.main()


        del Main.boot
        del Main.main

        Main.export      = export
        Main.require_gem = require_gem

        return execute


    Gem .boot = boot
    Main.main = main
