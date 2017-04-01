#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Pattern')
def gem():
    require_gem('Sapphire.Core')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.CreateMatch')


    from Tremolite import create_match_code, DOT, END_OF_PATTERN, MATCH, OPTIONAL_GROUP, ZERO_OR_MORE



    @share
    def create_sapphire_match():
        MATCH('comment_match', OPTIONAL_GROUP('comment', '#') + ZERO_OR_MORE(DOT) + END_OF_PATTERN)
        create_match_code('../Sapphire/Match.py', '2017 Amit Green', 'Sapphire.Match')
