#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class PyactiveresourcePackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'pyactiveresource'
		self._version = '1.0.0'
		self._section = 'python'
		self._priority = 'optional'
		self._authors = ['Jared Kuolt <me@superjared.com>', 'Mark Roach <mrroach@google.com>']
		self._copyright = ['2008 Jared Kuolt', '2008 Mark Roach', '2008 Google Inc.']
		self._homepage = 'http://code.google.com/p/pyactiveresource/'
		self._license = 'MIT'
		self._source = 'http://code.google.com/p/pyactiveresource/pyactiveresource-1.0.0.tar.gz'
		self._build_method = 'python library'

		self._build_requirements = []

		self._install_requirements = []

		self._short_description = "ActiveResource for Python."

		self._long_description = "Active Resource attempts to provide a coherent wrapper object-relational \n" + \
								"mapping for REST web services. It follows the same philosophy as Active Record,\n" + \
								" in that one of its prime aims is to reduce the amount of code needed to map to\n" + \
								" these resources."

		self._changelog = [{"version" : "1.0.0", "time" : "Fri, 07 Aug 2009 18:32:26 -0700 ", "text" : "Initial release" } ]




