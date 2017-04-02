#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Core')
def gem():
    require_gem('Gem.Cache')
    require_gem('Gem.Path')


    from Gem import produce_cache_functions, read_text_from_path


    share(
        #
        #   Imported functions
        #
        'produce_cache_functions',    produce_cache_functions,
        'read_text_from_path',        read_text_from_path,
    )
