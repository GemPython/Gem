AGATE_FILES = ../Main/Agate.py ../Agate/RUNME.py

GEM_FILES = \
	../Gem/__init__.py \
	../Gem/Boot.py \
	../Gem/Core.py ../Gem/CatchException.py \
	../Gem/Exception.py \
	../Gem/File.py ../Gem/FileOutput.py ../Gem/FileStatus.py \
	../Gem/Import.py ../Gem/IO.py \
	../Gem/Path.py \
	../Gem/RegularExpression.py

WORK_FILES = Makefile

FILES = $(AGATE_FILES) $(GEM_FILES) $(WORK_FILES)

all: clean files links

clean:
	rm -f *.old *.new
	rm -f a.py
	rm -f b.py
	rm -f c.py ce.py
	rm -f e.py
	rm -f files fi.py fo.py fs.py
	rm -f in.py im.py io.py
	rm -f m
	rm -f p.py
	rm -f r.py re.py

files:
	echo $(FILES) >files.new
	mv files.new files

links:
	ln -s ../Main/Agate.py              a.py
	ln -s ../Gem/Boot.py                b.py
	ln -s ../Gem/Core.py                c.py
	ln -s ../Gem/CatchException.py      ce.py
	ln -s ../Gem/Exception.py           e.py
	ln -s ../Gem/File.py                fi.py
	ln -s ../Gem/FileOutput.py          fo.py
	ln -s ../Gem/FileStatus.py          fs.py
	ln -s ../Gem/__init__.py            in.py
	ln -s ../Gem/Import.py              im.py
	ln -s ../Gem/IO.py                  io.py
	ln -s Makefile                      m
	ln -s ../Gem/Path.py                p.py
	ln -s ../Agate/RUNME.py             r.py
	ln -s ../Gem/RegularExpression.py   re.py
