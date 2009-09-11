#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, time, re
import commands
import platform
import pexpect
import base64
import gc
from helper import *

exec_file("package_names.py", globals(), locals())

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

packagetastic_dir = None
def init_packagetastic(distro_name, package_name):
	# Make sure we are on linux
	if platform.system() != 'Linux':
		print "Packagetastic only works on Linux, not '" + platform.system() + "'. Exiting ..."
		exit()

	# Make sure we have a distro file that matches the name
	if not os.path.isfile('distros/' + distro_name + '.py'):
		print "Packagetastic does not know how to build for the distro '" + distro_name + "'. Exiting ..."
		exit()

	# Make sure we have a stem file that matches the name
	if not os.path.isfile('stems/' + package_name + '.py'):
		print "Packagetastic does not have a stem file for the package '" + package_name + "'. Exiting ..."
		exit()

	# Try to get the OS name
	os_name = None
	if commands.getoutput('whereis lsb_release').split(':')[1] != '':
		os_name = commands.getoutput('lsb_release -is')
	elif os.path.isfile('/etc/distro-release'):
		os_name = commands.getoutput('cat /etc/distro-release')
	elif os.path.isfile('/etc/system-release'):
		os_name = commands.getoutput('cat /etc/system-release').split()[0]
	elif os.path.isfile('/etc/lsb-release'):
		os_name = str.split(str.split(commands.getoutput('cat /etc/lsb-release'), "DISTRIB_ID=")[1], "\n")[0]
	elif os.path.isfile('/etc/debian_version'):
		os_name = "Debian"
	elif os.path.isfile('/etc/fedora-release').split()[0]:
		os_name = "Fedora"
	elif os.path.isfile('/etc/SuSE-release'):
		os_name = "SuSE"
	elif os.path.isfile('/etc/mandriva-release'):
		os_name = "Mandriva"
	else:
		print "Packagetastic could not find your Linux distribution name. Exiting ..."
		exit()

	# Make sure we got a distro we can build for
	# NOTE: Other distros are LinuxMint, Mandriva, SuSE
	if ['Debian', 'Ubuntu', 'Fedora'].count(os_name) == 0:
		print "Packagetastic does not yet work with the Linux distribution '" + os_name + "'. Exiting ..."
		exit()

	# Make sure we are on the distro we want to build for
	if distro_name != os_name.lower():
		print "Packagetastic cannot build packages for '" + distro_name + "' while on '" + os_name + "'. Exiting ..."
		exit()

	# Get the path of packagetastic's location
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
	source = meta.source
	if meta.source.split('/')[-1].endswith('.tar.bz2'):
		os.chdir('sources')
		dir_name = meta.source.split('/')[-1].rstrip('.tar.bz2')
		print "Converting bzip source code to gzip ..."
		commands.getoutput("tar xjf " + meta.source.split('/')[-1])
		commands.getoutput(substitute_strings("mv " + dir_name + " #{name}-#{version}", meta.to_hash()))
		commands.getoutput(substitute_strings("tar -czf #{name}-#{version}.tar.gz #{name}-#{version}", meta.to_hash()))
		commands.getoutput(substitute_strings("rm -rf #{name}-#{version}", meta.to_hash()))
		source = meta.source.rstrip(meta.source.split('/')[-1]) + substitute_strings("#{name}-#{version}.tar.gz", meta.to_hash())
		os.chdir('..')

	# Uncompress the source code
	print "Uncompressing source code ..."
	if not os.path.isdir("builds"): os.mkdir("builds")
	commands.getoutput(substitute_strings("cp sources/" + source.split('/')[-1] + " builds/#{name}_#{version}.orig.tar.gz", meta.to_hash()))
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

	def get_license_text(self):
		with open(packagetastic_dir + '/license_headers/' + self.license) as f:
			return f.read()
	license_text = property(get_license_text)

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
				'license_text' : self.license_text, 
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

def validate_package(distro_name, meta, packages):
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

	# Make sure we know about the build dependencies
	package_names = globals()['package_names']
	for build_requirement in meta.build_requirements:
		build_requirement = build_requirement.split()[0]
		if not package_names.has_key(build_requirement):
			print "Stem file is Broken. The build requirement \"" + build_requirement + "\" was not found. Please add it to package_names.py. Exiting ..."
			exit()
		elif package_names[build_requirement].has_key(distro_name) and \
			len(package_names[build_requirement][distro_name]) == 0:
			print "Stem file is Broken. The build requirement \"" + build_requirement + "\" is missing for this distro. Please add it to package_names.py. Exiting ..."
			exit()

	# Make sure we know about the install dependencies
	for package in packages:
		for install_requirement in package.install_requirements:
			install_requirement = install_requirement.split()[0]
			if not package_names.has_key(install_requirement):
				print "Stem file is Broken. The install requirement \"" + install_requirement + "\" was not found. Please add it to package_names.py. Exiting ..."
				exit()
			elif package_names[install_requirement].has_key(distro_name) and \
				len(package_names[install_requirement][distro_name]) == 0:
				print "Stem file is Broken. The install requirement \"" + install_requirement + "\" is missing for this distro. Please add it to package_names.py. Exiting ..."
				exit()
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
	validate_package(distro_name, meta, packages)

	# Build the package for that distro
	meta.packager_name = packager_name
	meta.packager_email = packager_email
	builder = eval('Builder()')
	builder.build(meta, packages, root_password, gpg_password)


