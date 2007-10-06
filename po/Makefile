INSTALL ?= install
PYFILES = ../bbcalc $(shell find ../lib -name "*.py" -print) 
POFILES = $(wildcard *.po)

help:
	@echo "USAGE:"
	@echo "make update - updates messages.pot and .po files"
	@echo "make dist   - creates .mo files in ../i18n dir"
	@echo "make pl.po  - updates pl.po file OR creates new one"
	@echo "              (replace 'pl' with your language code)"

messages.pot:
	xgettext -k_ -kN_ --language=Python -o messages.pot $(PYFILES) --from-code=utf-8

%.po: messages.pot
	@if test -f $@; then \
		echo -n "Updating '$*' language ";\
		msgmerge -U $@ messages.pot;\
	else \
		msginit -l $*.UTF8 -o $@; \
	fi

%.mo:
	for pofile in $(patsubst ../i18n/%/LC_MESSAGES/bbcalc.mo,%.po,$@); do \
		${INSTALL} -m 755 -d $(subst bbcalc.mo,,$@);\
		msgconv -t UTF-8 $${pofile} -o $${pofile}_utf8;\
		msgfmt $${pofile}_utf8 -o $@;\
		rm $${pofile}_utf8;\
	done

update: clean $(POFILES)

dist: clean $(POFILES:%.po=../i18n/%/LC_MESSAGES/bbcalc.mo)

clean:
	$(RM) $(POFILES:%.po=../i18n/%/LC_MESSAGES/bbcalc.mo)
	$(RM) messages.pot

.PHONY: update dist
