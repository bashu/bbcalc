# ******************************************************************************
# GConf Schemas
# ******************************************************************************
# GConf Preference Schemas
schemadir = $(GCONF_SCHEMA_FILE_DIR)
schema_in_files = bbcalc.schemas.in
schema_DATA = $(schema_in_files:.schemas.in=.schemas)

# ******************************************************************************
# Application Icon
# ******************************************************************************
icondir = $(datadir)/pixmaps
icon_DATA = bbcalc.png

# ******************************************************************************
# Desktop File
# ******************************************************************************
@INTLTOOL_DESKTOP_RULE@

desktopdir = $(datadir)/applications
desktop_in_files = bbcalc.desktop.in
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)

# ******************************************************************************
# Build rules
# ******************************************************************************
@INTLTOOL_SCHEMAS_RULE@

install-data-hook:
if GCONF_SCHEMAS_INSTALL
	GCONF_CONFIG_SOURCE=$(GCONF_SCHEMA_CONFIG_SOURCE) \
	$(GCONFTOOL) --makefile-install-rule $(schema_DATA)
endif

DISTCLEANFILES = \
	$(desktop_DATA) \
	$(schema_DATA)

EXTRA_DIST = \
	$(icon_DATA)		\
	$(desktop_in_files) \
	$(desktop_DATA) \
	$(schema_in_files)
