#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'spacepony-client'
		self._category = 'Applications/Internet'
		self._priority = 'optional'
		self._authors = [u'Matthew Brennan Jones <mattjones@workhorsy.org>']
		self._copyright = [u'2009 Matthew Brennan Jones']
		self._homepage = 'http://launchpad.net/spacepony'
		self._license = 'AGPL3+'
		self._source = 'http://launchpad.net/spacepony/trunk/0.1.0/+download/spacepony-client-0.1.0.tar.gz'

		self._build_requirements = ['python-dev', 'gettext', 'desktop-file-utils']

		self._short_description = u"Desktop settings syncing client"

		self._long_description = u"Space Pony makes it easy to sync your Linux desktop settings \n" + \
									u"to the web and other machines. "

		self._changelog = [Changelog(version="0.1.0", release=1, time="Fri, 07 Aug 2009 18:32:26 -0700", text=u"Initial release") ]

class Shrip(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'spacepony-client'
		self._build_method = 'python application'
		self._category = 'Applications/Internet'
		self._priority = 'optional'
		self._install_requirements = ['python-gobject', 'python-gconf', 'python-vte', 
										'python-inotify', 'pyactiveresource']


