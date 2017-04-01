#
#   Copyright (c) 2017 Amit Green.  All rights reserved.
#
AGATE_FILES = ../Agate/RUNME.py

BERYL_FILES = \
    ../Beryl/__init__.py \
    ../Beryl/Ask.py \
    ../Beryl/BerylAnswer.py \
    ../Beryl/Main.py

GEM_FILES = \
	../Gem/__init__.py \
    ../Gem/Absent.py ../Gem/Ascii.py \
	../Gem/Boot.py \
	../Gem/Cache.py ../Gem/Codec.py ../Gem/Core.py ../Gem/CatchException.py \
	../Gem/DelayedFileOutput.py \
	../Gem/ErrorNumber.py ../Gem/Exception.py ../Gem/ExecuteFile.py \
	../Gem/FileOutput.py ../Gem/FileStatus.py \
	../Gem/Import.py ../Gem/IO.py \
    ../Gem/Map.py \
    ../Gem/Path.py ../Gem/Path2.py ../Gem/PortrayString.py \
    ../Gem/RegularExpression.py \
    ../Gem/SimpleStringIO.py ../Gem/StringOutput.py ../Gem/System.py

DRAVITE_FILES = \
    ../Dravite/Euclid.py \
    ../Dravite/__init__.py \
    ../Dravite/Main.py \
    ../Dravite/RSA_Example.py

IVORY_FILES = ../Ivory/Main.py

LICENSE_FILES = \
    ../OtherLicenses/README.txt

SAPPHIRE_FILES = \
    ../Sapphire/Core.py \
    ../Sapphire/Main.py \
    ../Sapphire/Parse.py \
    ../Sapphire/Pattern.py

TOPAZ_FILES = \
    ../Topaz/Core.py \
    ../Topaz/Main.py \
    ../Topaz/Path.py ../Topaz/Pattern.py ../Topaz/PortrayString.py \
    ../Topaz/StringOutput.py

TREMOLITE_FILES = \
    ../Tremolite/Build.py \
    ../Tremolite/Compile.py ../Tremolite/Core.py ../Tremolite/CreateMatch.py \
    ../Tremolite/Main.py \
    ../Tremolite/Name.py \
    ../Tremolite/Parse.py
    #
    #   Excludes:
    #       ../Tremolite/LICENSE
    #       ../Tremolite/Match.py
    #


WORK_FILES = Makefile

FILES = \
    $(AGATE_FILES) \
    $(BERYL_FILES) \
    $(DRAVITE_FILES) \
    $(GEM_FILES) \
    $(IVORY_FILES) \
    $(LICENSE_FILES) \
    $(SAPPHIRE_FILES) \
    $(TOPAZ_FILES) \
    $(TREMOLITE_FILES) \
    $(WORK_FILES)


all: clean files links


clean:
	rm -rf __pycache__
	rm -f *.old *.new *.pyc

	rm -f ab.py ac.py ag.py
	rm -f 2re.py 2sf.py 2sp.py 2sc.py
	rm -f 3re.py 3sf.py 3sp.py 3sc.py
	rm -f ba.py bi.py bk.py bm.py bo.py
	rm -f ca.py ce.py co.py
	rm -f de.py dfo.py di.py dm.py dr.py
	rm -f ef.py en.py ex.py
	rm -f files fo.py fs.py
	rm -f gd.py
	rm -f hc.py hm.py hpa.py hpt.py
	rm -f in.py im.py io.py iv.py
	rm -f jb.py
	rm -f lr.txt
	rm -f m m.py
	rm -f pa.py pa2.py ps.py ps3.py
	rm -f rm.py rx.py
	rm -f so.py ssio.py sy.py
	rm -f tcm.py tco.py tlp.txt tma.py tmc.py tn.py tp.py tu.py tx.py
	rm -f zc.py zm.py zpa.py zps.py zpt.py zso.py


files:
	echo $(FILES) >files.new
	mv files.new files


links:
	ln -s ../Gem/Absent.py                      ab.py
	ln -s ../Gem/Ascii.py                       ac.py
	ln -s ../Agate/RUNME.py                     ag.py
	ln -s /usr/lib/python2.7/re.py              2re.py
	ln -s /usr/lib/python2.7/sre_compile.py     2sc.py
	ln -s /usr/lib/python2.7/sre_constants.py   2sf.py
	ln -s /usr/lib/python2.7/sre_parse.py       2sp.py
	ln -s /usr/lib/python3.5/re.py              3re.py
	ln -s /usr/lib/python3.5/sre_compile.py     3sc.py
	ln -s /usr/lib/python3.5/sre_constants.py   3sf.py
	ln -s /usr/lib/python3.5/sre_parse.py       3sp.py
	ln -s ../Beryl/BerylAnswer.py               ba.py
	ln -s ../Beryl/__init__.py                  bi.py
	ln -s ../Beryl/Ask.py                       bk.py
	ln -s ../Beryl/Main.py                      bm.py
	ln -s ../Gem/Boot.py                        bo.py
	ln -s ../Gem/Cache.py                       ca.py
	ln -s ../Gem/CatchException.py              ce.py
	ln -s ../Gem/Core.py                        co.py
	ln -s ../Dravite/Euclid.py                  de.py
	ln -s ../Gem/DelayedFileOutput.py           dfo.py
	ln -s ../Dravite/__init__.py                di.py
	ln -s ../Dravite/Main.py                    dm.py
	ln -s ../Dravite/RSA_Example.py             dr.py
	ln -s ../Gem/ExecuteFile.py                 ef.py
	ln -s ../Gem/ErrorNumber.py                 en.py
	ln -s ../Gem/Exception.py                   ex.py
	ln -s ../Gem/FileOutput.py                  fo.py
	ln -s ../Gem/FileStatus.py                  fs.py
	ln -s ../Gem/Codec.py                       gd.py
	ln -s ../Sapphire/Core.py                   hc.py
	ln -s ../Sapphire/Main.py                   hm.py
	ln -s ../Sapphire/Parse.py                  hpa.py
	ln -s ../Sapphire/Pattern.py                hpt.py
	ln -s ../Gem/__init__.py                    in.py
	ln -s ../Gem/Import.py                      im.py
	ln -s ../Ivory/Main.py                      iv.py
	ln -s ../Gem/IO.py                          io.py
	ln -s ../Junk/Boot.py                       jb.py
	ln -s ../OtherLicenses/README.txt           lr.txt
	ln -s Makefile                              m
	ln -s ../Gem/Map.py                         m.py
	ln -s ../Gem/Path.py                        pa.py
	ln -s ../Gem/Path2.py                       pa2.py
	ln -s ../Gem/PortrayString.py               ps.py
	ln -s ../Junk/PortrayString_3.py            ps3.py
	ln -s ../Agate/RUNME.py                     rm.py
	ln -s ../Gem/RegularExpression.py           rx.py
	ln -s ../Gem/StringOutput.py                so.py
	ln -s ../Gem/SimpleStringIO.py              ssio.py
	ln -s ../Gem/System.py                      sy.py
	ln -s ../Tremolite/CreateMatch.py           tcm.py
	ln -s ../Tremolite/Core.py                  tco.py
	ln -s ../Tremolite/LicenseTemplate.txt      tlp.txt
	ln -s ../Tremolite/Main.py                  tma.py
	ln -s ../Tremolite/Match.py                 tmc.py
	ln -s ../Tremolite/Name.py                  tn.py
	ln -s ../Tremolite/Parse.py                 tp.py
	ln -s ../Tremolite/Build.py                 tu.py
	ln -s ../Tremolite/Compile.py               tx.py
	ln -s ../Topaz/Core.py                      zc.py
	ln -s ../Topaz/Main.py                      zm.py
	ln -s ../Topaz/Path.py                      zpa.py
	ln -s ../Topaz/PortrayString.py             zps.py
	ln -s ../Topaz/Pattern.py                   zpt.py
	ln -s ../Topaz/StringOutput.py              zso.py


wc:
    #
	#  Excludes $(AGATE_FILES)
    #
	wc -l \
		$(BERYL_FILES) \
		$(DRAVITE_FILES) \
        $(GEM_FILES) \
        $(IVORY_FILES) \
        $(LICENSE_FILES) \
        $(SAPPHIRE_FILES) \
        $(TOPAZ_FILES) \
        $(TREMOLITE_FILES) \
        $(WORK_FILES)
