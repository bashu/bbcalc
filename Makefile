# BBCalc makefile
#
# (c) 2007 Basil Shubin
#
# Based on a same file from Griffith application
#

PACKAGE=bbcalc
LANGUAGES=$(shell find i18n/ -maxdepth 1 -mindepth 1 -type d -not -name CVS -printf "%f ")
VERSION=$(shell grep "^pversion" lib/version.py | cut -d \"  -f 2)

.PHONY: help clean install

INSTALL ?= install
MAKE ?= make
RM ?= rm
MSGFMT ?= msgfmt
MSGMERGE ?= msgmerge
XGETTEXT ?= xgettext
FIND ?= find
DOC2MAN ?= docbook2x-man

PREFIX = /usr
BINDIR = $(PREFIX)/bin
DATADIR = $(PREFIX)/share/bbcalc
LIBDIR = $(DATADIR)/lib
GLADEDIR = $(DATADIR)/glade
APPLICATIONSDIR = $(PREFIX)/share/applications
ICONDIR = $(PREFIX)/share/pixmaps
LOCALEDIR = $(PREFIX)/share/locale

help:
	@echo Usage:
	@echo "make             - not used"
	@echo "make clean       - delete built modules and object files"
	@echo "make install     - install binaries into the official directories"
	@echo "make uninstall   - uninstall binaries from the official directories"
	@echo "make help        - prints this help"
	@echo "make dist        - makes a distribution tarball"
	@echo "make locales     - update i18n files"
	@echo
	

install: locales
	@echo
	@echo "installing BBCalc"
	@echo "^^^^^^^^^^^^^^^^^"
	$(INSTALL) -m 755 -d $(BINDIR) $(DATADIR) $(LIBDIR) $(ICONSDIR) \
		$(APPLICATIONSDIR)
	$(INSTALL) -m 755 bbcalc $(DATADIR)
	# install all modules (dirs and files)
	(cd lib; for dir in `$(FIND) . -type d | grep -v ".svn"`; do \
		$(INSTALL) -m 755 -d $(LIBDIR)/$$dir ; \
	done)
	(cd lib; for file in `$(FIND) . -name "*.py"`; do \
		$(INSTALL) -m 644 $$file $(LIBDIR)/$$file ; \
	done)
	# install glade files
	$(INSTALL) -m 755 -d $(GLADEDIR)
	(cd glade; for file in `$(FIND) . -name "*.glade"`; do \
		$(INSTALL) -m 644 $$file $(GLADEDIR)/$$file ; \
	done)
#	$(INSTALL) -m 644 src/images/bbcalc.png $(ICONDIR)
#	$(INSTALL) -m 644 src/images/bbcalc.xpm $(ICONDIR)
	$(INSTALL) -m 644 data/bbcalc.desktop $(APPLICATIONSDIR)
	
	# installing language files
	for lang in $(LANGUAGES); do \
		${INSTALL} -m 755 -d $(LOCALEDIR)/$$lang/LC_MESSAGES; \
		$(INSTALL) -m 644 i18n/$$lang/LC_MESSAGES/*.mo $(LOCALEDIR)/$$lang/LC_MESSAGES; \
	done
	
	if test -f $(PREFIX)/bin/bbcalc; then ${RM} $(PREFIX)/bin/bbcalc; fi	
	
	ln -s $(DATADIR)/bbcalc $(BINDIR)/bbcalc
	chmod +x $(BINDIR)/bbcalc
	
uninstall:
	@echo
	@echo "uninstalling BBCalc"
	@echo "^^^^^^^^^^^^^^^^^^^"
	${RM} -r $(LIBDIR)
	${RM} -r $(GLADEDIR)
	${RM} -r $(DATADIR)
#	${RM} -r $(ICONDIR)/bbcalc.png
#	${RM} -r $(ICONDIR)/bbcalc.xpm
	${RM} -r $(APPLICATIONSDIR)/bbcalc.desktop
	for lang in $(LANGUAGES); do \
		${RM} -r $(LOCALEDIR)/$$lang/LC_MESSAGES/bbcalc.mo; \
	done
	${RM} -r $(BINDIR)/bbcalc
	
clean:
	${FIND} lib \( -iname '*\.py[co]' -or -iname '*~' -or -iname '*\.bak' \) -exec ${RM} '{}' \;
	
dist: clean
	@tar --exclude=*svn* --exclude=*.tar* --exclude=*~* --exclude=debian -cf bbcalc.tar ./
	@mkdir $(PACKAGE)-$(VERSION)
	@tar -xf bbcalc.tar -C $(PACKAGE)-$(VERSION)
	@${RM} bbcalc.tar
	@tar -czf $(PACKAGE)-$(VERSION).tar.gz $(PACKAGE)-$(VERSION) && echo File ./$(PACKAGE)-$(VERSION).tar.gz generated successfully
	@${RM} -r $(PACKAGE)-$(VERSION)
	
locales:
	@echo
	@echo "updating i18n files"
	@echo "^^^^^^^^^^^^^^^^^^^"
	(cd po; make update; make dist)
