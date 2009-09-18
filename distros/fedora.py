#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class Builder(object):
	# In Fedora, the lists of groups can be found with:
	# less /usr/share/doc/rpm-*/GROUPS
	# http://fedoraproject.org/wiki/PackageMaintainers/CreatingPackageHowTo#Spec_file_pieces_explained
	category_to_group = {
		'Applications/Audio' : 'Applications/Multimedia', 
		'Applications/Archiving' : 'Applications/Archiving', 
		'Applications/Communications' : 'Applications/Communications', 
		'Applications/Databases' : 'Applications/Databases', 
		'Applications/Editors' : 'Applications/Editors', 
		'Applications/Emulators' : 'Applications/Emulators', 
		'Applications/Engineering' : 'Applications/Engineering', 
		'Applications/File' : 'Applications/File', 
		'Applications/Games' : 'Amusements/Games', 
		'Applications/Graphics' : 'Applications/Multimedia', 
		'Applications/HamRadio' : 'Applications/Engineering', 
		'Applications/Internet' : 'Applications/Internet', 
		'Applications/Multimedia' : 'Applications/Multimedia', 
		'Applications/Office' : 'Applications/Productivity', 
		'Applications/Publishing' : 'Applications/Publishing', 
		'Applications/System' : 'Applications/System', 
		'Applications/Text' : 'Applications/Text', 
		'Applications/Video' : 'Applications/Multimedia', 
		'Applications/Virtualization' : 'Applications/System', 
		'Development/Debuggers' : 'Development/Debuggers', 
		'Development/Languages' : 'Development/Languages', 
		'Development/Libraries' : 'Development/Libraries', 
		'Development/System' : 'Development/System', 
		'Development/Tools' : 'Development/Tools', 
		'Development/VersionControlSystems' : 'Development/Tools', 
		'Documentation' : 'Documentation', 
		'Localization' : 'Applications/Text', 
		'System/Base' : 'System Environment/Base', 
		'System/Daemons' : 'System Environment/Daemons', 
		'System/Databases' : 'System Environment/Daemons', 
		'System/Desktops' : 'User Interface/Desktops', 
		'System/Drivers' : 'User Interface/X Hardware Support', 
		'System/FileSystems' : 'System Environment/Base', 
		'System/Fonts' : 'User Interface/X', 
		'System/Kernel' : 'System Environment/Kernel', 
		'System/Libraries' : 'System Environment/Libraries', 
		'System/Shells' : 'System Environment/Shells', 
		'System/Virtualization' : 'System Environment/Daemons', 
		'System/WebServers' : 'System Environment/Daemons'
	}

	build_method_to_build_arch = {
		'c application' : 'i586', 
		'c library' : 'i586', 
		'mono application' : 'i586', 
		'mono library' : 'i586', 
		'python application' : 'noarch', 
		'python library' : 'noarch', 
		'documentation' : 'noarch'
	}

	# FIXME: Figure out how to do "one or two or three"
	def filter_requirement(self, value):
		return value.replace('(', '').replace(')', '').split(' | ')[0]

	def build(self, meta, packages, packager_sudo, packager_gpg):
		# Setup the directories
		print "Setting up the rpmdev directories ..."
		commands.getoutput('rm -rf ~/rpmbuild')
		commands.getoutput('rpmdev-setuptree')

		setup_source_code(meta)

		# Copy the source code to the build tree
		print "Copying the source code ..."
		commands.getoutput(substitute_strings("cp ../../sources/" + meta.source.split('/')[-1] + " ~/rpmbuild/SOURCES/" + meta.source.split('/')[-1], meta.to_hash()))

		# Copy any patches to the build tree
		for patch in meta.patches:
			commands.getoutput("cp ../../patches/" + meta.name + "/" + patch + " ~/rpmbuild/SOURCES/" + patch)

		params = meta.to_hash()
		params['packages'] = packages
		params['category_to_group'] = self.category_to_group
		params['build_method_to_build_arch'] = self.build_method_to_build_arch
		params['filter_requirement'] = self.filter_requirement

		# Find an internal name that is a variation of the meta.name
		params['internal_name'] = meta.name
		pwd = commands.getoutput('pwd')
		for entry in os.listdir(pwd):
			if os.path.isdir(pwd + '/' + entry):
				if entry.lower().replace('-', '').replace('_', '') == meta.name.lower().replace('-', '').replace('_', ''):
					params['internal_name'] = entry

		# Find out which languages are used
		for lang in ['c', 'python', 'mono']:
			params['uses_' + lang] = False
			for package in packages:
				if package.build_method == lang + ' application' or package.build_method == lang + ' library':
					params['uses_' + lang] = True

		# FIXME: Figure out how %defattr(-,root,root,-) works
		# Get the docs and example params
		params['docs'] = []
		for doc in ['README', 'COPYING', 'ChangeLog', 'LICENSE', 'AUTHORS']:
			if os.path.isfile(doc):
				params['docs'].append(doc)
		for doc in ['doc', 'examples']:
			if os.path.isdir(doc):
				params['docs'].append(doc)
		params['docs'].sort()

		# Get the man1 params
		if os.path.isfile('doc/' + params['internal_name'] + '.1'):
			params['has_man1'] = True
		elif os.path.isfile('man/' + params['internal_name'] + '.1'):
			params['has_man1'] = True
		elif os.path.isfile('src/' + params['internal_name'] + '.1'):
			params['has_man1'] = True
		else:
			params['has_man1'] = False

		# Get the man5 params
		if os.path.isfile('doc/' + params['internal_name'] + '_config.5'):
			params['has_man5'] = True
		elif os.path.isfile('man/' + params['internal_name'] + '_config.5'):
			params['has_man5'] = True
		else:
			params['has_man5'] = False

		# Get the icons
		params['has_icon_pngs'] = False
		params['has_icon_svgs'] = False
		if os.path.isdir('data/icons') or os.path.isdir('icons'):
			params['has_icon_pngs'] = True
		if os.path.isdir('data/icons/scalable') or os.path.isdir('icons/scalable'):
			params['has_icon_svgs'] = True

		# Get the desktop file
		params['has_desktop_file'] = False
		if os.path.isfile('data/' + params['internal_name'] + '.desktop'):
			params['has_desktop_file'] = True
			params['desktop_file'] = 'data/' + params['internal_name'] + '.desktop'
		elif os.path.isfile('ui/' + params['internal_name'] + '.desktop'):
			params['has_desktop_file'] = True
			params['desktop_file'] = 'ui/' + params['internal_name'] + '.desktop'
		elif os.path.isfile('bin/' + params['internal_name'] + '.desktop'):
			params['has_desktop_file'] = True
			params['desktop_file'] = 'bin/' + params['internal_name'] + '.desktop'

		# Get more params
		params['has_info'] = os.path.isfile('doc/' + params['internal_name'] + '.info')
		params['has_lang'] = os.path.isdir('po')
		params['has_datadir'] = os.path.isdir(params['internal_name'])

		# Get the build params
		params['has_bindir'] = False
		params['import_python_sitelib'] = False
		for package in packages:
			if package.build_method == 'c application' or package.build_method == 'c library':
				params['has_bindir'] = True
			elif package.build_method == 'python library':
				params['import_python_sitelib'] = True
			elif package.build_method == 'python application':
				params['has_bindir'] = True
				params['import_python_sitelib'] = True

		# Add additional install requirements based on our source code interrogation
		params['additional_install_requirements'] = []
		if params['uses_python']:
			params['additional_install_requirements'] += ['python']
			params['build_requirements'] += ['python-devel']
		if params['has_desktop_file'] and meta.build_requirements.count('desktop-file-utils') == 0:
			params['build_requirements'] += ['desktop-file-utils']


		# Create the spec file
		os.chdir('../..')
		print "Building the spec file ..."
		with open(os.path.expanduser('~/rpmbuild/SPECS/') + meta.name + '.spec', 'w') as spec_file:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['distros/fedora_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.spec.py")
			spec_file.write(template.render(**params).replace("@@", "%").replace("\\\\\\", "\\\n"))

		# Create the rpm file
		packagetastic_dir = commands.getoutput('pwd')
		os.chdir(os.path.expanduser("~"))

		print "Running rpmbuild ..."
		command = "rpmbuild -bs rpmbuild/SPECS/" + meta.name + ".spec"
		#print commands.getoutput(command)
		#"""
		child = pexpect.spawn(command, timeout=1200)

		expected_lines = [pexpect.EOF]

		still_reading = True
		while still_reading:
			result = child.expect(expected_lines)
			#print "[[[" + str(child.before) + "]]]"
			#print "[[[" + str(child.after) + "]]]"

			if result == len(expected_lines)-1:
				still_reading = False

		child.close()
		#"""

		print "Running mock ..."
		os.chdir("rpmbuild/SRPMS/")
		command = "mock -r fedora-11-i386 --verbose --rebuild " + meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11.src.rpm"
		#print commands.getoutput(command)
		#"""
		child = pexpect.spawn(command, timeout=1200)

		expected_lines = [
		"ERROR: Bad build req: No Package Found for [\w|\-]*. Exiting.", 

		"DEBUG:     File not found: [\w|\d|\_|\-|\.|\/|\ ]*\r\n", 

		"DEBUG: error: File not found: [\w|\d|\_|\-|\.|\/|\ ]*\r\n", 

		"DEBUG: No Package Found for [\w|\d|\s|\>|\<|\=|\_|\-|\.|\/|\ ]*\r\n", 

		"DEBUG: \/usr\/bin\/python: can't open file \'setup.py\': \[Errno 2\] No such file or directory", 

		pexpect.EOF]

		still_reading = True
		had_error = False
		while still_reading:
			result = child.expect(expected_lines)
			#print "[[[" + str(child.before) + "]]]"
			#print "[[[" + str(child.after) + "]]]"

			if result == 0:
				package_name = child.after.split('ERROR: Bad build req: No Package Found for ')[1].split('. Exiting.')[0]
				print "Unknown build requirement '" + package_name + "'."
				had_error = True
			elif result == 1:
				file_name = child.after.split("DEBUG:     File not found: ")[1].split()[0]
				print "File not found '" + file_name + "'. Exiting ..."
				exit()
			elif result == 2:
				file_name = child.after.split("DEBUG: error: File not found: ")[1].split()[0]
				print "File not found '" + file_name + "'. Exiting ..."
				exit()
			elif result == 3:
				file_name = child.after.split("DEBUG: No Package Found for ")[1].split()[0]
				print "Unknown build requirement '" + file_name + "'."
				had_error = True
			elif result == 4:
				print "No python setup.py file found. Exiting ..."
				exit()
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()
		if had_error:
			print "Exiting ..."
			exit()
		#"""

		print "Copying the rpm package to the packages directory ..."
		os.chdir(packagetastic_dir)
		if not os.path.isdir("packages"): os.mkdir("packages")
		for package in packages:
			build_arch = self.build_method_to_build_arch[package.build_method]
			rpm = meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11." + build_arch + ".rpm"
			print commands.getoutput("cp /var/lib/mock/fedora-11-i386/result/" + rpm + " packages/" + rpm)
		print "Done"




