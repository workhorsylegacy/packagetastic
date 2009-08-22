#!/usr/bin/env python

import os, time, re
import commands
import pexpect
import base64


licenses = { 'GPL2+' : \
"""    This package is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this package; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
"""
,
'GPL3+' : \
"""This package is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

gPodder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
,
'AGPL3+' : \
"""   This package is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This package is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this package.  If not, see <http://www.gnu.org/licenses/>.
"""
,
'LGPL2.1' : \
"""
    This package is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2 of the License, or (at your option) any later version.

    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this package; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
"""
,
'MIT' : \
"""
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
}

def to_package_class_name(package_name):
	name = package_name.capitalize() + 'Package()'
	retval = ''

	prev_was_dash = False
	for i in range(len(name)):
		if prev_was_dash:
			retval += name[i].capitalize()
		else:
			retval += name[i]

		prev_was_dash = (name[i] == '-')

	return retval.replace('-', '')

def substitute_strings(string, sub_hash):
	result = string[:]

	for key, replacement in sub_hash.iteritems():
		p = re.compile("#\{" + key + "\}")

		if replacement == None: replacement = ''

		while True:
			# Look for a pattern, and return if there was none
			match = p.search(result)
			if match == None: break

			# Replace the pattern with the replacement
			start, end = match.span()
			result = result[:start] + replacement + result[end:]
	return result

class BasePackage(object):
	# FIXME: This should be just a constructor that is called when children are __init__()
	def call_parent_constructor(self):
		self._name = None
		self._alternate_name = None
		self._version = None
		self._section = None
		self._priority = None
		self._authors = []
		self._copyright = []
		self._packager_name = None
		self._packager_email = None
		self._homepage = None
		self._license = None
		self._source = None
		self._build_method = None
		self._build_requirements = []
		self._install_requirements = []
		self._short_description = None
		self._long_description = None
		self._distro_style = None
		self._changelog = None

	def get_name(self): return self._name
	def set_name(self, value): self._name = value
	name = property(get_name, set_name)

	def get_alternate_name(self): return self._alternate_name
	def set_alternate_name(self, value): self._alternate_name = value
	alternate_name = property(get_alternate_name, set_alternate_name)

	def get_version(self): return self._version
	def set_version(self, value): self._version = value
	version = property(get_version, set_version)

	def get_section(self): return self._section
	def set_section(self, value): self._section = value
	section = property(get_section, set_section)

	def get_priority(self): return self._priority
	def set_priority(self, value): self._priority = value
	priority = property(get_priority, set_priority)

	def get_authors(self): return self._authors
	def set_authors(self, value): self._authors = value
	authors = property(get_authors, set_authors)

	def get_copyright(self): return self._copyright
	def set_copyright(self, value): self._copyright = value
	copyright = property(get_copyright, set_copyright)

	def get_packager_name(self): return self._packager_name
	def set_packager_name(self, value): self._packager_name = value
	packager_name = property(get_packager_name, set_packager_name)

	def get_packager_email(self): return self._packager_email
	def set_packager_email(self, value): self._packager_email = value
	packager_email = property(get_packager_email, set_packager_email)

	def get_homepage(self): return self._homepage
	def set_homepage(self, value): self._homepage = value
	homepage = property(get_homepage, set_homepage)

	def get_license(self): return self._license
	def set_license(self, value): self._license = value
	license = property(get_license, set_license)

	def get_source(self): return self._source
	def set_source(self, value): self._source = value
	source = property(get_source, set_source)

	def get_build_method(self): return self._build_method
	def set_build_method(self, value): self._build_method = value
	build_method = property(get_build_method, set_build_method)

	def get_build_requirements(self): return self.distroify_requirements(self._build_requirements)
	def set_build_requirements(self, value): self._build_requirements = value
	build_requirements = property(get_build_requirements, set_build_requirements)

	def get_install_requirements(self): return self.distroify_requirements(self._install_requirements)
	def set_install_requirements(self, value): self._install_requirements = value
	install_requirements = property(get_install_requirements, set_install_requirements)

	def get_short_description(self): return self._short_description
	def set_short_description(self, value): self._short_description = value
	short_description = property(get_short_description, set_short_description)

	def get_long_description(self): return self._long_description
	def set_long_description(self, value): self._long_description = value
	long_description = property(get_long_description, set_long_description)

	def get_distro_style(self): return self._distro_style
	def set_distro_style(self, value): self._distro_style = value
	distro_style = property(get_distro_style, set_distro_style)

	def get_changelog(self): return self._changelog
	def set_changelog(self, value): self._changelog = value
	changelog = property(get_changelog, set_changelog)

	def after_install(self): pass
	def before_install(self): pass
	def after_uninstall(self): pass
	def before_uninstall(self): pass

	def to_hash(self, additional_fields=None):
		retval={ 'name' : self.name, 
				'alternate_name' : self.alternate_name, 
				'version' : self.version, 
				'section' : self.section, 
				'priority' : self.priority, 
				'authors' : self.authors, 
				'copyright' : self.copyright, 
				'packager_name' : self.packager_name, 
				'packager_email' : self.packager_email, 
				'homepage' : self.homepage, 
				'license' : self.license, 
				'source' : self.source, 
				'build_method' : self.build_method, 
				'build_requirements' : self.build_requirements, 
				'install_requirements' : self.install_requirements, 
				'short_description' : self.short_description, 
				'long_description' : self.long_description, 
				'after_install' : self.after_install(), 
				'before_install' : self.before_install(), 
				'after_uninstall' : self.after_uninstall(), 
				'before_uninstall' : self.before_uninstall()
				}

		# Add custom data
		if additional_fields != None:
			retval.update(additional_fields)

		# Get the distros current style for joining lists of items
		join_style = ''
		if self.distro_style == 'fedora':
			join_style = ' '
		elif self.distro_style == 'ubuntu':
			join_style = ', '

		# Make changes that make data easier to use
		retval['authors'] = str.join("\n    ", retval['authors'])
		retval['copyright'] = str.join("\n    ", retval['copyright'])
		retval['build_requirements'] = str.join(join_style, retval['build_requirements'])
		retval['install_requirements'] = str.join(join_style, retval['install_requirements'])
		retval['year'] = time.strftime("%Y", time.localtime())
		retval['timestring'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
		retval['human_timestring'] = time.strftime("%a %b %d %Y", time.localtime())
		retval['license_text'] = licenses[self.license]
		retval['upstream_authors'] = ('Upstream Authors', 'Upstream Author')[ len(self.authors) > 0 ]

		return retval

	def distroify_requirements(self, requirements):
		# Convert the requirements to the style for the distro
		retval = []
		for req in requirements:
			if self.distro_style == 'fedora' and req.endswith('-dev'):
				req += 'el'
			elif self.distro_style == 'ubuntu' and req.endswith('-devel'):
				req = req[:-2]

			retval.append(req)

		return retval


def build(distro_name, package_name):
	# Make sure we have a distro file that matches the name
	if not os.path.isfile('distros/' + distro_name + '.py'):
		print "Packagetastic does not know how to build for the distro '" + distro_name + "'. Exiting ..."
		exit()

	# Make sure we have a stem file that matches the name
	if not os.path.isfile('stems/' + package_name + '.py'):
		print "Packagetastic does not have a stem file for the package '" + package_name + "'. Exiting ..."
		exit()

	# Load the distro and stem files
	execfile('distros/' + distro_name + '.py')
	execfile('stems/' + package_name + '.py')

	# Get the package to build
	package = eval(to_package_class_name(package_name))

	# Make sure the packager_name file exists
	if not os.path.isfile('packager_name'):
		print "Add the packager name to the 'packager_name' file."
		exit()

	# Make sure the packager_email file exists
	if not os.path.isfile('packager_email'):
		print "Add the packager email address to the 'packager_email' file."
		exit()

	f = open('packager_name')
	package.packager_name = f.read()[0:-1]
	f.close()

	f = open('packager_email')
	package.packager_email = f.read()[0:-1]
	f.close()

	# Build the package for that distro
	package.distro_style = distro_name
	builder = eval('Builder()')
	builder.build(package)




