#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Pattern')
def gem():
    require_gem('Sapphire.Core')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.CreateMatch')
    require_gem('Tremolite.Name')


    from Tremolite import create_match_code, ANY_OF, DOT, EMPTY, FULL_MATCH, GROUP, NAME, NAMED_GROUP
    from Tremolite import ONE_OR_MORE, OPTIONAL, OPTIONAL_GROUP, ZERO_OR_MORE


    @share
    def create_sapphire_match():
        ow  = ZERO_OR_MORE(' ')
        ow1 = NAMED_GROUP('ow1', ow)
        w   = ONE_OR_MORE(' ')
        w1  = NAMED_GROUP('w1', w)
        w2  = NAMED_GROUP('w2', w)

        identifier = NAME('identifier', ANY_OF('A-Z', '_', 'a-z') + ZERO_OR_MORE(ANY_OF('0-9', 'A-Z', '_', 'a-z')))
        name_1     = NAMED_GROUP('name_1', identifier)
        name_2     = NAMED_GROUP('name_2', identifier)

        left_parenthesis         = NAMED_GROUP('left_parenthesis', ow + '(' + ow)
        right_parenthesis__colon = NAMED_GROUP('right_parenthesis__colon', ow + ')' + ow + ':' + ow)
        keyword_define           = NAMED_GROUP('keyword_define', 'def' + w)

        comment  = NAME('comment', '#' + GROUP('comment', ZERO_OR_MORE(DOT)))
        define_1 = NAME('define_1', keyword_define + name_1 + left_parenthesis + name_2 + right_parenthesis__colon)

        FULL_MATCH('line_match', ow1 + (comment | define_1 | EMPTY))
 
        create_match_code('../Sapphire/Match.py', '2017 Amit Green', 'Sapphire.Match')
