#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Topaz.Path')
def gem():
    require_gem('Gem.Path')
    require_gem('Topaz.Core')


    from Gem import remove_path__ignore_file_not_found, rename_path__ignore_file_not_found


    @share
    def test_remove_path():
        r = remove_path__ignore_file_not_found('nonexistent')

        assert r is false

        line('PASSED: remove_path')


    @share
    def test_rename_path():
        r = rename_path__ignore_file_not_found('nonexistent', 'even-more-nonexistent')

        assert r is false

        line('PASSED: rename_path')
