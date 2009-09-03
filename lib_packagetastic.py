#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, time, re
import commands
import pexpect
import base64
import gc

packagetastic_categories = [
	'Applications/Archiving', 
	'Applications/Audio', 
	'Applications/Communications', 
	'Applications/Databases', 
	'Applications/Editors', 
	'Applications/Emulators', 
	'Applications/Engineering', 
	'Applications/File', 
	'Applications/Games', 
	'Applications/Graphics', 
	'Applications/HamRadio', 
	'Applications/Internet', 
	'Applications/Multimedia', 
	'Applications/Office', 
	'Applications/Publishing', 
	'Applications/System', 
	'Applications/Text', 
	'Applications/Video', 
	'Applications/Virtualization', 
	'Development/Debuggers', 
	'Development/Languages', 
	'Development/Libraries', 
	'Development/System', 
	'Development/Tools', 
	'Development/VersionControlSystems', 
	'Documentation', 
	'Localization', 
	'System/Base', 
	'System/Daemons', 
	'System/Databases', 
	'System/Desktops', 
	'System/Drivers', 
	'System/FileSystems', 
	'System/Fonts', 
	'System/Kernel', 
	'System/Libraries', 
	'System/Shells', 
	'System/Virtualization', 
	'System/WebServers'
]

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

packagetastic_dir = None
def init_packagetastic():
	global packagetastic_dir
	packagetastic_dir = commands.getoutput('pwd')
	if packagetastic_dir.count('packagetastic') == 0:
		raise Exception("Could not find packagetastic in the current path.")


def setup_source_code(meta):
	# Make sure the source code exists
	if not os.path.isfile("sources/" + meta.source.split('/')[-1]):
		print substitute_strings("Missing source code at: sources/" + meta.source.split('/')[-1] + ". Exiting ...", meta.to_hash())
		exit()

	# Convert any .tar.bz2 files to .tar.gz
	if meta.source.split('/')[-1].endswith('.tar.bz2'):
		os.chdir('sources')
		dir_name = meta.source.split('/')[-1].rstrip('.tar.bz2')
		print "Converting bzip source code to gzip ..."
		commands.getoutput("tar xjf " + meta.source.split('/')[-1])
		commands.getoutput(substitute_strings("mv " + dir_name + " #{name}-#{version}", meta.to_hash()))
		commands.getoutput(substitute_strings("tar -czf #{name}-#{version}.tar.gz #{name}-#{version}", meta.to_hash()))
		commands.getoutput(substitute_strings("rm -rf #{name}-#{version}", meta.to_hash()))
		meta.source = meta.source.rstrip(meta.source.split('/')[-1]) + substitute_strings("#{name}-#{version}.tar.gz", meta.to_hash())
		os.chdir('..')

	# Uncompress the source code
	print "Uncompressing source code ..."
	if not os.path.isdir("builds"): os.mkdir("builds")
	commands.getoutput(substitute_strings("cp sources/" + meta.source.split('/')[-1] + " builds/#{name}_#{version}.orig.tar.gz", meta.to_hash()))
	os.chdir("builds")
	commands.getoutput(substitute_strings("tar xzf #{name}_#{version}.orig.tar.gz", meta.to_hash()))
	os.chdir(substitute_strings("#{name}-#{version}", meta.to_hash()))

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

class Changelog(object):
	def __init__(self, version, release, time, text):
		self._version = version
		self._release = release
		self._time = time
		self._text = text

	def get_version(self): return self._version
	version = property(get_version)

	def get_release(self): return self._release
	release = property(get_release)

	def get_time(self): return self._time
	time = property(get_time)

	def get_text(self): return self._text
	text = property(get_text)

class BaseMeta(object):
	def __init__(self):
		self._name = None
		self._priority = None
		self._category = None
		self._authors = []
		self._copyright = []
		self._packager_name = None
		self._packager_email = None
		self._homepage = None
		self._license = None
		self._source = None
		self._build_requirements = []
		self._short_description = None
		self._long_description = None
		self._changelog = None

	def get_name(self): return self._name
	name = property(get_name)

	def get_priority(self): return self._priority
	priority = property(get_priority)

	def get_category(self): return self._category
	category = property(get_category)

	def get_authors(self): return self._authors
	authors = property(get_authors)

	def get_copyright(self): return self._copyright
	copyright = property(get_copyright)

	def get_packager_name(self): return self._packager_name
	def set_packager_name(self, value): self._packager_name = value
	packager_name = property(get_packager_name, set_packager_name)

	def get_packager_email(self): return self._packager_email
	def set_packager_email(self, value): self._packager_email = value
	packager_email = property(get_packager_email, set_packager_email)

	def get_homepage(self): return self._homepage
	homepage = property(get_homepage)

	def get_license(self): return self._license
	license = property(get_license)

	def get_source(self): return self._source
	source = property(get_source)

	def get_build_requirements(self): return self._build_requirements
	build_requirements = property(get_build_requirements)

	def get_short_description(self): return self._short_description
	short_description = property(get_short_description)

	def get_long_description(self): return self._long_description
	long_description = property(get_long_description)

	def get_changelog(self): return self._changelog
	changelog = property(get_changelog)

	def get_version(self):
		return self._changelog[0].version
	version = property(get_version)

	def get_release(self):
		return self._changelog[0].release
	release = property(get_release)

	def get_patches(self):
		global packagetastic_dir
		patches = []
		if os.path.isdir(packagetastic_dir + "/patches/" + self.name):
			patch_files = os.listdir(packagetastic_dir + "/patches/" + self.name)
			patch_files.sort()
			for patch_file in patch_files:
				if not patch_file.endswith('.patch'): continue
				patches.append(patch_file)
		return patches
	patches = property(get_patches)

	def after_install(self): pass
	def before_install(self): pass
	def after_uninstall(self): pass
	def before_uninstall(self): pass

	def to_hash(self):
		retval={ 'authors' : self.authors, 
				'after_install' : self.after_install(), 
				'after_uninstall' : self.after_uninstall(), 
				'before_install' : self.before_install(), 
				'before_uninstall' : self.before_uninstall(), 
				'build_requirements' : self.build_requirements, 
				'category' : self.category, 
				'changelog' : self.changelog, 
				'copyright' : self.copyright, 
				'homepage' : self.homepage, 
				'license' : self.license, 
				'long_description' : self.long_description, 
				'name' : self.name, 
				'packager_email' : self.packager_email, 
				'packager_name' : self.packager_name, 
				'patches' : self.patches, 
				'priority' : self.priority, 
				'release' : str(self.release), 
				'short_description' : self.short_description, 
				'source' : self.source, 
				'version' : self.version, 
				}

		# Make changes that make data easier to use
		retval['year'] = time.strftime("%Y", time.localtime())
		retval['timestring'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
		retval['human_timestring'] = time.strftime("%a %b %d %Y", time.localtime())
		retval['license_text'] = licenses[self.license]

		return retval

class BasePackage(object):
	def __init__(self):
		self._name = None
		self._build_method = None
		self._alternate_name = None
		self._priority = None
		self._category = None
		self._install_requirements = []
		self._additional_description = u""

	def get_name(self): return self._name
	name = property(get_name)

	def get_build_method(self): return self._build_method
	build_method = property(get_build_method)

	def get_alternate_name(self): return self._alternate_name
	alternate_name = property(get_alternate_name)

	def get_priority(self): return self._priority
	priority = property(get_priority)

	def get_category(self): return self._category
	category = property(get_category)

	def get_install_requirements(self): return self._install_requirements
	install_requirements = property(get_install_requirements)

	def get_additional_description(self): return self._additional_description
	additional_description = property(get_additional_description)

	def to_hash(self):
		retval={'additional_description' : self.additional_description, 
				'alternate_name' : self.alternate_name, 
				'build_method' : self.build_method, 
				'category' : self.category, 
				'install_requirements' : self.install_requirements, 
				'name' : self.name, 
				'priority' : self.priority, 
				}

		# Make changes that make data easier to use
		retval['year'] = time.strftime("%Y", time.localtime())
		retval['timestring'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
		retval['human_timestring'] = time.strftime("%a %b %d %Y", time.localtime())

		return retval

def validate_package(meta, packages):
	# Make sure meta and packages were loaded
	if not meta:
		print "No BaseMeta class was found in the stem file. Exiting ..."
		exit()
	if len(packages) == 0:
		print "No BasePackage classes were found in the stem file. Exiting ..."
		exit()

	# Make sure unicode is used for the correct fields
	for author in meta.authors:
		if not isinstance(author, unicode):
			print "Stem file is Broken. The authors field \"" + author + "\" is not unicode. Exiting ..."
			exit()

	for copyright in meta.copyright:
		if not isinstance(copyright, unicode):
			print "Stem file is Broken. The copyright field \"" + copyright + "\" is not unicode. Exiting ..."
			exit()

	if not isinstance(meta.short_description, unicode):
		print "Stem file is Broken. The short_description field \"" + meta.short_description + "\" is not unicode. Exiting ..."
		exit()

	if not isinstance(meta.long_description, unicode):
		print "Stem file is Broken. The long_description field \"" + meta.long_description + "\" is not unicode. Exiting ..."
		exit()

	for entry in meta.changelog:
		if not isinstance(entry.text, unicode):
			print "Stem file is Broken. The changelog's text field for \"version:" + entry.version + ' -- time:' + entry.time + "\" is not unicode. Exiting ..."
			exit()

	for package in packages:
		if not isinstance(package.additional_description, unicode):
			print "Stem file is Broken. The additional_description field \"" + package.additional_description + "\" is not unicode. Exiting ..."
			exit()

def build(distro_name, package_name):
	# Make sure the packager_name file exists
	if not os.path.isfile('packager_name'):
		print "Add the packager name to the 'packager_name' file."
		exit()

	# Make sure the packager_email file exists
	if not os.path.isfile('packager_email'):
		print "Add the packager email address to the 'packager_email' file."
		exit()

	# Make sure the root_password file exists
	if not os.path.isfile('root_password'):
		print "Add the root password to the 'root_password' file."
		exit()

	# Make sure the gpg_password file exists
	if not os.path.isfile('gpg_password'):
		print "Add the gpg password to the 'gpg_password' file."
		exit()

	f = open('packager_name')
	packager_name = f.read()[0:-1]
	f.close()

	f = open('packager_email')
	packager_email = f.read()[0:-1]
	f.close()

	f = open('root_password')
	root_password = f.read()[0:-1]
	f.close()

	f = open('gpg_password')
	gpg_password = f.read()[0:-1]
	f.close()

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

	# Get the package meta data
	meta = None
	for obj in gc.get_objects():
		if type(obj) == type and issubclass(obj, BaseMeta) and obj().name == package_name:
			meta = obj()
			break

	# Get the packages to build
	packages = []
	for obj in gc.get_objects():
		if type(obj) == type and obj != BasePackage and issubclass(obj, BasePackage):
			package = obj()
			packages.append(package)

	# Validate the meta and packages
	validate_package(meta, packages)

	# Build the package for that distro
	meta.packager_name = packager_name
	meta.packager_email = packager_email
	builder = eval('Builder()')
	builder.build(meta, packages, root_password, gpg_password)


