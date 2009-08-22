#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class JokosherPackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'jokosher'
		self._version = '0.11.1'
		self._section = 'misc'
		self._priority = 'optional'
		self._authors = ['Jono Bacon <jono@jonobacon.org>', 
							'Jason Field <jfield@sonaptic.com>', 
							'Jens Geiregat <jens.geiregat@gmail.com>', 
							'Stuart Langridge <sil@kryogenix.org>', 
							'Laszlo Pandy <laszlok2@gmail.com>', 
							'Chris Procter <chris-procter@talk21.com>', 
							'Michael Sheldon <mike@mikeasoft.com>', 
							'Fabrice Silva <silva@crans.org>', 
							'Ben Thorp <mrben@jedimoose.org>', 
							'David Corrales <corrales.david@gmail.com>', 
							'John Kelly <jkelly.dev@googlemail.com>']
		self._copyright = ['Jono Bacon <jono@jonobacon.org>', 
							'Jason Field <jfield@sonaptic.com>', 
							'Stuart Langridge <sil@kryogenix.org>', 
							'Laszlo Pandy <laszlok2@gmail.com>', 
							'Michael Sheldon <mike@mikeasoft.com>', 
							'Ben Thorp <mrben@jedimoose.org>']
		self._homepage = 'http://jokosher.org'
		self._license = 'GPL2+'
		self._source = 'http://launchpad.net/jokosher/0.11/0.11.1/+download/jokosher-0.11.1.tar.gz'
		self._build_method = 'python application'

		self._build_requirements = ['python-support']

		self._install_requirements = ['python-cairo', 
										'python-dbus', 
										'python-glade2', 
										'python-gtk2', 
										'python-gst0.10', 
										'gstreamer0.10-gnonlin (>= 0.10.8)', 
										'gstreamer0.10-plugins-good (>= 0.10.9)', 
										'gstreamer0.10-plugins-base (>= 0.10.12)', 
										'python-setuptools']

		self._short_description = "simple and easy to use audio multi-tracker"

		self._long_description = "Jokosher is a simple and poweful multi-track studio. Jokosher provides a\n" + \
									"complete application for recording, editing, mixing and exporting audio, and\n" + \
									"has been specifically designed with usability in mind. The developers behind\n" + \
									"Jokosher have re-thought audio production at every level, and created\n" + \
									"something devilishly simple to use."

		self._changelog = [{"version" : "0.11.1", "time" : "Fri, 21 Aug 2009 19:49:12 -0700", "text" : "Initial release" } ]



