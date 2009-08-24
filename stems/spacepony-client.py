#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'spacepony-client'
		self._section = 'misc'
		self._priority = 'optional'
		self._authors = ['Matthew Brennan Jones <mattjones@workhorsy.org>']
		self._copyright = ['2009 Matthew Brennan Jones']
		self._homepage = 'http://launchpad.net/spacepony'
		self._license = 'AGPL3+'
		self._source = 'http://launchpad.net/spacepony/trunk/0.1.0/+download/spacepony-client-0.1.0.tar.gz'
		self._build_method = 'python application'

		self._build_requirements = ['python-devel', 'gettext', 'desktop-file-utils']

		self._short_description = "Desktop settings syncing client"

		self._long_description = "Space Pony makes it easy to sync your Linux desktop settings \n" + \
									"to the web and other machines. "

		self._changelog = [{"version" : "0.1.0", "time" : "Fri, 07 Aug 2009 18:32:26 -0700", "text" : "Initial release" } ]

class Shrip(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'spacepony-client'
		self._section = 'misc'
		self._priority = 'optional'
		self._install_requirements = ['python-gobject', 'python-gconf', 'python-vte', 
										'python-pyinotify', 'pyactiveresource']

