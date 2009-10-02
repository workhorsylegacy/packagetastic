#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, time, re
import commands
import platform
import pexpect
import base64
import gc
import distutils
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
	if os.path.isdir("builds"): commands.getoutput("rm -rf builds")
	os.mkdir("builds")
	commands.getoutput(substitute_strings("cp sources/" + source.split('/')[-1] + " builds/#{name}_#{version}.orig.tar.gz", meta.to_hash()))
	os.chdir("builds")
	commands.getoutput(substitute_strings("tar xzf #{name}_#{version}.orig.tar.gz", meta.to_hash()))
	os.chdir(substitute_strings("#{name}-#{version}", meta.to_hash()))
'''
def get_file_structure_for_package(meta, packages, params):
	# FIXME: We no longer need to probe for file names on each build.
	# Move the build/probe code to the ./packagetastic update_files blah area 
	# Set the default values
	params['bindir_entries'] = []
	params['infodir_entries'] = []
	params['mandir_entries'] = []
	params['datadir_entries'] = []
	params['libdir_entries'] = []
	params['docs'] = []
	params['import_python_sitelib'] = False
	params['has_mime'] = False
	params['has_info'] = False
	params['has_icon_cache'] = False
	params['has_icons'] = False
	params['has_omf'] = False
	params['has_lang'] = os.path.isdir('po')
	params['has_desktop_file'] = False
	params['desktop_file_name'] = None

	# Find out which build methods are used
	params['builds_with_autotools'] = os.path.isfile('Makefile.in')
	params['builds_with_python'] = os.path.isfile('setup.py')

	# Build the program in a sub directory
	os.mkdir('packagetastic_build')
	if params['builds_with_autotools']:
		pwd = commands.getoutput('pwd')
		commands.getoutput('./configure --prefix=' + pwd + '/packagetastic_build')
		commands.getoutput('make')
		commands.getoutput('make install')
	elif params['builds_with_python']:
		commands.getoutput('python setup.py bdist')

		if not os.path.isdir('dist/'):
			print "Broken python setup.py. Ran 'python setup.py bdist', but found no *.tar.gz. Exiting ..."
			exit()

		tgz_name = os.listdir('dist/')[0]
		if tgz_name.count('tar.gz') == 0:
			print "Broken python setup.py. Ran 'python setup.py bdist', but found no *.tar.gz. Exiting ..."
			exit()

		commands.getoutput('mv dist/' + tgz_name + ' packagetastic_build/' + tgz_name)
		os.chdir('packagetastic_build/')
		commands.getoutput("tar xzf " + tgz_name)
		commands.getoutput("rm " + tgz_name)
		os.chdir('..')
		commands.getoutput('mv packagetastic_build/usr/ packagetastic_build_usr/')
		commands.getoutput('rm -rf packagetastic_build/')
		commands.getoutput('mv packagetastic_build_usr/ packagetastic_build/')

	for package in packages:
		if package.build_method.count('python') and params['builds_with_python']:
			params['import_python_sitelib'] = True

	# Get the docs, lang, and example params
	for doc in ['README', 'COPYING', 'ChangeLog', 'LICENSE', 'AUTHORS']:
		if os.path.isfile(doc):
			params['docs'].append(doc)
	for doc in ['doc', 'examples']:
		if os.path.isdir(doc):
			params['docs'].append(doc)
	params['docs'].sort()

	# Get a list of all the files
	files = []
	entries = os.listdir("packagetastic_build/")
	while len(entries) > 0:
		entry = entries.pop(0)
		if os.path.isdir("packagetastic_build/" + entry):
			for sub in os.listdir("packagetastic_build/" + entry):
				entries.append(entry + '/' + sub)
		elif os.path.isfile("packagetastic_build/" + entry):
			files.append(entry)

	simple_name = meta.name.lower().replace('_', '').replace('-', '')

	# Add the files to the categories they belong to
	# FIXME: get the mime, omf, icons
	for entry in files:
		if entry.startswith('bin/'):
			params['bindir_entries'].append(entry[len('bin/'):])
		elif entry.startswith('info/'):
			if entry != "info/dir":
				params['infodir_entries'].append(entry[len('info/'):] + '*')
				params['has_info'] = True
		elif entry.startswith('share/man/'):
			params['mandir_entries'].append(entry[len('share/man/'):] + '*')
		elif entry.startswith('man/'):
			params['mandir_entries'].append(entry[len('man/'):] + '*')
		elif entry.startswith('share/icons/'):
			if entry == 'share/icons/hicolor/icon-theme.cache':
				params['has_icon_cache'] = True
			else:
				params['datadir_entries'].append(entry[len('share/'):])
				params['has_icons'] = True
		elif entry.startswith('share/pixmaps/'):
			params['datadir_entries'].append(entry[len('share/'):])
		elif entry.startswith('share/applications/'):
			params['datadir_entries'].append(entry[len('share/'):])
			if entry.endswith('.desktop'):
				params['has_desktop_file'] = True
				params['desktop_file_name'] = entry[len('share/'):]
		elif entry.startswith('share/mime/'):
			params['datadir_entries'].append(entry[len('share/'):])
			params['has_mime'] = True
		elif entry.startswith('share/gnome/help/'):
			params['datadir_entries'].append(entry[len('share/'):])
		elif entry.startswith('share/omf/'):
			params['datadir_entries'].append(entry[len('share/'):])
			params['has_omf'] = True
		elif entry.startswith('share/' + simple_name + '/'):
			params['datadir_entries'].append(entry[len('share/'):])
		elif entry.startswith('lib/'):
			params['libdir_entries'].append(entry[len('lib/'):])
'''

def get_file_structure_for_package(meta, packages, params):
	# Set the default values
	params['infodir_entries'] = []
	params['mandir_entries'] = []
	params['datadir_entries'] = []
	params['libdir_entries'] = []
	params['docs'] = []
	params['import_python_sitelib'] = False
	params['has_mime'] = False
	params['has_info'] = False
	params['has_icon_cache'] = False
	params['has_icons'] = False
	params['has_omf'] = False
	params['has_lang'] = os.path.isdir('po')
	params['has_desktop_file'] = False
	params['desktop_file_name'] = None

	# Find out which build methods are used
	params['builds_with_autotools'] = os.path.isfile('Makefile.in')
	params['builds_with_python'] = os.path.isfile('setup.py')

	for package in packages:
		if package.build_method.count('python') and params['builds_with_python']:
			params['import_python_sitelib'] = True

	# Get the docs, lang, and example params
	for doc in ['README', 'COPYING', 'ChangeLog', 'LICENSE', 'AUTHORS']:
		if os.path.isfile(doc):
			params['docs'].append(doc)
	for doc in ['doc', 'examples']:
		if os.path.isdir(doc):
			params['docs'].append(doc)
	params['docs'].sort()

	simple_name = meta.name.lower().replace('_', '').replace('-', '')

	# Add the files to the categories they belong to
	for entry in packages[0].files:
		if entry.startswith('/usr/share/info/'):
			if not entry.startswith("/usr/share/info/dir"):
				params['has_info'] = True
		elif entry.startswith('/usr/share/icons/'):
			if entry == '/usr/share/icons/hicolor/icon-theme.cache':
				params['has_icon_cache'] = True
			else:
				params['has_icons'] = True
		elif entry.startswith('/usr/share/applications/'):
			if entry.endswith('.desktop'):
				params['has_desktop_file'] = True
				params['desktop_file_name'] = entry[len('/usr/share/'):]
		elif entry.startswith('/usr/share/mime/'):
			params['has_mime'] = True
		elif entry.startswith('/usr/share/omf/'):
			params['has_omf'] = True

def requirements_to_distro_specific(distro_name, requirements):
	distro_requirements = []
	for requirement in requirements:
		name, version = '', ''
		if requirement.count(' ') > 0:
			name = requirement.split()[0]
			version = requirement[len(name):]
		else:
			name = requirement.split()[0]

		for new_name in package_names[name][distro_name]:
			distro_requirements.append(new_name + version)

	return distro_requirements

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
		self._files = []
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

	def get_files(self): return self._files
	files = property(get_files)

	def get_additional_description(self): return self._additional_description
	additional_description = property(get_additional_description)

	def to_hash(self):
		retval={'additional_description' : self.additional_description, 
				'alternate_name' : self.alternate_name, 
				'build_method' : self.build_method, 
				'category' : self.category, 
				'install_requirements' : self.install_requirements, 
				'files' : self._files, 
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

	# Make sure we know about the name
	package_names = globals()['package_names']
	for package in packages:
		if not package_names.has_key(package.name):
			print "The package name \"" + package.name + "\" was not found. Please add it to package_names.py. Exiting ..."
			exit()

	# Make sure we know about the build requirements
	for build_requirement in meta.build_requirements:
		build_requirement = build_requirement.split()[0]
		if not package_names.has_key(build_requirement):
			print "Stem file is Broken. The build requirement \"" + build_requirement + "\" was not found. Please add it to package_names.py. Exiting ..."
			exit()
		elif package_names[build_requirement].has_key(distro_name) and \
			len(package_names[build_requirement][distro_name]) == 0:
			print "Stem file is Broken. The build requirement \"" + build_requirement + "\" is missing for this distro. Please add it to package_names.py. Exiting ..."
			exit()

	# Make sure we know about the install requirements
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

def build(distro_name, package_name, use_chroot, is_interactive):
	# Make sure the packager_name file exists
	if not os.path.isfile('packager_name'):
		print "Add the packager name to the 'packager_name' file."
		exit()

	# Make sure the packager_email file exists
	if not os.path.isfile('packager_email'):
		print "Add the packager email address to the 'packager_email' file."
		exit()

	# Make sure the packager_sudo file exists
	if not os.path.isfile('packager_sudo'):
		print "Add the sudo password to the 'packager_sudo' file."
		exit()

	# Make sure the packager_gpg file exists
	if not os.path.isfile('packager_gpg'):
		print "Add the gpg password to the 'packager_gpg' file."
		exit()

	f = open('packager_name')
	packager_name = f.read()[0:-1]
	f.close()

	f = open('packager_email')
	packager_email = f.read()[0:-1]
	f.close()

	f = open('packager_sudo')
	packager_sudo = f.read()[0:-1]
	f.close()

	f = open('packager_gpg')
	packager_gpg = f.read()[0:-1]
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

	# Convert the requirements to be distro specific
	meta.__dict__['_build_requirements'] = \
		requirements_to_distro_specific(distro_name, meta.build_requirements)
	for package in packages:
		package.__dict__['_install_requirements'] = \
			requirements_to_distro_specific(distro_name, package.install_requirements)

	# Build the package for that distro
	meta.packager_name = packager_name
	meta.packager_email = packager_email
	builder = eval('Builder()')
	builder.build(meta, packages, packager_sudo, packager_gpg, use_chroot, is_interactive)


