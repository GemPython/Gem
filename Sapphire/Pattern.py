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
        name_3     = NAMED_GROUP('name_3', identifier)

        left_parenthesis         = NAME('left_parenthesis', ow + '(' + ow)
        right_parenthesis        = NAME('right_parenthesis', ow + ')' + ow)
        right_parenthesis__colon = NAME('right_parenthesis__colon', ow + ')' + ow + ':')
        pair_of_parenthesis      = left_parenthesis + right_parenthesis
        keyword_define           = NAMED_GROUP('keyword_define', 'def' + w)
        keyword_return           = NAMED_GROUP('keyword_return', 'return' + ow)

        comment = NAME('comment', '#' + GROUP('comment', ZERO_OR_MORE(DOT)))

        define_1 = NAME(
                       'define_1',
                       keyword_define
                           + name_1
                           + GROUP('define__left_parenthesis', left_parenthesis)
                           + name_2
                           + GROUP('define__right_parenthesis__colon', right_parenthesis__colon)
                   )

        return_name = NAME(
                          'return_name',
                          keyword_return
                              + GROUP('return__name_1', identifier)
                              + OPTIONAL_GROUP('return__pair_of_parenthesis', pair_of_parenthesis)
                     )

        FULL_MATCH('line_match', ow1 + (comment | define_1 | return_name | EMPTY))
 
        create_match_code('../Sapphire/Match.py', '2017 Amit Green', 'Sapphire.Match')
