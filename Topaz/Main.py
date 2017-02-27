#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
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


@gem('Topaz.Main')
def gem():
    require_gem('Gem.RawString')


    from Gem import portray_raw_string, raise_value_error


    @share
    def main():
        for [s, expected] in [
                [   r'',                            "r''"                               ],

                #   
                #   8  = last saw \
                #
                [   'backslash: \\',                portray('backslash: \\')            ],  #   0,8,0

                #
                #   0 = no ' or " seen
                #
                [   r'test',                        r"r'test'"                          ],  #   0,0,0
                [   r'double backslash: \\',        r"r'double backslash: \\'"          ],  #   0,0,0
                [   r"\'",                          r'''r"\'"''',                       ],  #   0,0,-1

                #
                #   1 = saw a '
                #       11 = last saw '
                #       12 = last saw ''
                #
                [   r"can't",                       r'''r"can't"'''                     ],  #   1,0,-1
                [   r"'",                           r'''r"'"'''                         ],  #   1,11,-1
                [   r"quoted: ''",                  r'''r"quoted: ''"'''                ],  #   1,12,-2
                [   r"\"'\"",                       r'''r"\"'\""''',                    ],  #   1,0,1

                #
                #   4 = saw a '''
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly
                #       parse it.
                #
                [   r"lots of ''''' - lots!",       """r"lots of ''''' - lots!""" + '"' ],  #   4,0,-5

                #
                #   2 = saw a "
                #       9  = last saw "
                #       10 = last saw ""
                #
                [   r'She said "hello"',            r"""r'She said "hello"'"""          ],  #   2,9,2
                [   r'"',                           r"""r'"'"""                         ],  #   2,9,1
                [   r'double quoted: ""',           r"""r'double quoted: ""'"""         ],  #   2,10,2
                [   r'\'"\'',                       r"""r'\'"\''""",                    ],  #   2,0,-1

                #
                #   5 = saw a """
                #
                #   NOTE:
                #       vim 7.4 gets confused with '''x\'''' - so use string concatanation so vim can properly
                #       parse it.
                #
                [   r'lots of """"" - lots!',       '''r'lots of """"" - lots!''' + "'" ],  #   6,0,5

                #<special-cases>
                #
                #   Begin with " & has ''' internally
                #
                [   '''"triple" is: ''\'.''',       portray('''"triple" is: ''\'.''')   ],  #   5,0,-1
                #
                #   Begin with " & more ' than "
                #
                [   r'''"'' ''"!''',                r"""r'''"'' ''"!'''"""              ],  #   3,0,-2
                #
                #   End with " & has ''' internally
                #
                [   '''three: "''\'."''',           portray('''three: "''\'."''')       ],  #   5,9,-1
                #
                #   End with " & more ' than "
                #
                [   r'''Wow: ''"''',                r"""r'''Wow: ''"'''"""              ],  #   3,9,-1
                #
                #   Begin with ' & has """ internally
                #
                [   """'triple' is: ""\".""",       portray("""'triple' is: ""\".""")   ],  #   7,0,1
                #
                #   Begin with ' & more " than '
                #
                [   r"""'"" ""'2""",                r'''r"""'"" ""'2"""'''              ],  #   3,0,2
                #
                #   End with ' & has """ internally
                #
                [   """3: '""\".'""",               portray("""3: '""\".'""")           ],  #   7,11,1
                #
                #   End with ' & more " than '
                #
                [   r"""End with "'": "'""",       r'''r"""End with "'": "'"""'''       ],  #   3,11,1
                #</special-cases>

                #
                #   3  = saw a ' & a "
                #       9  = last saw "
                #       10 = last saw ""
                #       11 = last saw '
                #
                [   r'''the quotes: ' & "''',       r"""r'''the quotes: ' & "'''"""     ],  #   3,9,0
                [   r"""single: ', '' .vs. "?""",   r'''r"""single: ', '' .vs. "?"""''' ],  #   3,0,-2
                [   r'''singles "'" & "''"''',      r"""r'''singles "'" & "''"'''"""    ],  #   3,9,1
                [   r'''more quotes: '' & ""''',    r"""r'''more quotes: '' & ""'''"""  ],  #   3,10,0
                [   r"""other way: " & '""",        r'''r"""other way: " & '"""'''      ],  #   3,11,1
                [   r"""prefer ", "", ', or ''""",  r'''r"""prefer ", "", ', or ''"""'''],  #   3,12,0

                #
                #   5 = saw a ''' & "
                #
                [   r"""more '''' than "!""",      '''r"""more ''\'' than "!"""''',     ],  #   5,0,-3
                [   r"""l""s '''' t""n "!""",      '''r"""l""s ''\'' t""n "!"""''',     ],  #   5,0,1

                #
                #   7 = saw a """ & '
                #
                [   r'''more """" than '!''',      """r'''more ""\"" than '!'''""",     ],  #   7,0,3
                [   r'''l''s """" t''n '!''',      """r'''l''s ""\"" t''n '!'''""",     ],  #   7,0,-1
        ]:
            actual = portray_raw_string(s)

            if actual != expected:
                line('  %s', actual)
                line('  %s', expected)

                raise_value_error('portray_raw_string(%r): %r (expected: %r)', s, actual, expected)
