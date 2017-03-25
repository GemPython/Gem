#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Topaz.Pattern')
def gem():
    require_gem('Topaz.Core')
    require_gem('Tremolite.Build')


    from Tremolite import ANY_OF, END_OF_PATTERN, EMPTY, EXACT, GROUP
    from Tremolite import MINIMUM_OF_ONE_OR_MORE, MINIMUM_OF_OPTIONAL, MINIMUM_OF_REPEAT_OR_MORE, MINIMUM_OF_ZERO_OR_MORE
    from Tremolite import ONE_OR_MORE, OPTIONAL, REPEAT, ZERO_OR_MORE


    @share
    def test_pattern():
        for [pattern, test] in [
                [   OPTIONAL('bc') + OPTIONAL('d' | EXACT('hi') + 'j') + 'x' + END_OF_PATTERN,      'hijx'      ],
                [   'x' + ('lemo' + ANY_OF('a-z') | GROUP('abc', 'y')) + END_OF_PATTERN,            'xy'        ],
                [   'x' + GROUP('abc', ANY_OF('a-z', 'A-Z')) + GROUP('z', 'z') + END_OF_PATTERN,    'xYz'       ],
                [   OPTIONAL('a') + ONE_OR_MORE('x') + ZERO_OR_MORE('yz') + END_OF_PATTERN,         'xx'        ],
                [   'a' + (EXACT('b') | r'c\i') + 'd' + ONE_OR_MORE('e' | EMPTY) + END_OF_PATTERN,  r'ac\id'    ],
                [   'x' + MINIMUM_OF_OPTIONAL('y') + MINIMUM_OF_ONE_OR_MORE('z') + END_OF_PATTERN,  'xzz'       ],
                [   MINIMUM_OF_ZERO_OR_MORE('x') + REPEAT('yz', 2, 3) + END_OF_PATTERN,             'yzyzyz'    ],
                [   MINIMUM_OF_REPEAT_OR_MORE('x' | EXACT('z'), 0) + 'y' + END_OF_PATTERN,          'xzxy'      ],
        ]:
            #line('%s', pattern)
            #line('%r', pattern)

            compiled = pattern.compile_ascii_regular_expression()
            m        = compiled.match(test)

            #line('  %s %r', portray_string(m.group()), m.groups())
            #line()

        line('PASSED: pattern')
