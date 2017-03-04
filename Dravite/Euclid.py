#
#   -*- coding: utf-8
#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
@gem('Dravite.Euclid')
def gem():
    #
    #<copyright>
    #
    #   Code copied from:
    #
    #       https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    #
    #   As of 2017-03-02, when the code was copied, it said:
    #
    #       "This page was last modified on 19 April 2016, at 15:15."
    #
    #       "Text is available under the Creative Commons Attribution-ShareAlike License.; additional terms
    #       may apply. By using this site, you agree to the Terms of Use and Privacy Policy."
    #
    #   The link for 'Creative Commons Attribution-ShareAlike License.' is to
    #
    #       "https://creativecommons.org/licenses/by-sa/3.0/"
    #
    #   As of 2017-03-02 this summary reads:
    #
    #                                       (CC) Creative
    #                                            Commons
    #                       
    #                           Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
    #
    #               This is a human-readable summary of (and not a substitute for) the license.
    #
    #       You are free to:
    #
    #           Share — copy and redistribute the material in any medium or format
    #           Adapt — remix, transform, and build upon the material
    #
    #           for any purpose, even commercially.
    #
    #           The licensor cannot revoke these freedoms as long as you follow the license terms.
    #
    #       Under the following terms:
    #
    #           Attribution — You must give appropriate credit, provide a link to the license, and indicate if
    #           changes were made. You may do so in any reasonable manner, but not in any way that suggests
    #           the licensor endorses you or your use.
    #
    #           ShareAlike — If you remix, transform, or build upon the material, you must distribute your
    #           contributions under the same license as the original.
    #
    #           No additional restrictions — You may not apply legal terms or technological measures that
    #           legally restrict others from doing anything the license permits.
    #
    #   As of 2017-03-03, a copy of this summary has been saved as:
    #
    #       "../OtherLicenses/cc/2017-03-02-by-sa_3.0.html".
    #
    #   The actual license the summary links to is at:
    #
    #       https://creativecommons.org/licenses/by-sa/3.0/legalcode
    #
    #   As of 2017-03-02, a copy of this license has been saved as:
    #
    #       "../OtherLicenses/cc/2017-03-02-by-sa_3.0_legalcode.html" in the same
    #
    #-----------------------------------------------------------------------------------------------------
    #
    #   As stated above for "Creative Commons Attribution-ShareAlike 3.0 Unported" under the "Attribution"
    #   section:
    #
    #       "Attribution — You must give appropriate credit, provide a link to the license, and indicate
    #       if changes were made. You may do so in any reasonable manner, but not in any way that
    #       suggests the licensor endorses you or your use.
    #
    #   To comply with these terms:
    #
    #       1.  Appropirate credite has been given by this copyright notice;
    #
    #       2.  A link has been provided to the license;
    #
    #       3.  This notice, hereby, *INDICATES THAT CHANGES HAVE BEEN* made to the original code;
    #
    #       4.  We do NOT indicate the licensor has endorsed our copy of the code in any way.
    #
    #-----------------------------------------------------------------------------------------------------
    #
    #   P.S.:  An MIT license is much easier to comply with than a "Attribute-ShareAlike" license,
    #          which is why we use the MIT license for the Gem project for all our own original code.
    #
    #          Of course the MIT license, does *NOT* apply to the orignal of the code, which has its
    #          own license as indicated above.
    #
    #          To make things simple, all *changes* to the original code below are dual licensed under
    #          both (1) the MIT License that the rest of Gem is licensed; and (2) under the exact same
    #          "Creative Commons Attribution-ShareAlike 3.0 Unported" license as the original code.
    #
    #   NOTE:  Dual copyright only applies to the changes, not to the original code which is obviously
    #          only licensed under the original license.
    #
    @share
    def greatest_common_demominator(b, n):
        [x0, x1, y0, y1] = ((1, 0, 0, 1))

        while n != 0:
            [q, b, n] = ((b // n, n, b % n))
            [x0, x1]  = ((x1, x0 - q * x1))
            [y0, y1]  = ((y1, y0 - q * y1))

        return ((b, x0, y0))


    #
    #   x = modular_inverse(b) mod n, (x * b) % n == 1
    #
    @share
    def modular_inverse(b, n):
        [g, x, J] = greatest_common_demominator(b, n)

        if g == 1:
            return x % n
    #</copyright>
