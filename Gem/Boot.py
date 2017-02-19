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
    is_python_3   = PythonSystem.version_info.major is 3
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
    Gem       = python_modules['Gem']
    Gem_name  = Gem.__name__ = intern_string(Gem.__name__)
    gem_scope = Gem.__dict__

    store_python_module(Gem_name, Gem)


    #
    #   Gem.Builtin:
    #       The same scope is used for both 'Gem.BuiltIn' & 'privileged_scope'.
    #
    #       'privileged_scope' requires '__builtins__' to be privileged.
    #
    #       On the other hand, '__builtins__' slightly *pollutes* Gem.Builtin.
    #
    #       For now the choice is to accept this, later on they can be spilt
    #
    special_builtins_name = intern_string('__builtins__')
    special_name          = intern_string('__name__')
    privileged_scope      = GemBuiltIn_scope = {
                                                   special_builtins_name : PythonCore.__dict__,
                                                   special_name          : intern_string('Gem.BuiltIn'),
                                               }

    #
    #   Gem.Shared
    #
    GemShared_scope = {
                          special_builtins_name : GemBuiltIn_scope,
                          special_name          : intern_string('Gem.Shared'),
                      }


    #
    #   boot
    #
    def boot():
        del Gem.Boot
        del python_modules['Gem.Boot']


    #
    #   Function
    #
    Function = boot.__class__

    if is_python_2:
        function_closure  = Function.func_closure .__get__
        function_code     = Function.func_code    .__get__
        function_defaults = Function.func_defaults.__get__
        function_globals  = Function.func_globals .__get__
    else:
        function_closure  = Function.__closure__ .__get__
        function_code     = Function.__code__    .__get__
        function_defaults = Function.__defaults__.__get__
        function_globals  = Function.__globals__ .__get__

    function_name = Function.__dict__['__name__'].__get__


    #
    #   localize, privilege, & localize3_or_privileged2
    #
    #       Strickly speaking:
    #
    #           We don't really need to localize ourselves ...
    #           (since is never exported or referenced once this function finishes)
    #
    #       However ... might as well ... hence: 'localize = localize(localize)'
    #
    def produce_change_scope(scope):
        def change_scope(f):
            return Function(
                       function_code(f),
                       scope,
                       function_name(f),
                       function_defaults(f),
                       function_closure(f),
                   )

        return change_scope


    privileged = produce_change_scope(privileged_scope)
    privileged = privileged(privileged)                     #   Make ourselves privileged ;)
    localize   = privileged(produce_change_scope(GemShared_scope))

    localize3_or_privileged2 = (privileged   if is_python_2 else   localize)


    #
    #   next_method
    #       Access the .next method of an iterator
    #
    #       (Deals with the annoyance of .next method named .next in python 2.0, but .__next__ in python 3.0)
    #
    if is_python_2:
        @localize
        def next_method(iterator):
            return iterator.next
    else:
        @localize
        def next_method(iterator):
            return iterator.__next__


    #
    #   export
    #       Exports a function to Gem (Global Execution Module); also the actual function exported
    #       is a copy of the original function -- but with its global scope replaced to be Gem's scope.
    #
    #       Can also be used with multiple arguments to export a list of values (no replacement of
    #       global scope's is done in this case).
    #
    @localize3_or_privileged2
    def produce_actual_export(scope, insert):
        def export(f, *arguments):
            if length(arguments) is 0:
                if (f.__class__ is Function) and (function_globals(f) is not privileged_scope):
                    name = intern_string(function_name(f))

                    return insert(
                               name,
                               Function(
                                   function_code(f),
                                   scope,                   #   Replace global scope with module's scope
                                   name,
                                   function_defaults(f),
                                   function_closure(f),
                               ),
                           )

                return insert(intern_string(f.__name__), f)

            argument_iterator = iterate(arguments)
            next_argument     = next_method(argument_iterator)

            assert f.__class__ is String

            insert(f, next_argument())

            for name in argument_iterator:
                assert name.__class__ is String

                insert(intern_string(name), next_argument())


        return export


    #
    #   share_code
    #
    if __debug__:
        #
        #   Code
        #
        Code = function_code(boot).__class__


        code_argument_count    = Code.co_argcount   .__get__
        code_cell_vars         = Code.co_cellvars   .__get__
        code_constants         = Code.co_consts     .__get__
        code_filename          = Code.co_filename   .__get__
        code_first_line_number = Code.co_firstlineno.__get__
        code_flags             = Code.co_flags      .__get__
        code_free_variables    = Code.co_freevars   .__get__
        code_global_names      = Code.co_names      .__get__
        code_line_number_table = Code.co_lnotab     .__get__
        code_name              = Code.co_name       .__get__
        code_number_locals     = Code.co_nlocals    .__get__
        code_stack_size        = Code.co_stacksize  .__get__
        code_variable_names    = Code.co_varnames   .__get__
        code_virtual_code      = Code.co_code       .__get__

        if not is_python_2:
            code_keyword_only_argument_count = Code.co_kwonlyargcount.__get__


        #
        #   rename_export_code
        #
        if is_python_2:
            def rename_code(code, name):
                return Code(
                           code_argument_count   (code),
                           code_number_locals    (code),
                           code_stack_size       (code),
                           code_flags            (code),
                           code_virtual_code     (code),
                           code_constants        (code),
                           code_global_names     (code),
                           code_variable_names   (code),
                           code_filename         (code),
                           intern_string(name),                              #   Rename to 'name'
                           code_first_line_number(code),
                           code_line_number_table(code),
                           code_free_variables   (code),
                           code_cell_vars        (code),
                      )
        else:
            def rename_code(code, name):
                return Code(
                           code_argument_count             (code),
                           code_keyword_only_argument_count(code),
                           code_number_locals              (code),
                           code_stack_size                 (code),
                           code_flags                      (code),
                           code_virtual_code               (code),
                           code_constants                  (code),
                           code_global_names               (code),
                           code_variable_names             (code),
                           code_filename                   (code),
                           intern_string(name),                              #   Rename to 'name'
                           code_first_line_number          (code),
                           code_line_number_table          (code),
                           code_free_variables             (code),
                           code_cell_vars                  (code),
                      )


        #
        #   share_code
        #
        share_code = rename_code(function_code(produce_actual_export(0, 0)), 'share')


    #
    #   produce__raise_already_exists
    #
    if __debug__:
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonCore)
        NameError       = PythonException.NameError


        @localize
        def arrange(format, *arguments):
            return format % arguments


        @localize
        def produce__raise_already_exists(interned_module_name):
            def raise_already_exists(name, previous, exporting):
                name_error = arrange("%s.%s already exists (value: %r): can't export %r also",
                                     interned_module_name, name, previous, exporting)

                raise NameError(name_error)


            return raise_already_exists


    #
    #   built_in
    #
    provide__built_in = GemBuiltIn_scope.setdefault


    if __debug__:
        raise__built_in__name_error = produce__raise_already_exists(intern_string('Gem.BuiltIn'))


        @localize
        def insert__built_in(name, exporting):
            previous = provide__built_in(name, exporting)

            if previous is exporting:
                return previous

            raise__built_in__name_error(name, previous, exporting)


        built_in = produce_actual_export(GemShared_scope, insert__built_in)

        built_in = Function(
                       rename_code(share_code, 'built_in'),
                       function_globals(built_in),
                       intern_string('built_in'),
                       function_defaults(built_in),
                       function_closure(built_in),
                   )
    else:
        built_in = produce_actual_export(GemShared_scope, provide__built_in)


    #
    #   produce_export_and_share
    #
    if __debug__:
        share_name = intern_string('share')


        @localize3_or_privileged2
        def produce_export_and_share(module, shared_scope = none):
            module_name    = module.__name__ = intern_string(module.__name__)
            module_scope   = module.__dict__
            provide_export = module_scope.setdefault

            if shared_scope is none:
                shared_scope = {}

            provide_shared = shared_scope.setdefault

            raise_already_exists       = produce__raise_already_exists(module_name)
            raise_share_already_exists = produce__raise_already_exists(
                                             intern_string(arrange('%s.Shared', module_name)),
                                         )


            def insert_share(name, exporting):
                previous = provide_shared(name, exporting)

                if previous is exporting:
                    return previous

                raise_share_already_exists(name, previous, exporting)


            def insert_export(name, exporting):
                #
                #   Everything 'exported' is also 'shared', so call both 'provide_export' & 'insert_share'
                #
                previous = provide_export(name, insert_share(name, exporting))

                if previous is exporting:
                    return exporting

                raise_already_exists(name, previous, exporting)


            export = produce_actual_export(shared_scope, insert_export)
            share  = produce_actual_export(shared_scope, insert_share)

            share = Function(
                        share_code,
                        function_globals(share),
                        share_name,
                        function_defaults(share),
                        function_closure(share),
                    )

            export('Shared', shared_scope)

            return ((export, share))
    else:
        @localize
        def produce_export_and_share(module, shared_scope = none):
            module_scope   = module.__dict__
            provide_export = module_scope.setdefault

            if shared_scope is none:
                shared_scope = {}

            provide_shared = shared_scope.setdefault


            def insert_export(name, exporting):
                #
                #   Everything 'exported' is also 'shared', so call both 'provide_export' & 'provide_shared'
                #
                return provide_export(name, provide_shared(name, exporting))


            export = produce_actual_export(shared_scope, insert_export)
            share  = produce_actual_export(shared_scope, provide_shared)

            export('Shared', shared_scope)

            return ((export, share))


    [export, share] = produce_export_and_share(Gem, shared_scope = GemShared_scope)


    built_in(
        #
        #   Keywords
        #       implemented as keywords in Python 3.0 --so can't use an expression like 'PythonCore.None'.
        #
        'false',    False,
        'none',     None,
        'true',     True,


        #
        #   Functions
        #
        '__import__',   PythonCore.__import__,
        'privileged',   privileged,
    )


    if is_python_3:
        built_in(PythonCore.__build_class__.__name__, PythonCore.__build_class__)


    share(
        'built_in',     built_in,
        'export',       export,
        'share',        share,
    )


    #
    #   gem
    #
    gem_name = intern_string('gem')


    @export
    @privileged
    def gem(module_gem):
        def execute(f):
            assert f.__name__ == gem_name

            Function(
                function_code(f),
                GemShared_scope,         #   Replace global scope with Gem' shared scope
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
        @privileged
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

            return produce_export_and_share(Main)[0](f)


        def execute(f):
            assert f.__name__ == 'main'

            f()

            Main.main()


        del Main.boot
        del Main.main

        Main.export      = export
        Main.require_gem = require_gem

        return execute


    Gem.boot = boot


    Main.__builtins__ = GemBuiltIn_scope
    Main.main         = main

    del Gem.__builtins__
    del Gem.__package__


import Gem

Gem_keys = sorted(Gem.__dict__.keys())
print('Gem: ', Gem_keys)
print('Gem.Shared: ', sorted(k   for k in Gem.Shared.keys()   if k not in Gem_keys))
print("Gem.Shared['__builtins__']: ", sorted(Gem.Shared['__builtins__'].keys()))
