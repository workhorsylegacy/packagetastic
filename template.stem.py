<%doc> \
    This is a template packagetastic stem file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with % \
    \\\\ is replaced with \\n \
</%doc>\
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = '${name}'
		#FIXME: Category is required
		self._category = ''
		self._priority = 'optional'
		#FIXME: Authors are required
		self._authors = []
		#FIXME: Copyright is required
		self._copyright = []
		#FIXME: Homepage is required
		self._homepage = ''
		#FIXME: License is required
		self._license = ''
		self._source = '${source}'

		#FIXME: Build Requirements are required
		self._build_requirements = []

		#FIXME: Short Description is required
		self._short_description = u""

		#FIXME: Long Description is required
		self._long_description = u""

		#FIXME: Add a proper time
		self._changelog = [Changelog(version="${version}", release=1, time="", text=u"Initial release") ]

% for package in packages:
class ${package['name'].capitalize()}(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = "${package['name']}"
		self._build_method = "${package['build_method']}"
		#FIXME: Category is required
		self._category = ''
		self._priority = 'optional'
		#FIXME: Install Requirements are required
		self._install_requirements = []

		#FIXME: This should be simplified to list a directory rather than
		# each file in said directory.
		self._files = [
		% for entry in package['files']:
			'${entry}', 
		% endfor
		]
% endfor

