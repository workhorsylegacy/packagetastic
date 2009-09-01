#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'jokosher'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._authors = [u'Jono Bacon <jono@jonobacon.org>', 
							u'Jason Field <jfield@sonaptic.com>', 
							u'Jens Geiregat <jens.geiregat@gmail.com>', 
							u'Stuart Langridge <sil@kryogenix.org>', 
							u'Laszlo Pandy <laszlok2@gmail.com>', 
							u'Chris Procter <chris-procter@talk21.com>', 
							u'Michael Sheldon <mike@mikeasoft.com>', 
							u'Fabrice Silva <silva@crans.org>', 
							u'Ben Thorp <mrben@jedimoose.org>', 
							u'David Corrales <corrales.david@gmail.com>', 
							u'John Kelly <jkelly.dev@googlemail.com>']
		self._copyright = [u'Jono Bacon <jono@jonobacon.org>', 
							u'Jason Field <jfield@sonaptic.com>', 
							u'Stuart Langridge <sil@kryogenix.org>', 
							u'Laszlo Pandy <laszlok2@gmail.com>', 
							u'Michael Sheldon <mike@mikeasoft.com>', 
							u'Ben Thorp <mrben@jedimoose.org>']
		self._homepage = 'http://jokosher.org'
		self._license = 'GPL2+'
		self._source = 'http://launchpad.net/jokosher/0.11/0.11.1/+download/jokosher-0.11.1.tar.gz'
		self._build_method = 'python application'

		self._build_requirements = ['python-support']

		self._short_description = u"simple and easy to use audio multi-tracker"

		self._long_description = u"Jokosher is a simple and poweful multi-track studio. Jokosher provides a\n" + \
									u"complete application for recording, editing, mixing and exporting audio, and\n" + \
									u"has been specifically designed with usability in mind. The developers behind\n" + \
									u"Jokosher have re-thought audio production at every level, and created\n" + \
									u"something devilishly simple to use."

		self._changelog = [{"version" : "0.11.1", "time" : "Fri, 21 Aug 2009 19:49:12 -0700", "text" : u"Initial release" } ]

class Jokosher(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'jokosher'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._install_requirements = ['python-cairo', 
										'python-dbus', 
										'python-glade2', 
										'python-gtk2', 
										'python-gst0.10', 
										'gstreamer0.10-gnonlin (>= 0.10.8)', 
										'gstreamer0.10-plugins-good (>= 0.10.9)', 
										'gstreamer0.10-plugins-base (>= 0.10.12)', 
										'python-setuptools']

