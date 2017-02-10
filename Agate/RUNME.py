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
    Python_System   = __import__('sys')
    is_python_2     = Python_System.version_info.major is 2
    Python_Builtins = __import__('__builtin__'  if is_python_2 else   'builtins')


    #
    #   Python functions
    #
    globals = Python_Builtins.globals
    iterate = Python_Builtins.iter
    length  = Python_Builtins.len


    #
    #   Python Types
    #
    String = Python_Builtins.str


    #
    #   Create export function
    #
    provide_gem = globals().setdefault


    def export(f, *arguments):
        if length(arguments) is 0:
            return provide_gem(f.__name__, f)

        argument_iterator = iterate(arguments)
        next_argument     = argument_iterator.next

        assert f.__class__ is String

        provide_gem(f, next_argument())

        for v in argument_iterator:
            if v.__class__ is String:
                provide_gem(v, next_argument())
            else:
                provide_gem(v.__name__, f)


    #
    #   Export ourselves :)
    #
    export(export)


    #
    #   Export everything else we used in creating export function
    #
    export(
        'globals',          globals,
        'is_python_2',      is_python_2,
        'Python_Builtins',  Python_Builtins,
        'Python_System',    Python_System,
    )


@gem('Gem.Core')
def gem():
    #
    #   Keywords
    #       implemented as keywords in Python 3.0 --so can't use something like Python_Builtins.None.
    #
    none = None

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
        #
        'false',    False,
        'none',     None,
        'true',     True,

        #
        #   Functions
        #
        'introspection',    Python_Builtins.dir,
        'intern_string',    (Python_Builtins   if is_python_2 else   Python_System).intern,
        'type',             Python_Builtins.type,
    )


@gem('Main')
def gem():
    import os, re, sys


    if is_python_2:
        #
        #   Insanely enough, the python 2.0 'input' function actually evaluated the input!
        #   We use the python 3.0 meaning of 'input' -- don't evaluate the input
        #
        input             = Python_Builtins.raw_input
        FileNotFoundError = Python_Builtins.OSError
    else:
        input             = Python_Builtins.input
        FileNotFoundError = Python_Builtins.FileNotFoundError


    compile_regular_expression = re.compile
    flush_standard_output      = sys.stdout.flush
    FrozenSet                  = Python_Builtins.frozenset
    ImportError                = Python_Builtins.ImportError
    Object                     = Python_Builtins.object
    open_file                  = Python_Builtins.open
    path_join                  = os.path.join
    path_remove                = os.remove
    path_rename                = os.rename
    property                   = Python_Builtins.property
    file_status                = os.stat


    her_or_his    = 'her|his'
    is_her_or_his = FrozenSet(['her', 'his']).__contains__


    def arrange(format, *arguments):
        return format % arguments


    def line(format, *arguments):
        print (format % arguments   if arguments else   format)
        flush_standard_output()


    def make_match_function(pattern):
        return compile_regular_expression(pattern).match


    github_username__match = make_match_function(r'[0-9A-Za-z]+(?:-[0-9A-Za-z]+)*\Z')


    class Ignore_FileNotFoundError(Object):
        __slots__ = ((
            'caught',                   #   None | FileNotFoundError
        ))


        def __init__(t):
            t.caught = none


        def __enter__(t):
            return t


        def __exit__(t, e_type, value, traceback):
            t.caught = value

            if e_type is FileNotFoundError:
                return true


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
                with Ignore_FileNotFoundError():
                    path_remove(path_old)

                with Ignore_FileNotFoundError():
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
            with Ignore_FileNotFoundError() as e:
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
        try:
            from Answers import github_username, name, pronoun
        except ImportError:
            github_username = ''
            name            = ''
            pronoun         = her_or_his

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
