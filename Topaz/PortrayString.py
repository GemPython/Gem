#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Topaz.PortrayString')
def gem():
    require_gem('Topaz.Core')
    require_gem('Gem.PortrayString')


    from Gem import N_N, portray_raw_string, portray_string


    def test_portray_raw_string__raw_string():
        saw_2 = false

        for row in [
            #<A_A>
                #
                #   A_A: ra
                #
                [   r"wink \"\"'",                  r'''r"wink \"\"'"'''                        ],

                #
                #   A_A: rq
                #
                [
                    "ending single quote '",
                    r'''r"ending single quote '"''',
                    '''"ending single quote '"''',
                ],
                [
                    "'",
                    r'''r"'"''',
                    '''"'"''',
                ],

                #
                #   A_A/AQ_A: lemon: kc
                #   A_A/AQ_A: lemon: ks: not possible   (''' not allowed)
                #
                [   """wi\nk \\"\\"'""",            r'''"""wi\nk \\"\\"'"""'''                  ],

                #
                #   A_A: backslash: kc/ks: not possible (always raw mode)
                #   A_A: pc/ps:            not possible (always raw mode)
                #
            #</A_A>

            #<A_B>
                #
                #   A_B: ra
                #
                [   r"\"two apostrophe\": ''",      r'''r"\"two apostrophe\": ''"'''            ],

                #
                #   A_B: rq
                #
                [
                    "quoted: ''",
                    r'''r"quoted: ''"''',
                    '''"quoted: ''"''',
                ],

                #
                #   A_B/AQ_B: lemon: kc
                #   A_B/AQ_B, lemon: ks: not possible (''' not allowed)
                #
                [   """wo\nk \\"\\"''""",           r'''"""wo\nk \\"\\"''"""'''                 ],

                #
                #   A_B: backslash: kc/ks: not possible (always raw mode)
                #   A_B: pc/ps:            not possible (always raw mode)
                #
            #</A_B>

            #<A_K>
                #
                #   A_K/A_N: ra/rq:         not possible (ends in \)
                #   A_K/A_N: lemon: kc
                #   A_K/A_N: lemon: ks: not possible (''' not allowed)
                #
                [   "le'mo\n\\",                    portray("le'mo\n\\")                        ],

                #
                #   A_K/A_N: backslash: kc
                #   A_K/A_N: backslash: ks: not possible (''' not allowed)
                #
                [   "apostrophe & backlash: '\\",   portray("apostrophe & backlash: '\\")       ],

                #
                #   A_K: pc/ps: not possible (always backslash)
                #
            #</A_K>

            #<A_N>
                #
                #   A_N: ra
                #
                #       NOTE: Ends in ", which is a little confusing.  We could theoretically use ''', hence:
                #             r'''\"'\"''' -- but that doesn't seem much clearer.
                #
                [   r"\"'\"",                       r'''r"\"'\""'''                             ],

                #
                #   A_N: rq
                #
                [
                    "can't",
                    r'''r"can't"''',
                    '''"can't"''',
                ],

                #
                #   A_N: lemon: kc
                #   A_N: lemon: ks (''' not allowed)
                #
                [   "ca\n't",                       portray("ca\n't"),                          ],

                #
                #   A_N: backslash: kc/ks: not possible (always raw mode)
                #   A_N: pc/ps:            not possible (always raw mode)
                #
            #</A_N>

            #<AQ_A>
                #
                #   AQ_A: ra
                #
                [
                    """End with "'": "'""",
                    r'''r"""End with "'": "'"""''',
                    '''"""End with "'": "'"""''',
                ],

                #
                #   AQ_A: rq
                #
                [
                    """other way: '"' & '""",
                    r'''r"""other way: '"' & '"""''',
                    '''"""other way: '"' & '"""''',
                ],

                #
                #   AQ_A: lemon: kc
                #   AQ_A: lemon: ks (''' not allowed)
                #
                [   """"lemo\n's"'""",              r'''"""\"lemo\n's"'"""'''                   ],

                #
                #   AQ_A: backslash: kc/ks: not possible (always raw mode)
                #   AQ_A: pc/ps:            not possible (always raw mode)
                #
            #</AQ_A>

            #<AQ_B>
                #
                #   AQ_B: ra
                #
                [
                    """prefer ", "", ', or ''""",
                    r'''r"""prefer ", "", ', or ''"""''',
                    '''"""prefer ", "", ', or ''"""''',
                ],

                #
                #   AQ_B: rq
                #
                [
                    """prefer ', '', ", or ''""",
                    r'''r"""prefer ', '', ", or ''"""''',
                    '''"""prefer ', '', ", or ''"""''',
                ],

                #
                #   AQ_B: lemon: kc
                #   AQ_B: lemon: ks (''' not allowed)
                #
                [   """"more lemo\n''s"'""",        r'''"""\"more lemo\n''s"'"""'''             ],

                #
                #   AQ_B: backslash: kc/ks: not possible (always raw mode)
                #   AQ_B: pc/ps:            not possible (always raw mode)
                #
            #</AQ_B>

            #<AQ_K>
                #
                #   AQ_K/AQ_N: ra/rq:     not possible (ends in \)
                #   AQ_K/AQ_N: lemon: kc
                #   AQ_K/AQ_N: lemon: ks: not possible (''' not allowed)
                #
                [   '''le'"mo"\n\\''',              r"""'''le'"mo"\n\\'''"""                    ],

                #
                #   AQ_K/AQ_N: backslash: kc
                #   AQ_K/AQ_N: backslash: ks: not possible (''' not allowed)
                #
                [   '''all ", ', & \\''',           r"""'''all ", ', & \\'''"""                 ],

                #
                #   A_QK: pc/ps: not possible (always backslash)
                #
            #</AQ_K>

            #<AQ_N>
                #
                #   AQ_N: ra
                #       """ chosen instead of ''' --- as it starts with a '
                #
                [   r"""'triple' is: ""\".""",      r'''r"""'triple' is: ""\"."""'''            ],
                [
                    """'"" ""'2""",
                    r'''r"""'"" ""'2"""''',
                    '''"""'"" ""'2"""''',
                ],

                #
                #   AQ_N: rq
                #       ''' chosen instead of """ --- as it starts with a "
                #
                [
                    r'''"triple" is: ''\'.''',
                    r"""r'''"triple" is: ''\'.'''""",
                ],

                [
                    r'''"'' ''"!''',
                    r"""r'''"'' ''"!'''""",
                    """'''\"'' ''"!'''""",
                ],

                [
                    """single: ', '' .vs. "?""",
                    r'''r"""single: ', '' .vs. "?"""''',
                    '''"""single: ', '' .vs. "?"""''',
                ],

                #
                #   AQ_N: lemon: kc
                #   AQ_N: lemon: ks (''' not allowed)
                #
                [   """lemo\n''s "yet" again""",    r"""'''lemo\n''s "yet" again'''"""          ],

                #
                #   AQ_N: backslash: kc/ks: not possible (always raw mode)
                #   AQ_N: pc/ps:            not possible (always raw mode)
                #
            #</AQ_N>

            #<AQ_Q>
                #
                #   AQ_Q: ra
                #
                [
                    '''singles "'" & "''"''',
                    r"""r'''singles "'" & "''"'''""",
                    """'''singles "'" & "''"'''""",
                ],
                [
                    '''the quotes: ' & "''',
                    r"""r'''the quotes: ' & "'''""",
                    """'''the quotes: ' & "'''""",
                ],

                #
                #   AQ_Q: rq
                #
                [
                    '''Wow: ''"''',
                    r"""r'''Wow: ''"'''""",
                    """'''Wow: ''"'''""",
                ],

                #
                #   AQ_Q: lemon: kc
                #   AQ_Q: lemon: ks (''' not allowed)
                #
                [   '''lemo\n's are "sour"''',      r"""'''lemo\n's are "sour"'''"""            ],

                #
                #   AQ_Q: backslash: kc/ks: not possible (always raw mode)
                #   AQ_Q: pc/ps:            not possible (always raw mode)
                #
            #</AQ_Q>

            #<AQ_R>
                #
                #   AQ_R: ra
                #
                [
                    '''more quotes: '' & ""''',
                    r"""r'''more quotes: '' & ""'''""",
                    """'''more quotes: '' & ""'''""",
                ],

                #
                #   AQ_R: rq
                #
                [
                    '''compare: ''+'' .vs. ""''',
                    r"""r'''compare: ''+'' .vs. ""'''""",
                    """'''compare: ''+'' .vs. ""'''""",
                ],

                #
                #   AQ_R: lemon: kc
                #   AQ_R: lemon: ks (''' not allowed)
                #
                [   '''yep - lemo\n's ""sour""''',  r"""'''yep - lemo\n's ""sour""'''"""        ],

                #
                #   AQ_R: backslash: kc/ks: not possible (always raw mode)
                #   AQ_R: pc/ps:            not possible (always raw mode)
                #
            #</AQ_R>

            #<AS_A>
                #
                #   AS_A: ra:         not possible (always portray)
                #   AS_A: rq:         not possible (always portray)
                #   AS_A: lemon: kc
                #   AS_A: lemon: ks: not possible (''' not allowed)
                #
                [   """\""\"\tab'""",               r'''"""\""\"\tab'"""'''                     ],

                #
                #   AS_A: backslash: kc
                #   AS_A: backslash: ks: not possible (''' not allowed)
                #
                [   """\""\"\\non-tab'""",          r'''"""\""\"\\non-tab'"""'''                ],

                #
                #   AS_A: pc
                #   AS_A: ps: not possible (''' not allowed)
                #
                [   """': '""\"".'""",              r'''"""': '""\"".'"""'''                    ],
                [   """3: '""\".'""",               r'''"""3: '""\".'"""'''                     ],
            #</AS_A>

            #<AS_B>
                #
                #   AS_B: ra:         not possible (always portray)
                #   AS_B: rq:         not possible (always portray)
                #   AS_B: lemon: kc
                #   AS_B: lemon: ks: not possible (''' not allowed)
                #
                [   """\""\"AS_B\n''""",            r'''"""\""\"AS_B\n''"""'''                  ],

                #
                #   AS_B: backslash: kc
                #   AS_B: backslash: ks: not possible (''' not allowed)
                #
                [   """\""\"\\AS_B''""",            r'''"""\""\"\\AS_B''"""'''                  ],

                #
                #   AS_B: pc
                #   AS_B: ps: not possible (''' not allowed)
                #
                [   """\""\""\"".''""",             r'''"""\""\""\"".''"""'''                   ],
            #</AS_B>

            #<AS_K>
                #
                #   AS_K/AS_N: ra/rq:     not possible (ends in \)
                #   AS_K/AS_N: lemon: kc
                #   AS_K/AS_N: lemon: ks: not possible (''' not allowed)
                #
                [   '''le'"""mo"""\n\\''',          """'''le'""\"mo""\"\\n\\\\'''"""            ],

                #
                #   AS_K/A_N: backslash: kc
                #   AS_K/A_N: backslash: ks: not possible (''' not allowed)
                #
                [   '''all """, ', & \\''',         """'''all ""\", ', & \\\\'''"""             ],

                #
                #   AS_K: pc/ps: not possible (always backslash)
                #
            #</AS_K>

            #<AS_N>
                #
                #   AS_N: ra
                #       Have to represent what we "expect" using \" internally
                #
                [
                    '''more """" than '!''',
                    """r'''more ""\"" than '!'''""",
                    """'''more ""\"" than '!'''""",
                ],

                #
                #   AS_N: rq
                #       Have to represent what we "expect" using \" internally
                #
                [
                    '''l''s """" t''n '!''',
                    """r'''l''s ""\"" t''n '!'''""",
                    """'''l''s ""\"" t''n '!'''""",
                ],

                #
                #   AS_N: lemon: kc
                #   AS_N: lemon: ks: not possible (''' not allowed)
                #       Have to represent what we "expect" using \" internally
                #
                [   '''"""'now' AS_\n''',          """'''""\"'now' AS_\\n'''"""                 ],

                #
                #   AS_N: backslash: kc/ks: not possible (always raw mode)
                #   AS_N: pc/ps:            not possible (always raw mode)
                #
            #</AS_N>

            #<C_A>
                #
                #   C_A: ra - not possible (" not allowed)
                #   C_A: rq
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    "lots of ''''' - more'",
                    """r"lots of ''''' - more'""" + '"',
                    '''"lots of ''\''\' - more'"''',
                ],

                #
                #   C_A:  lemon: kc: not possible (""" not allowed)
                #   C_A:  lemon: ks
                #       Have to represent what we "expect" using \' internally
                #
                [   "'''@C_N + e\nding '",          '''"''\'@C_N + e\\nding '"'''               ],

                #
                #   C_A: backslash: kc/ks: not possible (always raw mode)
                #   C_A: pc/ps:            not possible (always raw mode)
                #
            #</C_A>

            #<C_B>
                #
                #   C_B: ra - not possible (" not allowed)
                #   C_B: rq
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    "lots of ''''' - extra''",
                    """r"lots of ''''' - extra''""" + '"',
                    '''"lots of ''\''\' - extra''"''',
                ],

                #
                #   C_B:  lemon: kc: not possible (""" not allowed)
                #   C_B:  lemon: ks
                #       Have to represent what we "expect" using \' internally
                #
                [   "'''@C_N + 2x e\nding ''",     '''"''\'@C_N + 2x e\\nding ''"'''            ],

                #
                #   C_B: backslash: kc/ks: not possible (always raw mode)
                #   C_B: pc/ps:            not possible (always raw mode)
                #
            #</C_B>

            #<C_C>
                #
                #   C_C: ra - not possible (" not allowed)
                #   C_C: rq
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    "abundance of '''''''",
                    r"""r"abundance of '''''''""" + '"',
                    '''"abundance of ''\''\''\'"''',
                ],

                #
                #   C_C:  lemon: kc: not possible (""" not allowed)
                #   C_C:  lemon: ks
                #       Have to represent what we "expect" using \' internally
                #
                [   "'''C_C is a pali\ndrome'''",   '''"''\'C_C is a pali\\ndrome''\'"'''       ],

                #
                #   C_C: backslash: kc/ks: not possible (always raw mode)
                #   C_C: pc/ps:            not possible (always raw mode)
                #
            #</C_C>

            #<C_K>
                #
                #   C_K/C_N: ra/rq:     not possible (ends in \)
                #   C_K/C_N: lemon: kc: not possible (""" not allowed)
                #   C_K/C_N: lemon: ks
                #
                [   "''''Super\n?'''\\",            """\"''''Super\\n?'''\\\\""" + '"'          ],

                #
                #   C_K/C_N: backslash: kc: not possible (""" not allowed)
                #   C_K/C_N: backslash: ks
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    "''''supercalifragilisticexpialidocious?'''\\",
                    """\"''''supercalifragilisticexpialidocious?'''\\\\""" + '"'
                ],

                #
                #   C_K: pc/ps: not possible (always backslash)
                #
            #</C_K>

            #<C_N>
                #
                #   C_N: ra - not possible (" not allowed)
                #   C_N: rq
                #
                #   NOTE:
                #       vim 7.4 gets confused with """x\"""" - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    "lots of ''''' - lots!",
                    """r"lots of ''''' - lots!""" + '"',
                    '''"lots of ''\''\' - lots!"''',
                ],

                #
                #   C_N:  lemon: kc: not possible (""" not allowed)
                #   C_N:  lemon: ks
                #       Have to represent what we "expect" using \' internally
                #
                [   "'''@C_\n",                     '''"''\'@C_\\n"'''                          ],

                #
                #   C_K/C_N: backslash: kc
                #   C_K/C_N: backslash: ks: not posssible (''' not allwoed)
                #
                [   '\\',                           r"'\\'"                                     ],

                #
                #   C_N: backslash: kc/ks: not possible (always raw mode)
                #   C_N: pc/ps:            not possible (always raw mode)
                #
            #</C_N>

            #<CQ_A>
                #
                #   CQ_A: ra: not possible (""" not allowed)
                #   CQ_A: rq
                #
                [
                    r"""End '''with "'": "'""",
                    '''r"""End ''\'with "'": "'"""''',
                    '''"""End ''\'with "'": "'"""''',
                ],

                #
                #   CQ_A: lemon: kc: not possible (""" not allowed)
                #   CQ_A: lemon: ks
                #
                [   """\"lemo\n'''s"'""",           '''"""\\"lemo\\n''\'s"'"""'''               ],

                #
                #   CQ_A: backslash: kc/ks: not possible (always raw mode)
                #   CQ_A: pc/ps:            not possible (always raw mode)
                #
            #</CQ_A>

            #<CQ_B>
                #
                #   CQ_B: ra: not possible (""" not allowed)
                #   CQ_B: rq
                #
                [
                    """More "quotes" ''' & ''""",
                    '''r"""More "quotes" ''\' & ''"""''',
                    '''"""More "quotes" ''\' & ''"""''',
                ],

                #
                #   CQ_B: lemon: kc: not possible (""" not allowed)
                #   CQ_B: lemon: ks
                #
                [   """\"lemo\n"ade'''s''""",   '''"""\\"lemo\\n"ade''\'s''"""'''               ],

                #
                #   CQ_B: backslash: kc/ks: not possible (always raw mode)
                #   CQ_B: pc/ps:            not possible (always raw mode)
                #
            #</CQ_A>

            #<CQ_C>
                #
                #   CQ_C: ra: not possible (""" not allowed)
                #   CQ_C: rq
                #
                [
                    """End with 3x "'": "'''""",
                    '''r"""End with 3x "'": "''\'"""''',
                    '''"""End with 3x "'": "''\'"""''',
                ],

                #
                #   CQ_C: lemon: kc: not possible (""" not allowed)
                #   CQ_C: lemon: ks
                #
                [   """'''"\tables"'''""",          '''"""''\'"\\tables"''\'"""'''              ],

                #
                #   CQ_C: backslash: kc/ks: not possible (always raw mode)
                #   CQ_C: pc/ps:            not possible (always raw mode)
                #
            #</CQ_C>

            #<CQ_K>
                #
                #   CQ_K/CQ_N: ra/rq:     not possible (ends in \)
                #   CQ_K/CQ_N: lemon: kc: not possible (""" not allowed)
                #   CQ_K/CQ_N: lemon: ks
                #
                [   """le'''"mo"\n\\""",            '''"""le''\'"mo"\\n\\\\"""'''               ],

                #
                #   CQ_K/C_N: backslash: kc: not possible (""" not allowed)
                #   CQ_K/C_N: backslash: ks
                #
                [   """deja vu: ", ''', & \\""",    '''"""deja vu: ", ''\', & \\\\"""'''        ],

                #
                #   CQ_K: pc/ps: not possible (always backslash)
                #
            #</CQ_K>

            #<CQ_N>
                #
                #   CQ_N: ra
                #       Have to represent what we "expect" using \' or \" internally
                #
                [
                    """l""s '''' t""n "!""",
                    '''r"""l""s ''\'' t""n "!"""''',
                    '''"""l""s ''\'' t""n "!"""''',
                ],

                #
                #   CQ_N: rq
                #
                [
                    """more '''' than "!""",
                    '''r"""more ''\'' than "!"""''',
                    '''"""more ''\'' than "!"""''',
                ],

                #
                #   CQ_C: lemon: kc: not possible (""" not allowed)
                #   CQ_N: lemon: ks
                #
                [   """'''"\rake"''' leaves""",     '''"""''\'"\\rake"''\' leaves"""'''         ],

                #
                #   CQ_K/C_N: backslash: kc: not possible (""" not allowed)
                #   CQ_K/C_N: backslash: ks
                #
                [
                    """been "there", '''done that'''\\""",
                    '''"""been "there", ''\'done that''\'\\\\"""'''
                ],

                #
                #   CQ_N: pc/ps:            not possible (always raw mode)
                #
            #</CQ_N>

            #<CQ_Q>
                #
                #   CQ_Q: ra/qs: not possible (ends in " so can't use either ''' or """ around it)
                #

                #
                #   CQ_Q: lemon: kc: not possible (""" not allowed)
                #   CQ_Q: lemon: ks
                #
                [   '''\''\'\t"''',                 """'''\\''\\'\\t"'''"""                     ],

                #
                #   CQ_Q: pc: not possible (""" not allowed)
                #   CQ_Q: ps
                #
                [   '''\'333: "''\'."''',           r"""'''\'333: "''\'."'''"""                 ],
            #</CQ_Q>

            #<CQ_R>
                #
                #   CQ_R: ra/qs: not possible (ends in " so can't use either ''' or """ around it)
                #

                #
                #   CQ_R: lemon: kc: not possible (""" not allowed)
                #   CQ_R: lemon: ks
                #
                [   '''almos\t done: ''\'""''',  """'''almos\\t done: ''\\'""'''"""             ],

                #
                #   CQ_R: pc: not possible (""" not allowed)
                #   CQ_R: ps
                #
                [   '''three: "''\''\''.""''',      r"""'''three: "''\''\''.""'''"""            ],
            #</CQ_R>

            #<N_K>
                #
                #   N_K/N_N: ra/rq:     not possible (ends in \)
                #   N_K/N_N: lemon: kc
                #   N_K/N_N: lemon: ks: not possible (''' not allowed)
                #
                [   'more lemo\ns\\',       "'more lemo\\ns\\\\'"                               ],

                #
                #   N_K/N_N: backslash: kc
                #   N_K/N_N: backslash: ks: not possible (''' not allowed)
                #
                [   'not a real lemon\\',  "'not a real lemon\\\\'"                             ],

                #
                #   N_K: pc/ps: not possible (always backslash)
                #
            #</N_K>

            #<N_N>
                #
                #   N_N: simple cases
                #
                [
                    '',
                    "r''",
                    "''",
                ],

                [ 
                    'test#2',
                    "r'test#2'",
                    "'test#2'",
                ],

                #
                #   N_N: ra
                #
                [   r'double backslash: \\',        r"r'double backslash: \\'"                  ],

                #
                #   N_N: rq
                #
                [   r"\'",                          r'''r"\'"'''                                ],

                #
                #   N_N: lemon: kc
                #   N_N: lemon: ks: not possible (''' not allowed)
                #
                [   'A \normal lemo\n',             "'A \\normal lemo\\n'"                      ],

                #
                #   N_K/N_N: backslash: kc
                #   N_K/N_N: backslash: ks: not possible (''' not allowed)
                #
                [   'backslash: \\',                "'backslash: \\\\'"                         ],

                #
                #   N_N: pc/ps: not possible (always raw mode)
                #
            #</N_N>

            #<Q_K>
                #
                #   Q_K/Q_N: ra/rq:     not possible (ends in \)
                #   Q_K/Q_N: lemon: kc
                #   Q_K/Q_N: lemon: ks: not possible (''' not allowed)
                #
                [   'le"mo"\nade\\',                """'le"mo"\\nade\\\\'"""                    ],

                #
                #   Q_K/Q_N: backslash: kc
                #   Q_K/Q_N: backslash: ks: not possible (''' not allowed)
                #
                [   'just " & \\',                  """'just " & \\\\'"""                       ],

                #
                #   Q_K: pc/ps: not possible (always backslash)
                #
            #</Q_K>

            #<Q_N>
                #
                #   Q_N: ra
                #
                [
                    '" is a quotation mark',
                    """r'" is a quotation mark'""",
                    """'" is a quotation mark'""",
                ],

                #
                #   Q_N: rq
                #
                [   r'\'"\'',                       r"""r'\'"\''"""                             ],

                #
                #   Q_N: lemon: kc
                #   Q_N: lemon: ks: not possible (''' not allowed)
                #
                [   'A "\normal" lemo\n',           """'A "\\normal" lemo\\n'"""                ],

                #
                #   Q_N: backslash: kc
                #   Q_N: backslash: ks: not possible (''' not allowed)
                #
                [   '"backslash": \\',             r"""'"backslash": \\'"""                     ],

                #
                #   Q_N: pc/ps: not possible (always raw mode)
                #
            #</Q_N>

            #<Q_Q>
                #
                #   Q_Q: ra
                #
                [
                    '"',
                    """r'"'""",
                    """'"'""",
                ],

                #
                #   Q_Q: rq
                #
                [   r'She \'said\' \'hello"',       r"""r'She \'said\' \'hello"'"""             ],

                #
                #   Q_Q: lemon: kc
                #   Q_Q: lemon: ks: not possible (''' not allowed)
                #
                [   'lemo\n "orchard"',             """'lemo\\n "orchard"'"""                   ],

                #
                #   Q_Q: backslash: kc/ks: not possible (always raw mode)
                #   Q_Q: pc/ps:            not possible (always raw mode)
                #
            #</Q_Q>

            #<Q_R>
                #
                #   Q_R: ra
                #
                [
                    'double quoted: ""',
                    """r'double quoted: ""'""",
                    """'double quoted: ""'""",
                ],

                #
                #   Q_R: rq
                #
                [   r'More \'\'\' than ""',         r"""r'More \'\'\' than ""'"""               ],

                #
                #   Q_R: lemon: kc
                #   Q_R: lemon: ks: not possible (''' not allowed)
                #
                [   'lemo\n"s and quotes""',        """'lemo\\n"s and quotes""'"""              ],

                #
                #   Q_R: backslash: kc/ks: not possible (always raw mode)
                #   Q_R: pc/ps:            not possible (always raw mode)
                #
            #</Q_R>

            #<S_K>
                #
                #   S_K/S_N: ra/rq:     not possible (ends in \)
                #   S_K/S_N: lemon: kc
                #   S_K/S_N: lemon: ks: not possible (''' not allowed)
                #
                [   '"""S\nakes""" \\',             """'""\"S\\nakes""\" \\\\'"""               ],

                #
                #   S_K/S_N: backslash: kc
                #   S_K/S_N: backslash: ks: not possible (''' not allowed)
                #
                [   '"""Snakes""" & backslash: \\', """'""\"Snakes""\" & backslash: \\\\'"""    ],

                #
                #   S_K: pc/ps: not possible (always backslash)
                #
            #</S_K>

            #<S_N>
                #
                #   S_N: ra
                #
                #   NOTE:
                #       vim 7.4 gets confused with '''x\'''' - so use string concatanation so vim can properly parse
                #       it.
                #
                [
                    'lots of """"" - lots!',
                    """r'lots of ""\""\" - lots!'""",
                    """'lots of ""\""\" - lots!'""",
                ],

                #
                #   S_N: rq
                #
                [   r'Prefer \'\'\'\' or """?',     """r'Prefer \\'\\'\\'\\' or ""\"?'"""       ],

                #
                #   S_K/S_N: kc
                #   S_K/S_N: backslash: ks: not possible (''' not allowed)
                #
                [   'Yet again """ & \\',           """'Yet again ""\" & \\\\'"""               ],

                #
                #   S_K: pc/ps: not possible (always raw mode)
                #
            #</S_N>

            #<S_Q>
                #
                #   S_Q: ra
                #
                [
                    'Three """ is more than 1 "',
                    """r'Three ""\" is more than 1 "'""",
                    """'Three ""\" is more than 1 "'""",
                ],

                #
                #   S_Q: rq
                #
                [   r'"""\'\'hi\'\' & \'hello"',    """r'""\"\\'\\'hi\\'\\' & \\'hello"'"""     ],

                #
                #   S_Q: lemon: kc
                #   S_Q: lemon: ks: not possible (''' not allowed)
                #
                [   '"""Quotatio\n"',               """'""\"Quotatio\\n"'"""                    ],

                #
                #   S_Q: backslash: kc/ks: not possible (always raw mode)
                #   S_Q: pc/ps:            not possible (always raw mode)
                #
            #</S_Q>

            #<S_R>
                #
                #   S_R: ra
                #
                [
                    'Three """ > 2 ""',
                    """r'Three ""\" > 2 ""'""",
                    """'Three ""\" > 2 ""'""",
                ],

                #
                #   S_R: rq
                #
                [   r'"""\'\'hello\'\' & \'bye""',  """r'""\"\\'\\'hello\\'\\' & \\'bye""'"""   ],

                #
                #   S_R: lemon: kc
                #   S_R: lemon: ks: not possible (''' not allowed)
                #
                [   '"""5 Quotatio\n marks""',      """'""\"5 Quotatio\\n marks""'"""           ],

                #
                #   S_R: backslash: kc/ks: not possible (always raw mode)
                #   S_R: pc/ps:            not possible (always raw mode)
                #
            #</S_R>

            #<S_S>
                #
                #   S_S: ra
                #
                [
                    '"""',
                    """r'""\"'""",
                    """'""\"'""",
                ],

                #
                #   S_S: rq
                #
                [   r'"""\'\'\'\'\'\'\'"""',        """r'""\"\\'\\'\\'\\'\\'\\'\\'""\"'"""      ],

                #
                #   S_S: lemon: kc
                #   S_S: lemon: ks: not possible (''' not allowed)
                #
                [   '"""And \now six!"""',          """'""\"And \\now six!""\"'"""              ],

                #
                #   S_S: backslash: kc/ks: not possible (always raw mode)
                #   S_S: pc/ps:            not possible (always raw mode)
                #
            #</S_S>

            #<Others>
                [
                    '''"lots of ''\''\' - lots!"''',
                    """'''"lots of ''\\''\\' - lots!"'''""",
                ],
            #</Others>
        ]:
            if row is 0:
                break

            if row is 2:
                saw_2 = true
                continue

            if length(row) is 2:
                [s, raw_expected] = row
                expected          = raw_expected
            else:
                [s, raw_expected, expected] = row

            actual = portray_raw_string(s)

            if actual != raw_expected:
                line('portray_raw_string(%r)', s)
                line('  actual:   %s', actual)
                line('  expected: %s', raw_expected)

                raise_value_error('portray_raw_string(%r): %r (expected: %r)', s, actual, raw_expected)

            if saw_2:
                continue

            if expected is not none:
                actual = portray_string(s)

                if actual != expected:
                    line('portray_string(%r)', s)
                    line('  actual:   %s', actual)
                    line('  expected: %s', expected)

                    raise_value_error('portray_string(%r): %r (expected: %r)', s, actual, expected)


    def create_state_machine_tuple():
        state_machine__map    = {}
        state_machine__lookup = state_machine__map.get
        state_machine__store  = state_machine__map.__setitem__


        def state_machine__insert(state):
            previous = state_machine__lookup(state.name)

            if previous is state:
                return

            assert previous is none

            state_machine__store(state.name, state)

            state_machine__insert(state.A)
            state_machine__insert(state.K)
            state_machine__insert(state.N)
            state_machine__insert(state.Q)


        state_machine__insert(N_N)

        return values_tuple_sorted_by_key(state_machine__map)


    def test_state_machine(state):
        def verify_name(mode, value, expected_prefix, expected_suffix):
            if value.name != expected_prefix + '_' + expected_suffix:
                raise_runtime_error('PortrayStringState.setup: %s + %s => %s (expected %s)',
                                    name, mode, value.name, expected_prefix + '_' + expected_suffix)

        name = state.name
        A    = state.A
        K    = state.K
        N    = state.N
        Q    = state.Q
        kc   = state.kc
        ks   = state.ks
        pc   = state.pc
        ps   = state.ps
        ra   = state.ra
        rq   = state.rq

        underscore = name.index('_')
        prefix     = name[:underscore]
        suffix     = name[underscore + 1:]

        PA = PC = PCS = PL = PN = PQ = PS = 0
        SA = SB = SC = SK = SN = SQ = SR = SS = 0

        if prefix == 'A':           PA = 7
        elif prefix == 'AQ':        PA = PQ = 7
        elif prefix == 'AS':        PA = PS = 7
        elif prefix == 'C':         PC = 7
        elif prefix == 'CQ':        PC = PQ = 7
        elif prefix == 'CS':        PC = PCS = PS = 7
        elif prefix == 'L':         PL = 7
        elif prefix == 'N':         PN = 7
        elif prefix == 'Q':         PQ = 7
        elif prefix == 'S':         PS = 7
        else:                       raise_runtime_error('incomplete: prefix: %s', prefix)

        if suffix == 'A':           SA = 7
        elif suffix == 'B':         SB = 7
        elif suffix == 'C':         SC = 7
        elif suffix == 'K':         SK = 7
        elif suffix == 'N':         SN = 7
        elif suffix == 'Q':         SQ = 7
        elif suffix == 'R':         SR = 7
        elif suffix == 'S':         SS = 7
        else:
            raise_runtime_error('incomplete: suffix: %s', suffix)

        #<A>
        C_prefix = '?'

        if PA:
            A_prefix = prefix
            C_prefix = 'C' + prefix[1:]
        elif (PC) or (PL):
            A_prefix = C_prefix = prefix
        elif PN:
            A_prefix = 'A'
        else:
            A_prefix = 'A' + prefix

        if (SA) or (SC):    verify_name('A', A, A_prefix, 'B')
        elif SB:            verify_name('A', A, C_prefix, 'C')
        elif SK:            verify_name('A', A, prefix,   'N')
        else:               verify_name('A', A, A_prefix, 'A')
        #</A>

        #<K>
        if SK:      verify_name('K', K, prefix, 'N')
        else:       verify_name('K', K, prefix, ('N'   if (PCS) or (PL) else   'K'))
        #</K>

        #<N>
        verify_name('N', N, prefix, 'N')
        #</N>

        #<Q>
        S_prefix = '?'

        if PQ:
            Q_prefix = prefix
            S_prefix = prefix[:-1] + 'S'
        elif (PL) or (PS):
            Q_prefix = S_prefix = prefix
        elif PN:
            Q_prefix = 'Q'
        else:
            Q_prefix = prefix + 'Q'

        #line('%s: SR<%d>, Qp<%s>, Sp<%s>', name, SR, Q_prefix, S_prefix)

        if (SQ) or (SS):    verify_name('Q', Q, Q_prefix, 'R')
        elif SR:            verify_name('Q', Q, S_prefix, 'S')
        elif SK:            verify_name('Q', Q, prefix,   'N')
        else:               verify_name('Q', Q, Q_prefix, 'Q')
        #</Q>

        #<ra & rq>
        if (PL) or (PCS) or (SK):
            expected_RQ = expected_RN = 0
        elif (PC):
            assert not SS

            if (SQ) or (SR):
                expected_RQ = expected_RN = 0
            else:
                if PQ:
                    expected_RQ = expected_RN = 'portray_raw_string_with_triple_quotation_mark'
                else:
                    expected_RQ = expected_RN = 'portray_raw_string_with_quotation_mark'
        elif (PS):
            assert not SC

            if (SA) or (SB):
                expected_RQ = expected_RN = 0
            else:
                if PA:
                    expected_RQ = expected_RN = 'portray_raw_string_with_triple_apostrophe'
                else:
                    expected_RQ = expected_RN = 'portray_raw_string_with_apostrophe'
        elif PA:
            assert not SC

            if PQ:
                if (SA) or (SB):
                    expected_RQ = expected_RN = 'portray_raw_string_with_triple_quotation_mark'
                elif (SQ) or (SR):
                    expected_RQ = expected_RN = 'portray_raw_string_with_triple_apostrophe'
                else:
                    expected_RN = 'portray_raw_string_with_triple_apostrophe'
                    expected_RQ = 'portray_raw_string_with_triple_quotation_mark'
            else:
                expected_RN = expected_RQ = 'portray_raw_string_with_quotation_mark'
        elif PQ:
            assert not SS

            expected_RQ = expected_RN = 'portray_raw_string_with_apostrophe'
        elif PN:
            assert (not SA) and (not SB) and (not SC) and (not SQ) and (not SR) and (not SS)

            expected_RN = 'portray_raw_string_with_apostrophe'
            expected_RQ = 'portray_raw_string_with_quotation_mark'
        else:
            expected_RQ = expected_RN = '?'

        if expected_RN is 0:
            if ra is not 0:
                raise_runtime_error('PortrayStringState.setup: %s.ra => %s (expected_RN 0)', name, ra, expected_RN)
        elif ra.__name__ != expected_RN:
            raise_runtime_error('PortrayStringState.setup: %s.ra => %s (expected_RN %s)',
                                name, ra.__name__, expected_RN)

        if expected_RQ is 0:
            if rq is not 0:
                raise_runtime_error('PortrayStringState.setup: %s.rq => %s (expected_RQ 0)', name, rq, expected_RQ)
        elif rq.__name__ != expected_RQ:
            raise_runtime_error('PortrayStringState.setup: %s.rq => %s (expected_RQ %s)',
                                name, rq.__name__, expected_RQ)
        #</ra & rq>

        #<favorite_3>
        if SC:
            expected_F3 = -1
        elif SS:
            expected_F3 = 1
        else:
            expected_F3 = 0

        if state.favorite_3 != expected_F3:
            raise_runtime_error('PortrayStringState.setup: %s.favorite_3<%d>  (expected %d)',
                                name, state.favorite_3, expected_F3)
        #</favorite_3>


    def test_portray_raw_string__state_machine():
        state_machine_tuple = create_state_machine_tuple()

        for state in state_machine_tuple:
            test_state_machine(state)


    @share
    def test_portray_raw_string():
        if __debug__:
            test_portray_raw_string__state_machine()

        test_portray_raw_string__raw_string()

        line('PASSED: portray_raw_string')
