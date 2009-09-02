#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'pyactiveresource'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._authors = [u'Jared Kuolt <me@superjared.com>', u'Mark Roach <mrroach@google.com>']
		self._copyright = [u'2008 Jared Kuolt', u'2008 Mark Roach', u'2008 Google Inc.']
		self._homepage = 'http://code.google.com/p/pyactiveresource/'
		self._license = 'MIT'
		self._source = 'http://code.google.com/p/pyactiveresource/pyactiveresource-1.0.0.tar.gz'
		self._build_method = 'python library'

		self._build_requirements = []

		self._short_description = u"ActiveResource for Python."

		self._long_description = u"Active Resource attempts to provide a coherent wrapper object-relational \n" + \
								u"mapping for REST web services. It follows the same philosophy as Active Record, \n" + \
								u"in that one of its prime aims is to reduce the amount of code needed to map to \n" + \
								u"these resources."

		self._changelog = [Changelog(version="1.0.0", release=1, time="Fri, 07 Aug 2009 18:32:26 -0700", text=u"Initial release") ]

class Pyactiveresource(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'pyactiveresource'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = []


