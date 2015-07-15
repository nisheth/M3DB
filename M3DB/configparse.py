#!/usr/bin/env python
# M3DB project - configparse.py
# m3dbhome env var?
from configparser import ConfigParser
import os
m3dbcfg = ConfigParser()
def LoadConfig(conffile, m3dbconfig={}):
	if os.path.isfile('m3db.conf'):
		m3dbcfg.read(conffile)
	else:
		print "Using default configuration no custom m3db.conf file found"
	for section in m3dbcfg.sections():
		section_name = section.lower()
		for option in m3dbcfg.options(section):
			value = m3dbcfg.get(section,option)
			m3dbconfig[section + "." + option] = value.strip()
	return m3dbconfig