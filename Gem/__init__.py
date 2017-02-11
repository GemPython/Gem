#
#   To use this program:
#
#       python RUNME.py
#
#   Thanks!
#
def gem(module_name):
    def execute(f):
        return f()

    return execute


@gem('Gem.Boot')
def gem():
    #
    #
    #   This really belongs in Gem.Core, but is here since we need it during Boot
    #
    PythonSystem = __import__('sys')
    is_python_2   = PythonSystem.version_info.major is 2
    PythonCore    = __import__('__builtin__'  if is_python_2 else   'builtins')


    #
    #   Python Functions
    #
    intern_string = (PythonCore   if is_python_2 else   PythonSystem).intern
    iterate       = PythonCore.iter
    length        = PythonCore.len


    #
    #   Python types
    #
    String = PythonCore.str


    #
    #   Python method
    #
    python_modules = PythonSystem.modules


    #
    #   Gem
    #       Replace the index in python_modules & also Gem.__name__ with an intern'ed copy of 'Gem'.
    #
    Gem                      = python_modules['Gem']
    Gem.__name__             = Gem_name                  = intern_string(Gem.__name__)
    python_modules[Gem_name] = Gem


    #
    #   export (version 1):
    #       Exports a function to Gem (Global Execution Module).  Version 1 does not need
    #       to replace the global scope, as its already set to Gem.
    #
    gem_scope   = Gem.__dict__
    provide_gem = gem_scope.setdefault


    def export(f):
        return provide_gem(f.__name__, f)


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
    #   export (version 2):
    #       Exports a function to Gem (Global Execution Module); also the actual function exported
    #       is a copy of the original function -- but with its global scope replaced to be Gem's scope.
    #
    #       Can also be used with multiple arguments to export a list of values (no replacement of
    #       global scope's is done in this case).
    #
    Function = export.__class__

    if is_python_2:
        function_closure  = Function.func_closure .__get__
        function_code     = Function.func_code    .__get__
        function_defaults = Function.func_defaults.__get__
    else:
        function_closure  = Function.__closure__.__get__
        function_code     = Function.__code__    .__get__
        function_defaults = Function.__defaults__.__get__

    function_name = Function.__dict__['__name__'].__get__


    @export
    def export(f, *arguments):
        if length(arguments) is 0:
            name = function_name(f)

            return provide_gem(
                       name,
                       Function(
                           function_code(f),
                           gem_scope,               #   Replace global scope with Gem's scope
                           name,
                           function_defaults(f),
                           function_closure(f),
                       ),
                   )

        argument_iterator = iterate(arguments)
        next_argument     = next_method(argument_iterator)

        assert f.__class__ is String

        provide_gem(f, next_argument())

        for v in argument_iterator:
            assert v.__class__ is String

            provide_gem(v, next_argument())


    export(export)                                  #   Export ourselves :)


    #
    #   gem
    #
    gem_name = intern_string('gem')


    del gem_scope[gem_name]


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


    python_modules['__main__'].gem = gem


    #
    #   Export everything else we used in creating export function
    #       Consider this part of Gem.Core -- and exporting it here just avoids repeating the code there
    #
    export(
        #
        #   Modules
        #
        'PythonCore',       PythonCore,
        'PythonSystem',     PythonSystem,

        #
        #   Functions
        #
        'intern_string',    intern_string,
        'iterate',          iterate,
        'length',           length,

        #
        #   Values
        #
        'is_python_2',      is_python_2,
    )
