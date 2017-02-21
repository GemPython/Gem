#
#   To use this program:
#
#       python RUNME.py
#
#   Thanks!
#


#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
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
    PythonSystem = __import__('sys')
    is_python_2   = PythonSystem.version_info.major is 2
    PythonCore    = __import__('__builtin__'  if is_python_2 else   'builtins')


    globals = PythonCore.globals
    iterate = PythonCore.iter
    length  = PythonCore.len


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
        'PythonCore',       PythonCore,
        'PythonSystem',     PythonSystem,
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
    flush_standard_output = PythonSystem.stdout.flush
    write_standard_output = PythonSystem.stdout.write


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
        #       implemented as keywords in Python 3.0 --so can't use something like PythonCore.None.
        #
        'false',    False,
        'none',     None,
        'true',     True,

        #
        #   Functions
        #
        'introspection',    PythonCore.dir,
        'intern_string',    (PythonCore   if is_python_2 else   PythonSystem).intern,
        'property',         PythonCore.property,
        'type',             PythonCore.type,

        #
        #   Types
        #
        'FrozenSet',        PythonCore.frozenset,
        'Object',           PythonCore.object,
        'String',           PythonCore.str,
    )


@gem('Gem.Exception')
def gem():
    PythonException = (__import__('exceptions')   if is_python_2 else  PythonCore)
    RuntimeError    = PythonException.RuntimeError


    @export
    def raise_runtime_error(format, *arguments):
        error_message = (format   % arguments   if arguments else   format)

        raise RuntimeError(error_message)


    export(
        'FileNotFoundError',  (PythonCore.OSError   if is_python_2 else    PythonCore.FileNotFoundError),
        'ImportError',        PythonException.ImportError,
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
    PythonImport = __import__('imp')
    find_module  = PythonImport.find_module
    load_module  = PythonImport.load_module


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
    export(
        'open_file',    PythonCore.open,
    )


@gem('Gem.FileStatus')
def gem():
    PythonOperatingSystem         = __import__('os')
    PythonFileStatus              = __import__('stat')
    PythonFileStatus__inode_flags = PythonFileStatus.S_IMODE
    PythonFileStatus__file_type   = PythonFileStatus.S_IFMT
    python_file_status            = PythonOperatingSystem.stat


    class FileType(Object):
        __slots__ = ((
            'name',                     #   String+
            'is_block_device',          #   Boolean
            'is_character_device',      #   Boolean
            'is_directory',             #   Boolean
            'is_fifo',                  #   Boolean
            'is_regular_file',          #   Boolean
            'is_socket',                #   Boolean
            'is_symbolic_link',         #   Boolean
            'nonexistent',              #   Boolean
        ))


        def __init__(
                t, name,

                is_block_device     = false,
                is_character_device = false,
                is_directory        = false,
                is_fifo             = false,
                is_regular_file     = false,
                is_socket           = false,
                is_symbolic_link    = false,
                nonexistent         = false,
        ):
            assert name.__class__ is String

            assert (
                     (
                           is_block_device + is_character_device + is_directory + is_fifo + is_regular_file
                         + is_socket + is_symbolic_link + nonexistent
                     )
                  == 1
            )

            t.name                = name
            t.is_block_device     = is_block_device
            t.is_character_device = is_character_device
            t.is_directory        = is_directory
            t.is_fifo             = is_fifo
            t.is_regular_file     = is_regular_file
            t.is_socket           = is_socket
            t.is_symbolic_link    = is_symbolic_link
            t.nonexistent         = nonexistent


    file_type__block_device     = FileType('block_device',     is_block_device     = true)
    file_type__character_device = FileType('character_device', is_character_device = true)
    file_type__directory        = FileType('directory',        is_directory        = true)
    file_type__fifo             = FileType('fifo',             is_fifo             = true)
    file_type__regular_file     = FileType('regular_file',     is_regular_file     = true)
    file_type__socket           = FileType('socket',           is_socket           = true)
    file_type__symbolic_link    = FileType('symbolic_link',    is_symbolic_link    = true)

    file_type__nonexistent = FileType('nonexistent', nonexistent = true)


    del FileType.__init__


    find__file_type = {
        PythonFileStatus.S_IFBLK  : file_type__block_device,
        PythonFileStatus.S_IFCHR  : file_type__block_device,
        PythonFileStatus.S_IFDIR  : file_type__regular_file,
        PythonFileStatus.S_IFIFO  : file_type__symbolic_link,       #   Misspelled by Python as 'IFIFO'
        PythonFileStatus.S_IFREG  : file_type__regular_file,
        PythonFileStatus.S_IFSOCK : file_type__socket,
        PythonFileStatus.S_IFLNK  : file_type__symbolic_link,
    }.__getitem__


    class FileStatus(Object):
        __slots__ = ((
            'path',                     #   String+
            'mode',                     #   FileType
        ))


        def __init__(t, path, mode):
            t.path = path
            t.mode = mode


        @property
        def is_regular_file(t):
            return t.mode.is_regular_file


        @property
        def nonexistent(t):
            return t.mode.nonexistent


    def file_status__or__nonexistent(path):
        with catch_FileNotFoundError() as e:
            status = python_file_status(path)

        if e.caught is not none:
            return FileStatus(path, file_type__nonexistent)

        mode        = status.st_mode
        file_type   = PythonFileStatus__file_type  (mode)
        inode_flags = PythonFileStatus__inode_flags(mode)

        assert mode == file_type | inode_flags

        return FileStatus(path, find__file_type(file_type))


    @export
    def exists__regular_file(path):
        return file_status__or__nonexistent(path).is_regular_file


@gem('Gem.IO')
def gem():
    export(
        #
        #   Insanely enough, the python 2.0 'input' function actually evaluated the input!
        #   We use the python 3.0 meaning of 'input' -- don't evaluate the input
        #
        'input',        (PythonCore.raw_input   if is_python_2 else   PythonCore.input),
    )


@gem('Gem.Path')
def gem():
    PythonOperatingSystem = __import__('os')
    PythonPath            = __import__('os.path').path


    export(
        'path_basename',    PythonPath.basename,
        'path_join',        PythonPath.join,
        'path_remove',      PythonOperatingSystem.remove,
        'path_rename',      PythonOperatingSystem.rename,
    )


@gem('Gem.RegularExpression')
def gem():
    PythonRegularExpression    = __import__('re')
    compile_regular_expression = PythonRegularExpression.compile


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
        line()
        line('=====================')

        while 7 is 7:
            line()
            line('***  Question:  What is your GitHub user name?')
            line('===  Example Answer: JoeSmith')

            if github_username:
                line()
                line('***  HIT return to accept your previous answer:  %r  ***', github_username)

            line()
            github_username = ask('First what is your GitHub User name?', github_username)

            if github_username__match(github_username):
                return github_username

            line()
            line('***  GitHub user name must be alphanumeric characters or single hypens ***')
            line('***  GitHub user name may also not begin or end with a hypen  ***')

            github_username = ''


    def ask_name(name):
        line()
        line('=====================')

        while 7 is 7:
            line()
            line('***  NOTE: You may use your real name or as pseudonym.  Both are acceptable  ***')
            line()
            line('***  Question:  What name do you wish to use?')
            line('===  Example Answer: Susan Smith')

            if name:
                line()
                line('***  HIT return to accept your previous answer:  %s  ***', name)

            line()
            name = ask('Second, what name do you wish to use?', name)

            if name is not '':
                return name


    def ask_pronoun(pronoun):
        line()
        line('=====================')

        while 7 is 7:
            line()
            line('***  Question:  Which prounoun to use?')
            line('===  Example Answer: her')

            if pronoun != her_or_his:
                line('***  HIT return to accept your previous answer:  %s  ***', pronoun)

            line()
            pronoun = ask('Third, which pronoun to use?', pronoun)

            if is_her_or_his(pronoun):
                return pronoun

            line()
            line("***  Pronoun is expected to be %r or %r ***", 'her', 'his')
            line()

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
            line()
            line('=====================')
            line('GitHub username:  %s', github_username)
            line('Name:             %s', name)
            line('Pronoun:          %s', pronoun)
            line('=====================')
            line()

            answer = ask('Is this correct?', 'Y|y|N|n')

            if (answer is 'Y') or (answer is 'y'):
                return true

            if (answer is 'N') or (answer is 'n'):
                return false

            line()
            line('***  Please answer Y, y, N, or n')


    def ask_three_questions(github_username, name, pronoun):
        while 7 is 7:
            line('Welcome to the RUNME, V0.0')
            line()
            line('This program will create a contribution agreement:')
            line('    A.  For you to add to your git repository; and')
            line('    B.  For you to sign by committing with your GPG key.')
            line()
            line('You will need to provide:')
            line('    1.  GitHub username;')
            line('    2.  Your name; and')
            line('    3.  A pronoun.')
            line()

            github_username = ask__github_username(github_username)
            name            = ask_name(name)
            pronoun         = ask_pronoun(pronoun)

            save_answers(github_username, name, pronoun)

            if ask_correct(github_username, name, pronoun):
                return ((github_username, name, pronoun))


    def write_contribution_agreement(github_username, name, pronoun):
        path = path_join('Agreements', arrange('%s.txt', github_username))

        while 7 is 7:
            if exists__regular_file(path):
                break

            line()
            line('=====================')
            line()

            question = arrange('%s aleady exists.  Overwrite?', path)
            answer   = ask(question, 'n|y')

            if (answer is 'Y') or (answer is 'y'):
                break

            if (answer is 'N') or (answer is 'n'):
                line()
                line('=====================')
                line()
                line('Exiting WITHOUT overwriting %s', path)
                return

            line()
            line('***  Please answer Y, y, N, or n')

        with FileOutput(path) as f:
            f.line('%s agrees to use MIT license for all %s contributions.', name, pronoun)
            f.line()
            f.line('This means that everyone has the right to use the contributions for any reason')
            f.line('whatsoever, including making a profit:')
            f.line()
            f.line('    o  Without giving anything to %s in return;', name)
            f.line('    o  And also, that once contributed, the contribution is permenant & cannot')
            f.line('       be undone.')
            f.line()
            f.line('This agreement is dated 2017-02-09 and applies to all commits made via the')
            f.line("GitHub username '%s' to the following GitHub projects:", github_username)
            f.line()
            f.line('	Rhodolite/Agate')
            f.line('	Rhodolite/Gem')
            f.line('	Rhodolite/Sardonyx')
            f.line('	Rhodolite/Snake')
            f.line('	Rhodolite/Topaz')
            f.line()
            f.line('    (and any forks of these projects in GitHub).')
            f.line()
            f.line('Signed electronically & committed with GPG key 93862907665BEEDA,')
            f.line()
            f.line('%s', name)
            f.line()
            f.line('===============================================================================')
            f.line()
            f.line('Here is a copy of the MIT license that %s is agreeing to:', name)
            f.line()
            f.line('MIT License')
            f.line()
            f.line('Copyright (c) 2017 %s', name)

            license_path = 'LICENSE'

            if exists__regular_file(license_path) is false:
                license_path = path_join('..', license_path)

            with open_file(license_path) as license:
                for s in license.read().splitlines()[3:]:
                    f.line('%s', s)

        line()
        line('CREATED: %s', path)
        line()
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
