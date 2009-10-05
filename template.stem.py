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
		self._category = '' #FIXME: required
		self._priority = 'optional'
		self._authors = [] #FIXME: required
		self._copyright = [] #FIXME: required
		self._homepage = '' #FIXME: required
		self._license = '' #FIXME: required
		self._source = '${source}'

		self._build_requirements = []

		self._short_description = u"" #FIXME: required

		self._long_description = u"" #FIXME: required

		#FIXME: Add a proper time
		self._changelog = [Changelog(version="${version}", release=1, time="", text=u"Initial release") ]

% for package in packages:
class ${package['name'].capitalize()}(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = "${package['name']}"
		self._build_method = "" #FIXME: required
		self._category = '' #FIXME: required
		self._priority = 'optional'
		self._install_requirements = []

		#FIXME: May need to be adjusted manually
		self._files = [ 
		% for entry in package['files']:
			'${entry}', 
		% endfor
		]
% endfor

