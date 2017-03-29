#
#   Copyright (c) 2017 Amit Green
#
if __name__ == '__main__':
    def gem(module_name):
        def execute(f):
            return f()

        return execute


    @gem('Ivory.Boot')
    def gem():
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
        exception_information = PythonSystem.exc_info
        intern_string         = (PythonBuiltIn   if is_python_2 else   PythonSystem).intern
        iterate               = PythonBuiltIn.iter
        length                = PythonBuiltIn.len
        system_exit           = PythonSystem.exit


        #
        #   Python types
        #
        Module = PythonBuiltIn.__class__


        #
        #   python_modules & store_python_modules
        #
        python_modules      = PythonSystem.modules
        store_python_module = python_modules.__setitem__


        #
        #   PythonException
        #
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
        NameError       = PythonException.NameError
        SystemExit      = PythonException.SystemExit


        #
        #   PythonTraceback
        #
        PythonTraceBack       = __import__('traceback')
        print_exception       = PythonTraceBack.print_exception


        #
        #   Ivory
        #
        Ivory_name         = intern_string('Ivory')
        Ivory              = Module(Ivory_name)
        Ivory_scope        = Ivory.__dict__
        Ivory.__builtins__ = PythonBuiltIn.__dict__

        store_python_module(Ivory_name, Ivory)


        #
        #   localize
        #
        def localize(f):
            return Function(
                       function_code(f),
                       Ivory_scope,
                       intern_string(function_name(f)),
                       function_defaults(f),
                       function_closure(f),
                   )

        #
        #   Function
        #
        Function = localize.__class__

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
            Code = function_code(localize).__class__


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
            @localize
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
            @localize
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
        #       Exports a function to Ivory; also the actual function exported
        #       is a copy of the original function -- but with its global scope replaced to 'scope'.
        #
        #       Can also be used with multiple arguments to export a list of values (no replacement of
        #       global scope's is done in this case).
        #
        @localize
        def produce_actual_export(scope, insert):
            def export(f, *arguments):
                if length(arguments) is 0:
                    if f.__class__ is Function:
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
        #   arrange
        #
        @localize
        def arrange(format, *arguments):
            return format % arguments


        #
        #   raise_already_exists
        #
        if __debug__:
            @localize
            def raise_already_exists(module_name, name, previous, exporting):
                name_error = arrange("%s.%s already exists (value: %r): can't export %r also",
                                     module_name, name, previous, exporting)

                raise NameError(name_error)


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
        #   share
        #
        insert_share = produce_single_insert('insert_share', Ivory_scope.setdefault, Ivory_name)
        share        = produce_actual_export(Ivory_scope, insert_share)


        if __debug__:
            share = rename_function('share', share)


        #
        #   Initial share
        #
        share(
            #
            #   Keywords
            #       implemented as keywords in Python 3.0 --so can't use an expression like 'PythonBuiltIn.None'.
            #
            'false',    False,
            'none',     None,
            'true',     True,

            #
            #   Modules
            #
            'PythonBuiltIn',    PythonBuiltIn,
            'PythonSystem',     PythonSystem,


            #
            #   Types
            #
            'Module',   Module,

            #
            #   Functions
            #
            'arrange',          arrange,
            'length',           length,
            'intern_string',    intern_string,
            'share',            share,


            #
            #   Values
            #
            'is_python_2',  is_python_2,
            'is_python_3',  is_python_3,
        )


        #
        #   gem
        #
        gem_name = intern_string('gem')


        def gem(module_gem):
            def execute(f):
                Function(
                    function_code(f),
                    Ivory_scope,         #   Replace global scope with Ivory's shared scope
                    gem_name,
                    function_defaults(f),
                    function_closure(f),
                )(
                )

                if f.__name__ == '__name__':
                    #
                    #   The final function just got executed:
                    #
                    #   1.  Cleanup after ourselves
                    #   2.  Run main inside an exception handler
                    #
                    main = Ivory_scope.pop('main')

                    try:
                        main()
                    except:
                        [e_type, e, e_traceback] = exception_information()

                        if e_type is SystemExit:    #   Builtin
                            raise

                        #
                        #   Use 'traceback.tb_next' to remove ourselves from the stack trace
                        #
                        try:
                            print_exception(e_type, e, e_traceback.tb_next)
                        finally:
                            e_type = e = e_traceback = 0

                        PythonSystem.exit(1)


                assert f.__name__ == '__name__'

                return gem


            return execute


        return gem


    @gem('Ivory.Main')
    def __name__():
        PythonPlatform  = __import__('platform')
        PythonSystem    = __import__('sys')
        is_python_2     = PythonSystem.version_info.major is 2
        is_python_3     = PythonSystem.version_info.major is 3
        PythonBuiltIn   = __import__('__builtin__'  if is_python_2 else   'builtins')
        PythonTraceBack = __import__('traceback')
        PythonTypes     = __import__('types')


        #
        #   Python keywords
        #       implemented as keywords in Python 3.0 --so can't use an expression like 'PythonBuiltIn.None'.
        #
        false = False
        none  = None


        #
        #   Python Functions
        #
        intern_string = (PythonBuiltIn   if is_python_2 else   PythonSystem).intern
        iterate       = PythonBuiltIn.iter
        length        = PythonBuiltIn.len
        portray       = PythonBuiltIn.repr
        type          = PythonBuiltIn.type


        #
        #   Python Types
        #
        FrozenSet = PythonBuiltIn.frozenset
        Method    = PythonTypes.MethodType
        NoneType  = none.__class__
        Object    = PythonBuiltIn.object
        Tuple     = PythonBuiltIn.tuple


        #
        #   Exceptions
        #
        PythonException = (__import__('exceptions')   if is_python_2 else  PythonBuiltIn)
        SystemExit      = PythonException.SystemExit



        #
        #   arrange
        #
        def arrange(format, *arguments):
            return format % arguments


        #
        #   line
        #
        flush_standard_output = PythonSystem.stdout.flush
        write_standard_output = PythonSystem.stdout.write
        position_cache        = [0]
        position              = Method(position_cache.__getitem__, 0)
        save_position         = Method(position_cache.__setitem__, 0)
        save_position_0       = Method(save_position, 0)


        def line(format = none, *arguments):
            if format is none:
                assert length(arguments) is 0

                write_standard_output('\n')
            else:
                if position() != 0:
                    write_standard_output(' ' + (format % arguments   if arguments else   format) + '\n')
                else:
                    write_standard_output((format % arguments   if arguments else   format) + '\n')

            flush_standard_output()
            save_position_0()



        def partial(format, *arguments):
            s = (format % arguments   if arguments else   format)

            write_standard_output(s)
            flush_standard_output()

            save_position(position() + length(s))


        #
        #   PrintHeader_and_PrintAndIgnoreExceptions
        #
        class PrintHeader_and_PrintAndIgnoreExceptions():
            __slots__ = ((
                'header',               #   String
            ))


            def __init__(t, header):
                t.header = header


            def __enter__(t):
                partial('%s ...', t.header)

                return t


            def __exit__(t, e_type, e_value, e_traceback):
                if (e_value is None) or (e_type is SystemExit):
                    return

                if position() != 0:
                    line()

                PythonTraceBack.print_exception(e_type, e_value, e_traceback.tb_next)

                #
                #   Swallow exception
                #
                return false


        def safe(header):
            return PrintHeader_and_PrintAndIgnoreExceptions(header)


        #
        #   python_version
        #
        def python_version():
            version_information = PythonSystem.version_info
            build_information   = PythonPlatform.python_build()

            assert (type(build_information) is Tuple) and (length(build_information) == 2)

            return arrange('%d%s%s%s (%s %s)',
                           version_information.major,
                           (
                               ''   if version_information.minor == version_information.micro == 0 else
                               arrange('.%d', version_information.micro)
                           ),
                           (
                               ''   if version_information.micro == 0 else
                               arrange('.%d', version_information.micro)
                           ),
                           (
                               ''   if version_information.serial == 0 else
                               arrange('.%d', version_information.serial)
                           ),
                           build_information[0],
                           build_information[1])



        #
        #   Main
        #
        @share
        def main():
            #
            #   Version
            #
            with safe('Python version'):
                line(python_version())


            #
            #   Executable
            #
            with safe('Python executable'):
                lookup_PythonSystem = PythonSystem.__dict__.get
                executable          = lookup_PythonSystem('executable')

                line('unknown'   if executable is none else   portray(executable))
