#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class TomboyPackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'tomboy'
		self._version = '0.15.0'
		self._section = 'gnome'
		self._priority = 'optional'
		self._authors = ['Alex Graveley <alex@beatniksoftware.com>', 
							'Boyd Timothy <btimothy@gmail.com>', 
							'Chris Scobell <chris@thescobells.com>', 
							'David Trowbridge <trowbrds@gmail.com>', 
							'Ryan Lortie <desrt@desrt.ca>', 
							'Sandy Armstrong <sanfordarmstrong@gmail.com>', 
							'Sebastian Rittau <srittau@jroger.in-berlin.de>', 
							'Kevin Kubasik <kevin@kubasik.net>', 
							'Stefan Schweizer <steve.schweizer@gmail.com>']
		self._copyright = ['2004-2007 Alex Graveley']
		self._packager_name = 'Matthew Brennan Jones'
		self._packager_email = 'mattjones@workhorsy.org'
		self._bug_mail = 'mattjones@workhorsy.org'
		self._homepage = 'http://projects.gnome.org/tomboy/'
		self._license = 'LGPL2.1'
		self._source = 'http://download.gnome.org/sources/tomboy/0.15/tomboy-0.15.0.tar.gz'
		self._build_method = 'mono application with c libraries'

		self._build_requirements = ['python-devel', 'gettext', 'desktop-file-utils']

		self._install_requirements = ['python-gobject', 'python-gtk2', 'python-gconf', 'python-vte']

		self._short_description = "multiple GNOME terminals in one window"

		self._long_description = "Terminator is a little project to produce an efficient way of\n" + \
									"filling a large area of screen space with terminals.\n" + \
									"\n" + \
									"The user can have multiple terminals in one window and use\n" + \
									"key bindings to switch between them. See the manpage for\n" + \
									"details."

		self._changelog = [{"version" : "0.15.0", "time" : "Fri, 07 Aug 2009 18:32:26 -0700 ", "text" : "Initial release" } ]





