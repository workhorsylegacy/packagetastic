#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'd-feet'
		self._category = 'Development/Tools'
		self._priority = 'extra'
		self._authors = ['John (J5) Palmieri <johnp@redhat.com>']
		self._copyright = ['2003, 2004, 2005, 2006 Red Hat Inc. <http://www.redhat.com/>', 
							'2003 David Zeuthen', 
							'2004 Rob Taylor', 
							'2005, 2006 Collabora Ltd. <http://www.collabora.co.uk/>']
		self._homepage = 'https://fedorahosted.org/d-feet/'
		self._license = 'GPL2+'
		self._source = 'http://johnp.fedorapeople.org/d-feet-0.1.8.tar.gz'
		self._build_method = 'python application'

		self._build_requirements = ['python-support']

		self._short_description = "A D-Bus object browser, viewer and debugger"

		self._long_description = "d-feet is a D-Bus debugger that allow you to:\n" + \
									"* View names on the session and system bus\n" + \
									"* View exported objects, interfaces, methods and signals\n" + \
									"* View the full command line of services on the bus\n" + \
									"* Execute methods with parameters on the bus and see their return values"

		self._changelog = [{"version" : "0.1.8", "time" : "Fri, 21 Aug 2009 20:12:51 -0700", "text" : "Initial release" } ]

class DFeet(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'd-feet'
		self._category = 'Development/Tools'
		self._priority = 'extra'
		self._install_requirements = ['python-dbus (>= 0.82.3)', 
										'python-gtk2', 
										'python-glade2']

