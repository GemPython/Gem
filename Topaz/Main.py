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
    require_gem('Gem.PortrayString')


    from Gem import portray_raw_string, raise_value_error


    @share
    def main():
        for [s, expected] in [
                [   r'',                            "r''"                               ],
                [   r'test',                        r"r'test'"                          ],
                [   r'double backslash: \\',        r"r'double backslash: \\'"          ],
                [   r"\'",                          r'''r"\'"'''                        ],
                [   r"ending single quote '",       r'''r"ending single quote '"'''     ],
                [   r"can't",                       r'''r"can't"'''                     ],
                [   r"'",                           r'''r"'"'''                         ],
                [   r"quoted: ''",                  r'''r"quoted: ''"'''                ],
                [   r'''\"'\"''',                   r"""r'''\"'\"'''"""                 ],
                [   r'She said "hello"',            r"""r'She said "hello"'"""          ],
                [   r'"',                           r"""r'"'"""                         ],
                [   r'double quoted: ""',           r"""r'double quoted: ""'"""         ],
                [   r"""\'"\'""",                   r'''r"""\'"\'"""'''                 ],
                [   r'''"triple" is: ''\'.''',      r'''r""""triple" is: ''\'."""'''    ],
                [   r'''"'' ''"!''',                r'''r""""'' ''"!"""'''              ],
                [   r'''Wow: ''"''',                r"""r'''Wow: ''"'''"""              ],
                [   r''''triple' is: ""\".''',      r"""r''''triple' is: ""\".'''"""    ],
                [   r''''"" ""'2''',                r"""r''''"" ""'2'''"""              ],
                [   r"""End with "'": "'""",        r'''r"""End with "'": "'"""'''      ],
                [   r'''the quotes: ' & "''',       r"""r'''the quotes: ' & "'''"""     ],
                [   r"""single: ', '' .vs. "?""",   r'''r"""single: ', '' .vs. "?"""''' ],
                [   r'''singles "'" & "''"''',      r"""r'''singles "'" & "''"'''"""    ],
                [   r'''more quotes: '' & ""''',    r"""r'''more quotes: '' & ""'''"""  ],
                [   r"""other way: " & '""",        r'''r"""other way: " & '"""'''      ],
                [   r"""prefer ", "", ', or ''""",  r'''r"""prefer ", "", ', or ''"""'''],

                #
                #   Have to represent what we "expect" using \' or \" internally
                #
                [   r"""more '''' than "!""",      '''r"""more ''\'' than "!"""''',     ],
                [   r"""l""s '''' t""n "!""",      '''r"""l""s ''\'' t""n "!"""''',     ],
                [   r'''more """" than '!''',      """r'''more ""\"" than '!'''""",     ],
                [   r'''l''s """" t''n '!''',      """r'''l''s ""\"" t''n '!'''""",     ],

                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" & '''x\'''' - so use string concatanation so
                #       vim can properly parse it.
                #
                [   r"lots of ''''' - lots!",       """r"lots of ''''' - lots!""" + '"' ],
                [   r'lots of """"" - lots!',       '''r'lots of """"" - lots!''' + "'" ],

                #
                #<have-to-use-normal-portray>
                #
                #   Ends in backslash
                #
                [   'backslash: \\',                portray('backslash: \\')            ],
                #
                #   End with " & has ''' internally
                #
                [   '''\'333: "''\'."''',           portray('''\'333: "''\'."''')       ],
                [   '''three: "''\'."''',           portray('''three: "''\'."''')       ],
                #
                #   End with ' & has """ internally
                #
                [   """\': '""\".'""",              portray("""\': '""\".'""")          ],
                [   """\'\\'""\".'""",              portray("""\'\\'""\".'""")          ],
                [   """3: '""\".'""",               portray("""3: '""\".'""")           ],
                #<have-to-use-normal-portray>

        ]:
            actual = portray_raw_string(s)

            if actual != expected:
                line('%r', s)
                line('  actual:   %s', actual)
                line('  expected: %s', expected)

                raise_value_error('portray_raw_string(%r): %r (expected: %r)', s, actual, expected)

        line('PASSED: portray_raw_string')
