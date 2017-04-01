#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Pattern')
def gem():
    require_gem('Sapphire.Core')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.CreateMatch')


    from Tremolite import DOT, END_OF_PATTERN


    @share
    def create_sapphire_match():
        MATCH('comment', '#' + DOT + END_OF_PATTERN)
