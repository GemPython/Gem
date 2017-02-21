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
    PythonSystem  = __import__('sys')
    is_python_2   = PythonSystem.version_info.major is 2
    is_python_3   = PythonSystem.version_info.major is 3
    PythonBuiltIn = __import__('__builtin__'  if is_python_2 else   'builtins')


    #
    #   Python keywords
    #
    none = None

    #
    #   Python Functions
    #
    intern_string = (PythonBuiltIn   if is_python_2 else   PythonSystem).intern
    iterate       = PythonBuiltIn.iter
    length        = PythonBuiltIn.len


    #
    #   Python types
    #
    Module    = PythonBuiltIn.__class__
    LiquidSet = PythonBuiltIn.set
    String    = PythonBuiltIn.str


    #
    #   python_modules (also lookup_python_module & store_python_module)
    #
    python_modules       = PythonSystem.modules
    lookup_python_module = python_modules.get
    store_python_module  = python_modules.__setitem__


    #
    #   Gem
    #
    Gem       = python_modules['Gem']
    Gem_name  = Gem.__name__ = intern_string(Gem.__name__)
    gem_scope = Gem.__dict__


    #
    #   GemBuiltIn
    #
    GemBuiltIn       = Module(intern_string('Gem.BuiltIn'))
    GemBuiltIn_scope = GemBuiltIn.__dict__


    #
    #   GemPrivileged
    #
    GemPrivileged       = Module(intern_string('Gem.Privileged'))
    GemPrivileged_scope = GemPrivileged.__dict__

    GemPrivileged.__builtins__ = PythonBuiltIn.__dict__


    #
    #   GemShared
    #
    GemShared       = Module(intern_string('Gem.Shared'))
    GemShared_scope = GemShared.__dict__


    #
    #   Store in python modules:
    #
    #       Gem                 (overwritten)
    #       Gem.Core
    #       Gem.Restricted
    #       Gem.Shared
    #   
    for module in [Gem, GemBuiltIn, GemPrivileged, GemShared]:
        store_python_module(module.__name__, module)


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
    #   Code
    #
    if __debug__:
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
    #   localize & privilege
    #
    #       Although it is possible to share code between 'localize' & 'privileged' -- it doesn't make
    #       sense -- since 'localize' is local to this function.  Thus when this when this function
    #       ends, 'localize' is deallocated anyay.
    #
    #       Also this way, 'localize' & privileged can be used on the next functions quickly.
    #
    def localize(f):
        return Function(
                   function_code(f),
                   GemShared_scope,
                   intern_string(function_name(f)),
                   function_defaults(f),
                   function_closure(f),
               )


    def privileged(f):
        return Function(
                   function_code(f),
                   GemPrivileged_scope,
                   intern_string(function_name(f)),
                   function_defaults(f),
                   function_closure(f),
               )


    #
    #   'privileged' is currently privileged ... but it won't be once exported.
    #
    #       Hence make it permenantly privileged by calling it on itself :)
    #
    privileged = privileged(privileged)


    localize3_or_privileged2 = (privileged   if is_python_2 else   localize)


    #
    #   rename_code
    #
    if __debug__:
        if is_python_2:
            @localize
            def rename_code(code, interned_name):
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
                           interned_name,                           #   Rename to 'name'
                           code_first_line_number(code),
                           code_line_number_table(code),
                           code_free_variables   (code),
                           code_cell_vars        (code),
                      )
        else:
            @localize
            def rename_code(code, interned_name):
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
                           interned_name,                           #   Rename to 'name'
                           code_first_line_number          (code),
                           code_line_number_table          (code),
                           code_free_variables             (code),
                           code_cell_vars                  (code),
                      )


    #
    #   rename_function
    #
    if __debug__:
        @localize3_or_privileged2
        def rename_function(actual_name, f, code = none, scope = none):
            interned_name = intern_string(actual_name)

            return Function(
                       (code) or (rename_code(function_code(f), interned_name)),
                       (scope) or (function_globals(f)),
                       interned_name,
                       function_defaults(f),
                       function_closure(f),
                   )
    else:
        @localize3_or_privileged2
        def rename_function(name, f, code = none, scope = none):
            if code is scope is none:
                return f

            return Function(
                       (code) or (function_code(f)),
                       (scope) or (function_globals(f)),
                       intern_string(actual_name),
                       function_defaults(f),
                       function_closure(f),
                   )


    #
    #   rename
    #
    if __debug__:
        def rename(name):
            def rename(f):
                return rename_function(name, f)


            return rename


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
    #       is a copy of the original function -- but with its global scope replaced to 'scope'.
    #
    #       Can also be used with multiple arguments to export a list of values (no replacement of
    #       global scope's is done in this case).
    #
    @localize3_or_privileged2
    def produce_actual_export(scope, insert):
        def export(f, *arguments):
            if length(arguments) is 0:
                if (f.__class__ is Function) and (function_globals(f) is not GemPrivileged_scope):
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

            insert(intern_string(f), next_argument())

            for name in argument_iterator:
                insert(intern_string(name), next_argument())


        return export


    #
    #   share_name & share_code
    #
    share_name = intern_string('share')


    if __debug__:
        share_code = rename_code(function_code(produce_actual_export(0, 0)), share_name)


    #
    #   arrange
    #
    @localize
    def arrange(format, *arguments):
        return format % arguments


    #
    #   raise_already_exists
    #
    if __debug__:
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
        NameError       = PythonException.NameError


        @localize
        def raise_already_exists(module_name, name, previous, exporting):
            name_error = arrange("%s.%s already exists (value: %r): can't export %r also",
                                 module_name, name, previous, exporting)

            raise NameError(name_error)


    #
    #   produce_dual_insert
    #
    if __debug__:
        @localize
        def produce_dual_insert(actual_name, single_insert, provide, module_name):
            module_name = intern_string(module_name)


            @rename(actual_name)
            def dual_insert(name, exporting):
                previous = provide(name, single_insert(name, exporting))

                if previous is exporting:
                    return exporting

                raise_already_exists(module_name, name, previous, exporting)


            return dual_insert
    else:
        @localize
        def produce_dual_insert(actual_name, single_insert, provide, module_name):
            def dual_insert(name, exporting):
                return provide(name, single_insert(name, exporting))


            return dual_insert


    #
    #   produce_single_insert
    #
    if __debug__:
        @localize
        def produce_single_insert(actual_name, provide, module_name):
            module_name = intern_string(module_name)


            @rename(actual_name)
            def single_insert(name, exporting):
                previous = provide(name, exporting)

                if previous is exporting:
                    return previous

                raise_already_exists(module_name, name, previous, exporting)


            return single_insert
    else:
        @localize
        def produce_single_insert(actual_name, provide, module_name):
            return provide


    #
    #   built_in & restricted
    #
    insert_privileged = produce_single_insert(
                            'insert_privileged',
                             GemPrivileged_scope.setdefault,
                             GemPrivileged.__name__,
                        )

    insert__built_in = produce_dual_insert(
                           'insert__built_in',
                           insert_privileged,
                           GemBuiltIn_scope.setdefault,
                           GemBuiltIn.__name__,
                       )

    built_in   = produce_actual_export(GemShared_scope, insert__built_in)
    restricted = produce_actual_export(GemShared_scope, insert_privileged)


    if __debug__:
        built_in   = rename_function('built_in',   built_in)
        restricted = rename_function('restricted', restricted)


    #
    #   special_builtins_name
    #
    special_builtins_name  = intern_string('__builtins__')


    #
    #   produce_export_and_share
    #
    interned_Shared_name = intern_string('Shared')


    @localize
    def produce_export_and_share(module, Shared = none):
        module_name  = module.__name__ = intern_string(module.__name__)
        module_scope = module.__dict__

        if Shared is none:
            Shared_name = intern_string(arrange('%s.Shared', module_name))
            Shared      = Module(interned_Shared_name)
        else:
            Shared_name = Shared.__name__

            assert Shared_name is intern_string(Shared_name)

        Shared_scope = Shared.__dict__

        insert_share = produce_single_insert(
                           'insert_share',
                           Shared_scope.setdefault,
                           Shared_name,
                       )

        insert_export = produce_dual_insert(
                            'insert_export',
                            insert_share,
                            module_scope.setdefault,
                            module_name,
                        )

        export = produce_actual_export(Shared_scope, insert_export)
        share  = produce_actual_export(Shared_scope, insert_share)

        if __debug__:
            share = rename_function(share_name, share, code = share_code)

        share(
                special_builtins_name,  GemBuiltIn_scope,
                'export',               export,
                share_name,             share,
                interned_Shared_name,   Shared,
            )

        export(
                interned_Shared_name,   Shared,
            )

        store_python_module(Shared_name, Shared)


    #
    #   export & share
    #
    produce_export_and_share(Gem, Shared = GemShared)

    export = GemShared.export
    share  = GemShared.share


    #
    #   Initial built-in's
    #
    built_in(
        #
        #   Keywords
        #       implemented as keywords in Python 3.0 --so can't use an expression like 'PythonBuiltIn.None'.
        #
        'false',    False,
        'none',     None,
        'true',     True,

        #
        #   Types
        #
        'LiquidSet',    PythonBuiltIn.set,
        'String',       PythonBuiltIn.str,

        #
        #   Functions
        #
        'arrange',          arrange,
        'length',           length,
        'intern_string',    intern_string,
    )


    #
    #   Only put in GemBuiltIn_scope: __build__class & __import__
    #
    #       (not needed in GemPrivileged_scope, since it is found in GemPrivileged_scope['__builtins__'])
    #
    if is_python_3:
        GemBuiltIn_scope[intern_string(PythonBuiltIn.__build_class__.__name__)] = PythonBuiltIn.__build_class__


    GemBuiltIn_scope[intern_string(PythonBuiltIn.__import__.__name__)] = PythonBuiltIn.__import__


    #
    #   Privileged
    #       Put the Python BuiltIn module into GemPrivileged: making it an unrestricted scope.
    #
    restricted(
        special_builtins_name, PythonBuiltIn.__dict__,
    )

    #
    #   Initial shares's
    #
    share(
        #
        #   __builtins__
        #
        #'__builtins__',    GemBuiltIn_scope,       #   Done in produce_export_and_share
        #

        #
        #   Functions
        #
        'built_in',     built_in,
        'Privileged',   GemPrivileged,
        'restricted',   restricted,

        #
        #   Modules
        #
        'PythonBuiltIn',   PythonBuiltIn,
        'PythonSystem', PythonSystem,
        #'Shared',      Shared                      #   Done in produce_export_and_share
    )


    export(
        #
        #   Types
        #
        'Module',   Module,

        #
        #   Modules
        #
        'BuiltIn',  GemBuiltIn,
        #'Shared',  GemShared,                      #   Done in produce_export_and_share

        #
        #   Functions
        #
        'rename_function',  rename_function,
        'privileged',       privileged,

        #
        #   Values
        #
        'is_python_2',  is_python_2,
        'is_python_3',  is_python_3,
    )


    #
    #   Main
    #
    Main = python_modules['__main__']


    #
    #   Debugging
    #
    if 0:
        flush_standard_output = PythonSystem.stdout.flush
        write_standard_output = PythonSystem.stdout.write


        def debug(format = none, *arguments):
            if format is none:
                assert length(arguments) is 0

                write_standard_output('\n')
            else:
                write_standard_output((format % arguments   if arguments else   format) + '\n')

            flush_standard_output()


    #
    #   gem_modules (also lookup_gem_module & store_gem_module)
    #
    gem_modules       = { Gem_name : Gem }
    lookup_gem_module = gem_modules.get
    store_gem_module  = gem_modules.__setitem__


    #
    #   gem
    #
    gem_name = intern_string('gem')


    @built_in
    @localize3_or_privileged2
    def gem(module_name):
        #debug('gem: %r', module_name)

        dot_index = module_name.rfind('.')

        assert dot_index is not -1

        parent_module_name = module_name[:dot_index]
        child_module_name  = module_name[dot_index + 1:]

        parent_module = lookup_python_module(parent_module_name)

        if parent_module is none:
            parent_module = require_gem(parent_module_name)
        
        Shared_Scope = parent_module.Shared.__dict__

        if child_module_name == 'Main':
            del Main.gem


            def execute(f):
                assert f.__name__ == gem_name

                Function(
                    function_code(f),
                    Shared_Scope,            #   Replace global scope with the module's shared scope
                    gem_name,
                    function_defaults(f),
                    function_closure(f),
                )(
                )

                main = parent_module.Shared.__dict__.pop('main')

                main()


            return execute


        def execute(f):
            assert f.__name__ == gem_name

            Function(
                function_code(f),
                Shared_Scope,            #   Replace global scope with the module's shared scope
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
    if is_python_2:
        #
        #   Python 2.0 method of loading a module with 'gem' pre-initialized
        #
        #       This is messy -- see below for the Python 3.0 method which is much cleaner.
        #
        PythonOldImport   = __import__('imp')
        find_module       = PythonOldImport.find_module
        load_module       = PythonOldImport.load_module
        PACKAGE_DIRECTORY = PythonOldImport.PKG_DIRECTORY


        @built_in
        @privileged
        def require_gem(module_name):
            module = lookup_gem_module(module_name)

            if module is not none:
                return module

            #debug('require_gem: %r', module_name)

            dot_index = module_name.rfind('.')

            if dot_index is not -1:
                parent_module = require_gem(module_name[:dot_index])

            module_name = intern_string(module_name)
            module      = Module(module_name)

            is_package = 0

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

            if dot_index is -1:
                [f, pathname, description] = find_module(module_name)
            else:
                [f, pathname, description] = find_module(module_name[dot_index + 1:], parent_module.__path__)

            #debug('%r: %r, %r, %r', module_name, f, pathname, description)

            #
            #   CAREFUL here:
            #       We *MUST* close 'f' if any exception is thrown.
            #
            #       So ASAP use 'f' within a 'with' clause (this ensures 'f' is always closed, whether
            #       an exception is thrown or not)
            #
            if f is not none:
                with f:
                    module.gem = gem
                    load_module(module_name, f, pathname, description)
            else:
                if description[2] == PACKAGE_DIRECTORY:
                    is_package = 7
                    produce_export_and_share(module)

                load_module(module_name, f, pathname, description)

            #
            #   If this is a package: Keep this module
            #   Otherwise:            Discard this module (it is no longer needed)
            #
            if is_package is 7:
                store_gem_module(module_name, module)
            else:
                del python_modules[module_name]

                store_gem_module(module_name, 0)

            return module


    else:
        #
        #   Python 3.0 method of loading a module with 'gem' pre-initialized
        #
        PythonImportUtility          = __import__('importlib.util').util
        ImportError                  = PythonBuiltIn.ImportError
        lookup_module_blueprint      = PythonImportUtility.find_spec
        create_module_from_blueprint = PythonImportUtility.module_from_spec


        @built_in
        def require_gem(module_name):
            module = lookup_gem_module(module_name)

            if module is not none:
                return module

            #debug('require_gem: %r', module_name)

            dot_index = module_name.rfind('.')

            if dot_index is not -1:
                parent_module = require_gem(module_name[:dot_index])

            module_name = intern_string(module_name)
            blueprint   = lookup_module_blueprint(module_name)

            if blueprint is none:
                import_error = arrange("Can't find module %s", module_name)

                raise ImportError(import_error)

            is_package = 0
            module     = create_module_from_blueprint(blueprint)

            if '__path__' in module.__dict__:
                is_package = 7
                produce_export_and_share(module)
            else:
                module.gem = gem

            blueprint.loader.exec_module(module)

            if is_package is 7:
                store_python_module(module_name, module)
                store_gem_module   (module_name, module)
            else:
                store_gem_module(module_name, 0)

            return module


    require_gem('Gem.Core')


    #
    #   main
    #
    Gem.boot = boot
    Main.gem = gem


    del Gem.__builtins__
    del Gem.__package__
