#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Core')
def gem():
    require_gem('Gem.Path')


    from Gem import read_text_from_path


    share(
        #
        #   Imported functions
        #
        'read_text_from_path',   read_text_from_path,
    )
