#
#   To use this program:
#
#       python RUNME.py
#
#   Thanks!
#


def gem(module_name):
    def execute(f):
        f()

        return gem

    return execute


@gem('Gem.Boot')
def gem():
    #
    #
    #   This really belongs in Gem.Core, but is here since we need it during Boot
    #
    Python_System   = __import__('sys')
    is_python_2     = Python_System.version_info.major is 2
    Python_Builtins = __import__('__builtin__'  if is_python_2 else   'builtins')


    globals = Python_Builtins.globals
    iterate = Python_Builtins.iter
    length  = Python_Builtins.len


    #
    #   attribute_next
    #       Access the .next method of an iterator
    #
    #       (Deals with Annoyance of .next method named .next in python 2.0, but .__next__ in python 3.0)
    #
    if is_python_2:
        def attribute_next(iterator):
            return iterator.next
    else:
        def attribute_next(iterator):
            return iterator.__next__


    #
    #   export:
    #       Exports a function to Gem (Global Execution Module).
    #       Can also be used with multiple arguments to export a list of values.
    #
    provide_gem = globals().setdefault


    def export(f, *arguments):
        if length(arguments) is 0:
            return provide_gem(f.__name__, f)

        argument_iterator = iterate(arguments)
        next_argument     = attribute_next(argument_iterator)

        provide_gem(f, next_argument())

        for v in argument_iterator:
            provide_gem(v, next_argument())


    #
    #   Export ourselves :)
    #
    export(export)


    #
    #   Export everything else we used in creating export function
    #       Consider this part of Gem.Core -- and exporting it here just avoids repeating the code there
    #
    export(
        'attribute_next',   attribute_next,
        'globals',          globals,
        'is_python_2',      is_python_2,
        'Python_Builtins',  Python_Builtins,
        'Python_System',    Python_System,
    )


@gem('Gem.Core')
def gem():
    #
    #   none
    #
    none = None


    #
    #   arrange
    #
    @export
    def arrange(format, *arguments):
        return format % arguments


    #
    #   line
    #
    flush_standard_output = Python_System.stdout.flush
    write_standard_output = Python_System.stdout.write


    @export
    def line(format = none, *arguments):
        if format is none:
            assert length(arguments) is 0

            write_standard_output('\n')
        else:
            write_standard_output((format % arguments   if arguments else   format) + '\n')

        flush_standard_output()


    export(
        #
        #   Keywords
        #       implemented as keywords in Python 3.0 --so can't use something like Python_Builtins.None.
        #
        'false',    False,
        'none',     None,
        'true',     True,

        #
        #   Functions
        #
        'introspection',    Python_Builtins.dir,
        'intern_string',    (Python_Builtins   if is_python_2 else   Python_System).intern,
        'property',         Python_Builtins.property,
        'type',             Python_Builtins.type,

        #
        #   Types
        #
        'FrozenSet',        Python_Builtins.frozenset,
        'Object',           Python_Builtins.object,
    )


@gem('Gem.Exception')
def gem():
    Python_Exceptions = (__import__('exceptions')   if is_python_2 else  Python_Builtins)

    export(
        'FileNotFoundError',  (Python_Builtins.OSError   if is_python_2 else    Python_Builtins.FileNotFoundError),
        'ImportError',        Python_Exceptions.ImportError,
    )
    

@gem('Gem.CatchException')
def gem():
    class CatchException(Object):
        __slots__ = ((
            'exception_type',           #   Type
            'caught',                   #   None | FileNotFoundError
        ))


        def __init__(t, exception_type):
            t.exception_type = exception_type
            t.caught         = none


        def __enter__(t):
            return t


        def __exit__(t, e_type, value, traceback):
            if e_type is t.exception_type:
                t.caught = value
                return true


    @export
    def catch_ImportError():
        return CatchException(ImportError)


    @export
    def catch_FileNotFoundError():
        return CatchException(FileNotFoundError)


@gem('Gem.Import')
def gem():
    Python_Import = __import__('imp')


    find_module = Python_Import.find_module
    load_module = Python_Import.load_module


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


@gem('Gem.File')
def gem():
    Python_OperatingSystem = __import__('os')

    export(
        'open_file',    Python_Builtins.open,
        'file_status',  Python_OperatingSystem.stat
    )


@gem('Gem.IO')
def gem():
    export(
        #
        #   Insanely enough, the python 2.0 'input' function actually evaluated the input!
        #   We use the python 3.0 meaning of 'input' -- don't evaluate the input
        #
        'input',        (Python_Builtins.raw_input   if is_python_2 else   Python_Builtins.input),
    )


@gem('Gem.Path')
def gem():
    Python_OperatingSystem = __import__('os')
    Python_Path            = __import__('os.path').path


    export(
        'path_join',    Python_Path.join,
        'path_remove',  Python_OperatingSystem.remove,
        'path_rename',  Python_OperatingSystem.rename,
    )


@gem('Gem.RegularExpression')
def gem():
    Python_RegularExpression = __import__('re')


    compile_regular_expression = Python_RegularExpression.compile


    @export
    def make_match_function(pattern):
        return compile_regular_expression(pattern).match


@gem('Main')
def gem():
    her_or_his    = 'her|his'
    is_her_or_his = FrozenSet(['her', 'his']).__contains__


    github_username__match = make_match_function(r'[0-9A-Za-z]+(?:-[0-9A-Za-z]+)*\Z')


    class FileOutput(Object):
        __slots__ = ((
            'path',                     #   String+
            'f',                        #   File
            '_write',                   #   Method
        ))


        def __init__(t, path):
            t.path   = path
            t._write = t.f  = none


        def __enter__(t):
            assert t.f is none

            t.f      = f       = open_file(t.path_new, 'w')
            t._write = f.write

            return t


        def __exit__(t, e_type, value, traceback):
            path = t.path
            f    = t.f

            path_new = t.path_new       #   Grab t.path_new & t.path_old before zaping t.path
            path_old = t.path_old

            t._write = t.f = t.path = none

            f.close()

            if e_type is none:
                with catch_FileNotFoundError():
                    path_remove(path_old)

                with catch_FileNotFoundError():
                    path_rename(path, path_old)

                path_rename(path_new, path)


        def line(t, format, *arguments):
            t._write((format % arguments) + '\n')


        @property
        def path_new(t):
            return arrange('%s.new', t.path)


        @property
        def path_old(t):
            return arrange('%s.old', t.path)


    def ask(question, answer):
        response = input(question + arrange(' [%s]  ', answer)   if answer else   question + '  ')

        return (response) or (answer)


    def save_answers(github_username, name, pronoun):
        with FileOutput('Answers.py') as f:
            f.line('github_username = %r', github_username)
            f.line('name = %r', name)
            f.line('pronoun = %r', pronoun)


    def ask__github_username(github_username):
        line('')
        line('=====================')

        while 7 is 7:
            line('')
            line('***  Question:  What is your GitHub user name?')
            line('===  Example Answer: JoeSmith')

            if github_username:
                line('')
                line('***  HIT return to accept your previous answer:  %r  ***', github_username)

            line('')
            github_username = ask('First what is your GitHub User name?', github_username)

            if github_username__match(github_username):
                return github_username

            line('')
            line('***  GitHub user name must be alphanumeric characters or single hypens ***')
            line('***  GitHub user name may also not begin or end with a hypen  ***')

            github_username = ''


    def ask_name(name):
        line('')
        line('=====================')

        while 7 is 7:
            line('')
            line('***  NOTE: You may use your real name or as pseudonym.  Both are acceptable  ***')
            line('')
            line('***  Question:  What name do you wish to use?')
            line('===  Example Answer: Susan Smith')

            if name:
                line('')
                line('***  HIT return to accept your previous answer:  %s  ***', name)

            line('')
            name = ask('Second, what name do you wish to use?', name)

            if name is not '':
                return name


    def ask_pronoun(pronoun):
        line('')
        line('=====================')

        while 7 is 7:
            line('')
            line('***  Question:  Which prounoun to use?')
            line('===  Example Answer: her')

            if pronoun != her_or_his:
                line('***  HIT return to accept your previous answer:  %s  ***', pronoun)

            line('')
            pronoun = ask('Third, which pronoun to use?', pronoun)

            if is_her_or_his(pronoun):
                return pronoun
                
            line('')
            line("***  Pronoun is expected to be %r or %r ***", 'her', 'his')
            line('')
            
            if pronoun == her_or_his:
                #
                #   Don't bother asking if 'her|his' was the correct answer, user probably just hit return
                #
                continue

            question = arrange('Are you sure you want to use %r instead?', pronoun)
            answer   = ask(question, 'n|N|y|Y')

            if (answer is 'y') or (answer is 'Y'):
                return pronoun

            pronoun = her_or_his


    def ask_correct(github_username, name, pronoun):
        while 7 is 7:
            line('')
            line('=====================')
            line('GitHub username:  %s', github_username)
            line('Name:             %s', name)
            line('Pronoun:          %s', pronoun)
            line('=====================')
            line('')

            answer = ask('Is this correct?', 'Y|y|N|n')

            if (answer is 'Y') or (answer is 'y'):
                return true

            if (answer is 'N') or (answer is 'n'):
                return false

            line('')
            line('***  Please answer Y, y, N, or n')


    def ask_three_questions(github_username, name, pronoun):
        while 7 is 7:
            line('Welcome to the RUNME, V0.0')
            line('')
            line('This program will create a contribution agreement:')
            line('    A.  For you to add to your git repository; and')
            line('    B.  For you to sign by committing with your GPG key.')
            line('')
            line('You will need to provide:')
            line('    1.  GitHub username;')
            line('    2.  Your name; and')
            line('    3.  A pronoun.')
            line('')

            github_username = ask__github_username(github_username)
            name            = ask_name(name)
            pronoun         = ask_pronoun(pronoun)

            save_answers(github_username, name, pronoun)

            if ask_correct(github_username, name, pronoun):
                return ((github_username, name, pronoun))


    def write_contribution_agreement(github_username, name, pronoun):
        path = path_join('Agreements', arrange('%s.txt', github_username))

        while 7 is 7:
            with catch_FileNotFoundError() as e:
                file_status(path)

            if e.caught is not none:
                break

            line('')
            line('=====================')
            line('')

            question = arrange('%s aleady exists.  Overwrite?', path)
            answer   = ask(question, 'n|y')

            if (answer is 'Y') or (answer is 'y'):
                break

            if (answer is 'N') or (answer is 'n'):
                line('')
                line('=====================')
                line('')
                line('Exiting WITHOUT overwriting %s', path)
                return

            line('')
            line('***  Please answer Y, y, N, or n')

        with FileOutput(path) as f:
            f.line('%s agrees to use MIT license for all %s contributions.', name, pronoun)
            f.line('')
            f.line('This means that everyone has the right to use the contributions for any reason')
            f.line('whatsoever, including making a profit:')
            f.line('')
            f.line('    o  Without giving anything to %s in return;', name)
            f.line('    o  And also, that once contributed, the contribution is permenant & cannot')
            f.line('       be undone.')
            f.line('')
            f.line('This agreement is dated 2017-02-09 and applies to all commits made via the')
            f.line("GitHub username '%s' to the following GitHub projects:", github_username)
            f.line('')
            f.line('	Rhodolite/Agate')
            f.line('	Rhodolite/Gem')
            f.line('	Rhodolite/Sardonyx')
            f.line('	Rhodolite/Snake')
            f.line('	Rhodolite/Topaz')
            f.line('')
            f.line('    (and any forks of these projects in GitHub).')
            f.line('')
            f.line('Signed electronically & committed with GPG key 93862907665BEEDA,')
            f.line('')
            f.line('%s', name)
            f.line('')
            f.line('===============================================================================')
            f.line('')
            f.line('Here is a copy of the MIT license that %s is agreeing to:', name)
            f.line('')
            f.line('MIT License')
            f.line('')
            f.line('Copyright (c) 2017 %s', name)

            with open_file('LICENSE') as license:
                for s in license.read().splitlines()[3:]:
                    f.line('%s', s)

        line('')
        line('CREATED: %s', path)
        line('')
        line('Please EDIT the GPG key to the key you will sign with')


    @export
    def main():
        Answers = find_and_import_module__or__none('Answers', ['.'])

        if Answers is none:
            github_username = ''
            name            = ''
            pronoun         = her_or_his
        else:
            github_username = Answers.github_username
            name            = Answers.name
            pronoun         = Answers.pronoun

        [github_username, name, pronoun] = ask_three_questions(github_username, name, pronoun)

        write_contribution_agreement(github_username, name, pronoun)


if __name__ == '__main__':
    main()


#
#   To use this program:
#
#       python RUNME.py
#
#   Thanks!
#
