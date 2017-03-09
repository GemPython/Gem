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
    ../Gem/Ascii.py \
	../Gem/Boot.py \
	../Gem/Core.py ../Gem/CatchException.py \
	../Gem/Exception.py ../Gem/ExecuteFile.py \
	../Gem/File.py ../Gem/FileOutput.py ../Gem/FileStatus.py \
	../Gem/Import.py ../Gem/IO.py \
    ../Gem/Map.py \
    ../Gem/Path.py ../Gem/PortrayString.py \
    ../Gem/RegularExpression.py \
    ../Gem/StringIO.py

DRAVITE_FILES = \
    ../Dravite/Euclid.py \
    ../Dravite/__init__.py \
    ../Dravite/Main.py \
    ../Dravite/RSA_Example.py

IVORY_FILES = ../Ivory/Main.py

LICENSE_FILES = \
    ../OtherLicenses/README.txt

TOPAZ_FILES = \
    ../Topaz/Core.py \
    ../Topaz/Main.py \
    ../Topaz/PortrayString.py

WORK_FILES = Makefile

FILES = \
    $(AGATE_FILES) \
    $(BERYL_FILES) \
    $(DRAVITE_FILES) \
    $(GEM_FILES) \
    $(IVORY_FILES) \
    $(LICENSE_FILES) \
    $(TOPAZ_FILES) \
    $(WORK_FILES)

all: clean files links

clean:
	rm -rf __pycache__
	rm -f *.old *.new *.pyc

	rm -f ac.py ag.py
	rm -f 2re.py 2sf.py 2sp.py 2sc.py
	rm -f 3re.py 3sf.py 3sp.py 3sc.py
	rm -f ba.py bi.py bk.py bm.py bo.py
	rm -f c.py ce.py
	rm -f de.py di.py dm.py dr.py
	rm -f ef.py ex.py
	rm -f files fi.py fo.py fs.py
	rm -f in.py im.py io.py iv.py
	rm -f jb.py
	rm -f lr.txt
	rm -f m m.py
	rm -f pa.py ps.py ps3.py
	rm -f rm.py rx.py
	rm -f sio.py
	rm -f tc.py tm.py tp.py tu.py tx.py
	rm -f zc.py zm.py zps.py


files:
	echo $(FILES) >files.new
	mv files.new files

links:
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
	ln -s ../Gem/Core.py                        c.py
	ln -s ../Gem/CatchException.py              ce.py
	ln -s ../Dravite/Euclid.py                  de.py
	ln -s ../Dravite/__init__.py                di.py
	ln -s ../Dravite/Main.py                    dm.py
	ln -s ../Dravite/RSA_Example.py             dr.py
	ln -s ../Gem/ExecuteFile.py                 ef.py
	ln -s ../Gem/Exception.py                   ex.py
	ln -s ../Gem/File.py                        fi.py
	ln -s ../Gem/FileOutput.py                  fo.py
	ln -s ../Gem/FileStatus.py                  fs.py
	ln -s ../Gem/__init__.py                    in.py
	ln -s ../Gem/Import.py                      im.py
	ln -s ../Ivory/Main.py                      iv.py
	ln -s ../Gem/IO.py                          io.py
	ln -s ../Junk/Boot.py                       jb.py
	ln -s ../OtherLicenses/README.txt           lr.txt
	ln -s Makefile                              m
	ln -s ../Gem/Map.py                         m.py
	ln -s ../Gem/Path.py                        pa.py
	ln -s ../Gem/PortrayString.py               ps.py
	ln -s ../Junk/PortrayString_3.py            ps3.py
	ln -s ../Agate/RUNME.py                     rm.py
	ln -s ../Gem/RegularExpression.py           rx.py
	ln -s ../Gem/StringIO.py                    sio.py
	ln -s ../Topaz/Core.py                      zc.py
	ln -s ../Topaz/Main.py                      zm.py
	ln -s ../Topaz/PortrayString.py             zps.py


wc:
	#  Excludes $(AGATE_FILES)
	wc -l \
		$(BERYL_FILES) \
		$(DRAVITE_FILES) \
        $(GEM_FILES) \
        $(IVORY_FILES) \
        $(LICENSE_FILES) \
        $(TOPAZ_FILES) \
        $(WORK_FILES)
