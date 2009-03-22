#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class TerminatorPackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'terminator'
		self._version = '0.8.1'
		self._section = 'misc'
		self._priority = 'optional'
		self._authors = ['Chris Jones <cmsj@tenshu.net>']
		self._copyright = ['2006-2008 Chris Jones']
		self._packager_name = 'Matthew Brennan Jones'
		self._packager_email = 'mattjones@workhorsy.org'
		self._bug_mail = 'mattjones@workhorsy.org'
		self._homepage = 'http://www.tenshu.net/terminator/'
		self._license = 'GPL2+'
		self._source = 'http://launchpad.net/terminator/trunk/0.8.1/+download/terminator_0.8.1.tar.gz'
		self._build_method = 'pure python application'

		self._build_requirements = []

		self._install_requirements = ['python-gobject', 'python-gtk2', 'python-gconf', 'python-vte']

		self._short_description = "multiple GNOME terminals in one window"

		self._long_description = "Terminator is a little project to produce an efficient way of\n" + \
									"filling a large area of screen space with terminals.\n" + \
									"\n" + \
									"The user can have multiple terminals in one window and use\n" + \
									"key bindings to switch between them. See the manpage for\n" + \
									"details."




