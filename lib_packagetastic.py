#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, time, re, gc, base64
import commands
import platform
import pexpect
import urllib2
import apt
from helper import *

exec_file("package_names.py", globals(), locals())

packagetastic_package_types = [
	'c application', 
	'c library', 
	'python application', 
	'python library', 
	'mono application', 
	'mono library', 
	'documentation'
]

packagetastic_build_methods = [
	'autotools', 
	'python'
]

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

class MetaPackage(object):
	def __init__(self):
		self._source = None
		self._name = None
		self._priority = None
		self._category = None
		self._build_method = None
		self._authors = []
		self._copyright = []
		self._packager_name = None
		self._packager_email = None
		self._homepage = None
		self._license = None
		self._build_requirements = []
		self._short_description = None
		self._long_description = None
		self._changelog = None

	def get_source(self): return self._source
	source = property(get_source)

	def get_source_file(self):
		extension = None
		if self.source.endswith('.tar.gz'):
			extension = '.tar.gz'
		elif self.source.endswith('.tar.bz2'):
			extension = '.tar.bz2'
		return self.name + '-' + self.version + extension
	source_file = property(get_source_file)

	def get_name(self): return self._name
	name = property(get_name)

	def get_priority(self): return self._priority
	priority = property(get_priority)

	def get_category(self): return self._category
	category = property(get_category)

	def get_build_method(self): return self._build_method
	build_method = property(get_build_method)

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

	def build(self):
		raise Exception("The build method must be overridden by the child class.")

	def configure(self, flags=''):
		child = pexpect.spawn('bash -c "./configure --prefix=/usr ' + flags + '"', timeout=60)
		expected_lines = ["[\w|\s]*\n", 
							pexpect.EOF]

		still_reading = True
		while still_reading:
			result = child.expect(expected_lines)

			if result == 0:
				print child.before
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()

	def make(self):
		child = pexpect.spawn('bash -c "make"', timeout=60)
		expected_lines = ["[\w|\s]*\n", 
							pexpect.EOF]

		still_reading = True
		while still_reading:
			result = child.expect(expected_lines)

			if result == 0:
				print child.before
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()

	def make_messages(self):
		run_as_user("make messages")

	def make_install(self):
		run_as_root("make install")

	def python_setup_install(self, flags=''):
		run_as_root("python setup.py install --record=install-files.txt " + flags)

	def python_unpack_eggs(self, egg_directory):
		curdir = os.getcwd()
		os.chdir(egg_directory)
		for entry in os.listdir('.'):
			if not entry.endswith('.egg'): continue

			print "Unpacking python egg: " + entry
			name = entry.split('-')[0]
			version = entry.split('-')[1]
			run_as_root("unzip -q '" + entry + "'")
			run_as_root("mv 'EGG-INFO' '" + name + "-" + version + ".egg-info'")
			run_as_root("rm '" + entry + "'")
		os.chdir(curdir)

	def to_hash(self):
		retval={ 'authors' : self.authors, 
				'after_install' : self.after_install(), 
				'after_uninstall' : self.after_uninstall(), 
				'before_install' : self.before_install(), 
				'before_uninstall' : self.before_uninstall(), 
				'build_requirements' : self.build_requirements, 
				'category' : self.category, 
				'build_method' : self.build_method, 
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
				'source_file' : self.source_file, 
				'version' : self.version, 
				}

		# Make changes that make data easier to use
		retval['year'] = time.strftime("%Y", time.localtime())
		retval['timestring'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
		retval['human_timestring'] = time.strftime("%a %b %d %Y", time.localtime())

		return retval

class BinaryPackage(object):
	def __init__(self):
		self._name = None
		self._alternate_name = None
		self._priority = None
		self._category = None
		self._package_type = None
		self._install_requirements = []
		self._files = []
		self._additional_description = u""
		self._custom = {}

	def get_name(self): return self._name
	name = property(get_name)

	def get_alternate_name(self): return self._alternate_name
	alternate_name = property(get_alternate_name)

	def get_priority(self): return self._priority
	priority = property(get_priority)

	def get_category(self): return self._category
	category = property(get_category)

	def get_package_type(self): return self._package_type
	package_type = property(get_package_type)

	def get_install_requirements(self): return self._install_requirements
	install_requirements = property(get_install_requirements)

	def get_files(self): return self._files
	files = property(get_files)

	def get_additional_description(self): return self._additional_description
	additional_description = property(get_additional_description)

	def get_custom(self): return self._custom
	custom = property(get_custom)

	def to_hash(self):
		retval={'additional_description' : self.additional_description, 
				'alternate_name' : self.alternate_name, 
				'category' : self.category, 
				'package_type' : self.package_type, 
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

user_gid, user_uid = None, None
def setup_user_ids(normal_user_uid):
	global user_gid
	global user_uid

	user_gid = normal_user_uid
	user_uid = normal_user_uid

	raise_privileges()
	lower_privileges()

def is_root():
	return os.getegid() == 0 and os.geteuid() == 0

def raise_privileges():
	if is_root():
		return

	os.setegid(0)
	os.seteuid(0)

def lower_privileges():
	global user_gid
	global user_uid

	if not is_root():
		return

	os.setegid(user_gid)
	os.seteuid(user_uid)

def run_as_root(command):
	raise_privileges()

	print command
	child = pexpect.spawn('bash -c "' + command + '"', timeout=60)
	expected_lines = ["[\w|\s]*\n", 
							pexpect.EOF]

	still_reading = True
	while still_reading:
		result = child.expect(expected_lines)

		if result == 0:
			print child.before
		elif result == len(expected_lines)-1:
			still_reading = False

	child.close()

	lower_privileges()

def run_as_user(command):
	print command
	return commands.getoutput(command)

def download_file(file_url, file_name):
	opener1 = urllib2.build_opener()
	page1 = opener1.open(file_url)
	file_chunk = None
	file_length = int(page1.headers['Content-Length'])
	file_chunk_length = 0
	out_file = open(file_name, 'wb')
	prev_output_length = 0

	while True:
		file_chunk = page1.read(1024)
		if len(file_chunk) == 0: break
		file_chunk_length += len(file_chunk)
		out_file.write(file_chunk)

		percent = 100.0 * (float(file_chunk_length) / float(file_length))
		output = ('Downloading source code: ' + str(percent) + ' %').ljust(50)
		sys.stdout.write("\b" * prev_output_length + output)
		sys.stdout.flush()
		prev_output_length = len(output)

	out_file.close()
	sys.stdout.write("\n")

packagetastic_dir = None
def init_packagetastic(distro_name):
	# Make sure we are on linux
	if platform.system() != 'Linux':
		print "Packagetastic only works on Linux, not '" + platform.system() + "'. Exiting ..."
		exit()

	# Try to get the OS name
	os_name = None
	if run_as_user('whereis lsb_release').split(':')[1] != '':
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
	if not os.path.isfile("sources/" + meta.source_file):
		print substitute_strings("Missing source code at: sources/#{source_file}. Exiting ...", meta.to_hash())
		exit()

	# Convert any .tar.bz2 files to .tar.gz
	source_file = meta.source_file
	if meta.source_file.endswith('.tar.bz2'):
		os.chdir('sources')
		dir_name = meta.source_file.rstrip('.tar.bz2')
		print "Converting bzip source code to gzip ..."
		run_as_user("tar xjf " + meta.source_file)
		run_as_user(substitute_strings("mv " + dir_name + " #{name}-#{version}", meta.to_hash()))
		run_as_user(substitute_strings("tar -czf #{name}-#{version}.tar.gz #{name}-#{version}", meta.to_hash()))
		run_as_user(substitute_strings("rm -rf #{name}-#{version}", meta.to_hash()))
		source_file = substitute_strings("#{name}-#{version}.tar.gz", meta.to_hash())
		os.chdir('..')

	# Uncompress the source code
	print "Uncompressing source code ..."
	if os.path.isdir("builds"):
		run_as_root("rm -rf builds")
	os.mkdir("builds")
	run_as_user("cp sources/" + source_file + " builds/" + source_file)
	os.chdir("builds")
	run_as_user("tar xzf " + source_file)
	run_as_user("rm " + source_file)
	if len(os.listdir(".")) == 0:
		print "Failed to uncompress the source code. Exiting ..."
		exit()
	actual_file = os.listdir(".")[0]
	if actual_file != substitute_strings("#{name}-#{version}", meta.to_hash()):
		run_as_user(substitute_strings("mv " + actual_file + " #{name}-#{version}", meta.to_hash()))
	os.chdir(substitute_strings("#{name}-#{version}", meta.to_hash()))

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
	params['has_lang'] = (os.path.isdir('po') or os.path.isdir('locale'))
	params['has_desktop_file'] = False
	params['desktop_file_name'] = None

	# Find out which build methods are used
	params['builds_with_autotools'] = \
		os.path.isfile('Makefile.in') or os.path.isfile('GNUmakefile')
	params['builds_with_python'] = os.path.isfile('setup.py')

	if meta.build_method.count('python') > 0 and params['builds_with_python']:
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
			if entry.endswith('.desktop') or entry.endswith('.desktop.in'):
				params['has_desktop_file'] = True
				params['desktop_file_name'] = entry[len('/usr/share/'):]
		elif entry.startswith('/usr/share/mime/'):
			params['has_mime'] = True
		elif entry.startswith('/usr/share/omf/'):
			params['has_omf'] = True

def requirements_to_distro_specific(distro_name, requirements):
	distro_requirements = []
	for requirement in requirements:
		name, compare, version = None, None, None
		r = requirement.split()
		if len(r) >= 1: name = r[0]
		if len(r) >= 2: compare = r[1]
		if len(r) >= 3: version = r[2]

		for new_name in package_names[name][distro_name]:
			distro_requirements.append({'name' : new_name, 
										'compare' : compare, 
										'version' : version})


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

def validate_package(distro_name, meta, packages):
	# Make sure meta and packages were loaded
	if not meta:
		print "No MetaPackage class was found in the stem file. Exiting ..."
		exit()
	if len(packages) == 0:
		print "No BinaryPackage classes were found in the stem file. Exiting ..."
		exit()

	# Make sure unicode is used for the correct fields
	for author in meta.authors:
		if not isinstance(author, unicode):
			print "Stem file is Broken. The meta authors field \"" + author + "\" is not unicode. Exiting ..."
			exit()

	for copyright in meta.copyright:
		if not isinstance(copyright, unicode):
			print "Stem file is Broken. The meta copyright field \"" + copyright + "\" is not unicode. Exiting ..."
			exit()

	if not isinstance(meta.short_description, unicode):
		print "Stem file is Broken. The meta short_description field \"" + meta.short_description + "\" is not unicode. Exiting ..."
		exit()

	if not isinstance(meta.long_description, unicode):
		print "Stem file is Broken. The meta long_description field \"" + meta.long_description + "\" is not unicode. Exiting ..."
		exit()

	for package in packages:
		if not isinstance(package.additional_description, unicode):
			print "Stem file is Broken. The package additional_description field \"" + package.additional_description + "\" is not unicode. Exiting ..."
			exit()

	for entry in meta.changelog:
		if not isinstance(entry.text, unicode):
			print "Stem file is Broken. The meta changelog's text field for \"version:" + entry.version + ' -- time:' + entry.time + "\" is not unicode. Exiting ..."
			exit()

	# Make sure the fields are valid
	if meta.name is None or meta.name == "":
		print "Stem file is Broken. The meta name is blank or null. Exiting ..."
		exit()

	if packagetastic_categories.count(meta.category) == 0:
		print "Stem file is Broken. The meta category field of \"" + str(meta.category) + "\" in unknown. Exiting ..."
		exit()

	if packagetastic_build_methods.count(meta.build_method) == 0:
		print "Stem file is Broken. The meta build method field of \"" + str(meta.build_method) + "\" in unknown. Exiting ..."
		exit()

	if meta.priority is None or meta.priority == "":
		print "Stem file is Broken. The meta priority is blank or null. Exiting ..."
		exit()

	if len(meta.authors) == 0:
		print "Stem file is Broken. The meta authors list must have at least one entry. Exiting ..."
		exit()

	if len(meta.copyright) == 0:
		print "Stem file is Broken. The meta copyright list must have at least one entry. Exiting ..."
		exit()

	if meta.homepage is None or meta.homepage == "":
		print "Stem file is Broken. The meta homepage is blank or null. Exiting ..."
		exit()

	if ['AGPL3+', 'GPL2+', 'GPL3+', 'LGPL2.1', 'MIT', 'BSD-C3'].count(meta.license) == 0:
		print "Stem file is Broken. The meta license field of \"" + str(meta.license) + "\" in unknown. Exiting ..."
		exit()

	if meta.source is None or meta.source == "":
		print "Stem file is Broken. The meta source is blank or null. Exiting ..."
		exit()

	if meta.short_description is None or meta.short_description == "":
		print "Stem file is Broken. The meta short_description is blank or null. Exiting ..."
		exit()

	if meta.long_description is None or meta.long_description == "":
		print "Stem file is Broken. The meta long_description is blank or null. Exiting ..."
		exit()

	if len(meta.changelog) == 0:
		print "Stem file is Broken. The meta changelog list must have at least one entry. Exiting ..."
		exit()

	for entry in meta.changelog:
		if entry.version is None or entry.version == "":
			print "Stem file is Broken. The meta changelog's version field is blank or null. Exiting ..."
			exit()
		elif entry.time is None or entry.time == "":
			print "Stem file is Broken. The meta changelog's time field is blank or null. Exiting ..."
			exit()
		elif entry.text is None or entry.text == "":
			print "Stem file is Broken. The meta changelog's text field is blank or null. Exiting ..."
			exit()

	for package in packages:
		if package.name is None or package.name == "":
			print "Stem file is Broken. The package name is blank or null. Exiting ..."
			exit()
		elif packagetastic_categories.count(package.category) == 0:
			print "Stem file is Broken. The package category field of \"" + str(package.category) + "\" in unknown. Exiting ..."
			exit()
		elif packagetastic_package_types.count(package.package_type) == 0:
			print "Stem file is Broken. The package type field of \"" + str(package.package_type) + "\" in unknown. Exiting ..."
			exit()
		elif package.priority is None or package.priority == "":
			print "Stem file is Broken. The package priority is blank or null. Exiting ..."
			exit()


	# Make sure we know about the name
	package_names = globals()['package_names']
	for package in packages:
		if not package_names.has_key(package.name):
			print "The package name \"" + package.name + "\" was not found. Please add it to package_names.py. Exiting ..."
			exit()

	# Make sure we know about the build requirements
	for build_requirement in meta.build_requirements:
		requirement = build_requirement.split()[0]

		if not package_names.has_key(requirement):
			print "Stem file is Broken. The build requirement \"" + requirement + "\" was not found. Please add it to package_names.py. Exiting ..."
			exit()
		elif package_names[requirement].has_key(distro_name) and \
			len(package_names[requirement][distro_name]) == 0:
			print "Stem file is Broken. The build requirement \"" + requirement + "\" is missing for this distro. Please add it to package_names.py. Exiting ..."
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

def _get_packager_data():
	global packagetastic_dir
	os.chdir(packagetastic_dir)

	# Make sure the packager_name file exists
	if not os.path.isfile('packager_name'):
		print "Add the packager name to the 'packager_name' file."
		exit()

	# Make sure the packager_email file exists
	if not os.path.isfile('packager_email'):
		print "Add the packager email address to the 'packager_email' file."
		exit()

	f = open('packager_name')
	packager_name = f.read()[0:-1]
	f.close()

	f = open('packager_email')
	packager_email = f.read()[0:-1]
	f.close()

	return (packager_name, packager_email)

def _get_package_data(distro_name, package_name, packager_name, packager_email):
	# Find any junk MetaPackage and BinaryPackage already in memory
	junk_objects = []
	for obj in gc.get_objects():
		if type(obj) == type and (issubclass(obj, MetaPackage) or issubclass(obj, BinaryPackage)):
			junk_objects.append(obj)

	# Load the distro and stem files
	execfile('distros/' + distro_name + '.py')
	execfile('stems/' + package_name + '.stem')

	# Get the package meta data
	meta = None
	for obj in gc.get_objects():
		if type(obj) == type and issubclass(obj, MetaPackage) and obj().name == package_name:
			if junk_objects.count(obj) == 0:
				meta = obj()
				break

	# Get the packages that are loaded
	packages = []
	for obj in gc.get_objects():
		if type(obj) == type and obj != BinaryPackage and issubclass(obj, BinaryPackage):
			if junk_objects.count(obj) == 0:
				package = obj()
				packages.append(package)

	# Validate the meta and packages
	validate_package(distro_name, meta, packages)

	meta.packager_name = packager_name
	meta.packager_email = packager_email
	builder = eval('Builder()')

	return (meta, packages, builder)

def build(distro_name, package_name):
	packager_name, packager_email = _get_packager_data()

	# Make sure we have a distro file that matches the name
	if not os.path.isfile('distros/' + distro_name + '.py'):
		print "Packagetastic does not know how to build for the distro '" + distro_name + "'. Exiting ..."
		exit()

	# Make sure we have a stem file that matches the name
	if not os.path.isfile('stems/' + package_name + '.stem'):
		print "Packagetastic does not have a stem file for the package '" + package_name + "'. Exiting ..."
		exit()

	# Create the package directories
	home = os.path.expanduser('~')
	if not os.path.isdir(home + '/.packagetastic'):
		os.mkdir(home + '/.packagetastic')
	if not os.path.isdir(home + '/.packagetastic/' + package_name):
		os.mkdir(home + '/.packagetastic/' + package_name)
	run_as_user('cp stems/' + package_name + '.stem ' + home + '/.packagetastic/' +  package_name + '/' + package_name + '.stem')

	meta, packages, builder = _get_package_data(distro_name, package_name, packager_name, packager_email)

	# Download the source code
	try:
		if not os.path.isdir('sources'):
			os.mkdir('sources')
		if not os.path.isfile('sources/' + meta.source_file):
			download_file(meta.source, 'sources/' + meta.source_file)
	except urllib2.HTTPError:
		print "HTTPError: Failed to download the source code. Exiting ..."
		exit()
	except urllib2.URLError:
		print "URLError: Failed to download the source code. Exiting ..."
		exit()

	# Convert the requirements to be distro specific
	meta.__dict__['_build_requirements'] = \
		requirements_to_distro_specific(distro_name, meta.build_requirements)
	for package in packages:
		package.__dict__['_install_requirements'] = \
			requirements_to_distro_specific(distro_name, package.install_requirements)

	# Build the package for that distro
	print "\nBuilding " + package_name + " ..."
	builder.build(meta, packages)

def install(distro_name, package_name):
	packager_name, packager_email = _get_packager_data()

	meta, packages, builder = _get_package_data(distro_name, package_name, packager_name, packager_email)

	# Convert the requirements to be distro specific
	meta.__dict__['_build_requirements'] = \
		requirements_to_distro_specific(distro_name, meta.build_requirements)
	for package in packages:
		package.__dict__['_install_requirements'] = \
			requirements_to_distro_specific(distro_name, package.install_requirements)

	# Install the package for that distro
	print "\nInstalling " + package_name + " ..."
	builder.install(meta, packages)

