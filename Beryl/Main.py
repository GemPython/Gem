#
#   Copyright (c) 2017 Amit Green & Mike Zhukovskiy.  All rights reserved.
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


@gem('Beryl.Main')
def gem():
    require_gem('Beryl.BerylAnswer')
    require_gem('Gem.ExecuteFile')
    require_gem('Gem.FileStatus')


    from Gem import execute_python_from_file, exists__regular_file


    @share
    def main():
        if exists__regular_file('Answers.py'):
            Answers = execute_python_from_file('Answers.py')

            github_username = Answers.github_username
            name            = Answers.name
            pronoun         = Answers.pronoun
            gpg_key         = Answers.gpg_key
        else:
            github_username = ''
            gpg_key         = ''
            name            = ''
            pronoun         = her_or_his

        answers = BerylAnswer(github_username, name, pronoun, gpg_key)

        answers.ask_four_questions()
        answers.write_contribution_agreement()
