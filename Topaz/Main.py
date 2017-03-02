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
    require_gem('Gem.Exception')
    require_gem('Gem.RawString_2')


    from Gem import portray_raw_string, raise_value_error


    @share
    def main():
        for [s, expected] in [
                [   r'',                            "r''"                               ],
                [   'backslash: \\',                portray('backslash: \\')            ],
                [   r'test',                        r"r'test'"                          ],
                [   r'double backslash: \\',        r"r'double backslash: \\'"          ],
                [   r"\'",                          r'''r"\'"'''                        ],
                [   r"ending single quote '",       r'''r"ending single quote '"'''     ],

                [   r"can't",                       r'''r"can't"'''                     ],
                [   r"'",                           r'''r"'"'''                         ],
                [   r"quoted: ''",                  r'''r"quoted: ''"'''                ],
                [   r'''\"'\"''',                   r"""r'''\"'\"'''"""                 ],

                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly
                #       parse it.
                #
                [   r"lots of ''''' - lots!",       """r"lots of ''''' - lots!""" + '"' ],
                [   r'She said "hello"',            r"""r'She said "hello"'"""          ],
                [   r'"',                           r"""r'"'"""                         ],
                [   r'double quoted: ""',           r"""r'double quoted: ""'"""         ],
                [   r"""\'"\'""",                   r'''r"""\'"\'"""'''                 ],

                #
                #   5 = saw a """
                #
                #   NOTE:
                #       vim 7.4 gets confused with '''x\'''' - so use string concatanation so vim can properly
                #       parse it.
                #
                [   r'lots of """"" - lots!',       '''r'lots of """"" - lots!''' + "'" ],

                #<special-cases>
                #
                #   Begin with " & has ''' internally
                #
                [   '''"triple" is: ''\'.''',       portray('''"triple" is: ''\'.''')   ],
                #
                #   Begin with " & more ' than "
                #
                [   r'''"'' ''"!''',                r"""r'''"'' ''"!'''"""              ],
                #
                #   End with " & has ''' internally
                #
                [   '''three: "''\'."''',           portray('''three: "''\'."''')       ],
                #
                #   End with " & more ' than "
                #
                [   r'''Wow: ''"''',                r"""r'''Wow: ''"'''"""              ],
                #
                #   Begin with ' & has """ internally
                #
                [   """'triple' is: ""\".""",       portray("""'triple' is: ""\".""")   ],
                #
                #   Begin with ' & more " than '
                #
                [   r"""'"" ""'2""",                r'''r"""'"" ""'2"""'''              ],
                #
                #   End with ' & has """ internally
                #
                [   """3: '""\".'""",               portray("""3: '""\".'""")           ],
                #
                #   End with ' & more " than '
                #
                [   r"""End with "'": "'""",       r'''r"""End with "'": "'"""'''       ],
                #</special-cases>

                #
                #   3  = saw a ' & a "
                #       9  = last saw "
                #       10 = last saw ""
                #       11 = last saw '
                #
                [   r'''the quotes: ' & "''',       r"""r'''the quotes: ' & "'''"""     ],
                [   r"""single: ', '' .vs. "?""",   r'''r"""single: ', '' .vs. "?"""''' ],
                [   r'''singles "'" & "''"''',      r"""r'''singles "'" & "''"'''"""    ],
                [   r'''more quotes: '' & ""''',    r"""r'''more quotes: '' & ""'''"""  ],
                [   r"""other way: " & '""",        r'''r"""other way: " & '"""'''      ],
                [   r"""prefer ", "", ', or ''""",  r'''r"""prefer ", "", ', or ''"""'''],

                #
                #   5 = saw a ''' & "
                #
                [   r"""more '''' than "!""",      '''r"""more ''\'' than "!"""''',     ],
                [   r"""l""s '''' t""n "!""",      '''r"""l""s ''\'' t""n "!"""''',     ],

                #
                #   7 = saw a """ & '
                #
                [   r'''more """" than '!''',      """r'''more ""\"" than '!'''""",     ],
                [   r'''l''s """" t''n '!''',      """r'''l''s ""\"" t''n '!'''""",     ],
        ]:
            actual = portray_raw_string(s)

            if actual != expected:
                line('%r', s)
                line('  actual:   %s', actual)
                line('  expected: %s', expected)

                raise_value_error('portray_raw_string(%r): %r (expected: %r)', s, actual, expected)
