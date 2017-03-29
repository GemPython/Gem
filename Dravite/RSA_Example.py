#
#   -*- coding: utf-8
#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
#   RSA Key Encryption as explained at http://southernpacificreview.com/2014/01/06/rsa-key-generation-example/
#
#   (See also https://en.wikibooks.org/wiki/Cryptography/A_Basic_Public_Key_Example)
#
@gem('Dravite.RSA_Example')
def gem():
    require_gem('Gem.Exception')
    require_gem('Dravite.Euclid')


    #
    #<copyright>
    #
    #   Code was created (but not copied) by reading:
    #
    #       http://southernpacificreview.com/2014/01/06/rsa-key-generation-example/
    #
    #   As of 2016-03-02 this reads (at the bottom of the page):
    #
    #       "© 2017 Southern Pacific Review. All Rights Reserved"
    #
    #   A google search for "site:southernpacificreview.com license" did not return any useful results.
    #
    #   However, again, as the code was not copied, but created by reading -- it is taken to be
    #   allowed under the "fair use" rule of copyrights.
    #
    #   Still, as an abundance of caution, please do not copy any code below without this Copyright
    #   notice.
    #
    #   Thanks :)
    #
    def RSA_find(p, q):
        n      = p * q
        secret = (p - 1) * (q - 1)
        same   = none

        for e in iterate_range(secret - 1, 1, -1):
            #line('greatest_common_demominator(%d, %d)[0]: %d',
            #     e, secret, greatest_common_demominator(e, secret)[0])

            if greatest_common_demominator(e, secret)[0] == 1:
                d = modular_inverse(e, secret)

                if d is not none:
                    if d != e:
                        break

                    same = d
        else:
            if same is none:
                raise_runtime_error("can't find any reasonable greatest demonistator for %d", secret)

            d = e = same

        #
        #   Now prove that for any m, (m ** d ** e) %n == m
        #
        #line('d, e, n: %d, %d, %d', d, e, n)

        for m in iterate_range(0, n):
            z = (m ** e) % n

            assert m == (z ** d) % n

        return [d, e, n, secret]
    #<copyright>


    @share
    def RSA_Example():
        p = 3
        q = 11

        [d, e, n, secret] = RSA_find(p, q)

        line('p: %d, q: %d, secret: %d', p, q, secret)
        line('public key:  %d, %d', e, n)
        line('private key: %d, %d', d, n)
        line('math: given the reality that for any m: m ** %d %% %d == 1', secret, n)
        line('math: then since %d * %d == %d; then %d %% %d == %d', d, e, d * e, d * e, secret, d * e % secret)
        line('math: hence for any m: m ** (%d * %d) %% %d = m ** (%d * %d + (%d %% %d)) == m ** 1 == m',
             d, e, n, secret, d * e / secret, d * e, secret)
