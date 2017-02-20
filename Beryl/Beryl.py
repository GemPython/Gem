#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
def boot(module_name):
    def execute(f):
        return f()

    return execute


@boot('Boot')
def boot():
    from sys     import path    as module_path
    from os.path import abspath as path_absolute, join as path_join

    module_path.insert(1, path_absolute(path_join(module_path[0], '..')))


    import Gem


#
#   The three main functions:
#
#
#   1.  main('Main')
#           The wrapper that for all functions defined 'Main' Module.  Defined in Gem.Boot
#
#           In addition to doing the standard wrapping, also calls the 'Main.main' function after the
#           'Main' module is instantiated.
#
#
#   2.  @main('Main')
#       def main():
#           This function instantiates the Main module.
#
#           It is reponsible for exporting a 'main' function to the 'Main' module.
#
#
#   3.  @export
#       def main():
#           The actual main function.  Exported to the 'Main' module.
#
#           This funtion is automatically executed after the 'Main' module is instantiated.
#
@main('Main')
def main():
    require_gem('Gem.ExecuteFile')
    require_gem('Gem.FileOutput')
    require_gem('Gem.FileStatus')
    require_gem('Gem.IO')
    require_gem('Gem.Path')
    require_gem('Gem.RegularExpression')


    from Gem import execute_python_from_file, exists__regular_file, FileOutput
    from Gem import input, make_match_function, path_join, privileged_2
    from Gem.Privileged import open_file


    her_or_his    = 'her|his'
    is_her_or_his = FrozenSet(['her', 'his']).__contains__


    github_username__match = make_match_function(r'[0-9A-Za-z]+(?:-[0-9A-Za-z]+)*\Z')


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

            if (answer == 'Y') or (answer == 'y'):
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

            if (answer == 'Y') or (answer == 'y'):
                return true

            if (answer == 'N') or (answer == 'n'):
                return false

            line('')
            line('***  Please answer Y, y, N, or n')


    def ask_three_questions(github_username, name, pronoun):
        while 7 is 7:
            line('Welcome to the Beryl, V0.0')
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


    @privileged_2
    def write_contribution_agreement(github_username, name, pronoun):
        path = path_join('Agreements', arrange('%s.txt', github_username))

        while 7 is 7:
            if not exists__regular_file(path):
                break

            line('')
            line('=====================')
            line('')

            question = arrange('%s aleady exists.  Overwrite?', path)
            answer   = ask(question, 'n|y')

            if (answer == 'Y') or (answer == 'y'):
                break

            if (answer == 'N') or (answer == 'n'):
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

            license_path = 'LICENSE'

            if exists__regular_file(license_path) is false:
                license_path = path_join('..', license_path)

            with open_file(license_path) as license:
                for s in license.read().splitlines()[3:]:
                    f.line('%s', s)

        line('')
        line('CREATED: %s', path)
        line('')
        line('Please EDIT the GPG key to the key you will sign with')


    @export
    def main():
        if exists__regular_file('Answers.py'):
            Answers = execute_python_from_file('Answers.py')

            github_username = Answers.github_username
            name            = Answers.name
            pronoun         = Answers.pronoun
        else:
            github_username = ''
            name            = ''
            pronoun         = her_or_his

        [github_username, name, pronoun] = ask_three_questions(github_username, name, pronoun)

        write_contribution_agreement(github_username, name, pronoun)
