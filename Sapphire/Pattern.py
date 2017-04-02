#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Sapphire.Pattern')
def gem():
    require_gem('Sapphire.Core')
    require_gem('Tremolite.Build')
    require_gem('Tremolite.CreateMatch')
    require_gem('Tremolite.Name')


    from Tremolite import create_match_code, ANY_OF, BACKSLASH, DOT, EMPTY, END_OF_PATTERN, EXACT, FULL_MATCH
    from Tremolite import GROUP, LINEFEED, MATCH, NAME, NAMED_GROUP, NOT_FOLLOWED_BY
    from Tremolite import ONE_OR_MORE, OPTIONAL, OPTIONAL_GROUP, PRINTABLE, PRINTABLE_MINUS, ZERO_OR_MORE


    @share
    def create_sapphire_match():
        ow  = ZERO_OR_MORE(' ')
        ow1 = NAMED_GROUP('ow1', ow)
        w   = ONE_OR_MORE(' ')
        w1  = NAMED_GROUP('w1', w)
        w2  = NAMED_GROUP('w2', w)

        alphanumeric_or_underscore = NAME('alphanumeric_or_underscore', ANY_OF('0-9', 'A-Z', '_', 'a-z'))

        identifier = NAME('identifier', ANY_OF('A-Z', '_', 'a-z') + ZERO_OR_MORE(alphanumeric_or_underscore))
        name_1     = NAMED_GROUP('name_1', identifier)
        name_2     = NAMED_GROUP('name_2', identifier)
        name_3     = NAMED_GROUP('name_3', identifier)

        single_quote = NAMED_GROUP(
                           'single_quote',
                           (
                                "'" + ONE_OR_MORE(BACKSLASH + PRINTABLE | PRINTABLE_MINUS("'", '\\')) + "'"
                                    | ("''" + NOT_FOLLOWED_BY("'"))
                           )
                       )

        left_parenthesis         = NAMED_GROUP('left_parenthesis',         ow + '(' + ow)
        right_parenthesis        = NAMED_GROUP('right_parenthesis',        ow + ')' + ow)
        right_parenthesis__colon = NAMED_GROUP('right_parenthesis__colon', ow + ')' + ow + ':')
        #pair_of_parenthesis      = NAMED_GROUP('pair_of_parenthesis',      ow + '(' + ow + ')' + ow)

        keyword__ow = NAMED_GROUP(
                          'keyword__ow',
                          (
                              GROUP(
                                  'keyword',
                                  '@' | (EXACT('def') | 'return') + NOT_FOLLOWED_BY(alphanumeric_or_underscore)
                              )
                                  + ow
                          ),
                      )

        comment = NAME('comment', '#' + GROUP('comment', ZERO_OR_MORE(DOT)))

        MATCH(
            'line_match',
            NAMED_GROUP('indented', ow)
                + (
                      keyword__ow + OPTIONAL(GROUP('newline_1', LINEFEED) + END_OF_PATTERN)
                    | (comment | EMPTY) + GROUP('newline_2', LINEFEED) + END_OF_PATTERN
                  )
        )

        FULL_MATCH(
            'define_1_match',
            name_1 + left_parenthesis + OPTIONAL(name_2) + right_parenthesis__colon + LINEFEED,
        )

        FULL_MATCH(
            'expression_match',
            name_1 + OPTIONAL(left_parenthesis + OPTIONAL(single_quote) + right_parenthesis) + LINEFEED,
        )
 
        create_match_code('../Sapphire/Match.py', '2017 Amit Green', 'Sapphire.Match')
