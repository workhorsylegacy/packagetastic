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

	package_type_to_architecture = {
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
		if value.count('>') > 0 or value.count('<') > 0 or value.count('>=') > 0 or value.count('<=') > 0:
			value = value.replace('(', '').replace(')', '')
		return value.split(' | ')[0]

	def expand_macro(self, string):
		macro_map = { "%{distro_id}" : commands.getoutput("lsb_release -ds").replace('"', '') }

		for key, value in macro_map.iteritems():
			string = string.replace(key, value)

		return string

	def build(self, meta, packages, packager_sudo, packager_gpg, use_chroot, is_interactive):
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
		params['package_type_to_architecture'] = self.package_type_to_architecture
		params['filter_requirement'] = self.filter_requirement

		# Get the file structure of the package
		print "Determining package file structure ..."
		get_file_structure_for_package(meta, packages, params)

		# Add additional install requirements based on our source code interrogation
		params['additional_install_requirements'] = []
		if params['builds_with_python']:
			params['additional_install_requirements'] += ['python']
			params['build_requirements'] += ['python-devel']
		if params['has_desktop_file'] and meta.build_requirements.count('desktop-file-utils') == 0:
			params['build_requirements'] += ['desktop-file-utils']

		# Add the configure-make-install params
		meta.build()
		params['configure_params'] = self.expand_macro(meta.params_for_configure)
		params['make_params'] = self.expand_macro(meta.params_for_make)
		params['install_params'] = self.expand_macro(meta.params_for_install)

		# Create the spec file
		os.chdir('../..')
		print "Generating the spec file ..."
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
		command = ""
		if use_chroot:
			command = "rpmbuild -bs rpmbuild/SPECS/" + meta.name + ".spec"
		else:
			command = "rpmbuild -ba rpmbuild/SPECS/" + meta.name + ".spec"

		if is_interactive:
			print commands.getoutput(command)
		else:
			child = pexpect.spawn(command, timeout=1200)

			expected_lines = [
			"error: Installed \(but unpackaged\) file\(s\) found:\r\n[\w|\W|\s]*\r\n\r\n", 

			"	[\w|\W]* is needed by [\w|\d|\s|\>|\<|\=|\_|\-|\.|\/|\ ]*\r\n", 

			"    File not found\: [\w|\d|\_|\-|\.|\/|\ ]*\r\n", 

			pexpect.EOF]

			still_reading = True
			had_error = False
			while still_reading:
				result = child.expect(expected_lines)
				#print "[[[" + str(child.before) + "]]]"
				#print "[[[" + str(child.after) + "]]]"

				if result == 0:
					had_error = True
					print "Files were found in the built package that were not expected:"
					for line in child.after.strip().split("\r\n")[1:]:
						line = line.strip()
						print "\t" + line
				elif result == 1:
					package_name = child.after.split(' is needed by ')[0].strip()
					print "Build requirement not installed '" + package_name + "'."
					had_error = True
				elif result == 2:
					file_name = child.after.split('File not found: ')[1].strip()
					print "File not found: '" + file_name + "'."
					had_error = True
				elif result == len(expected_lines)-1:
					still_reading = False

			child.close()
			if had_error:
				print "Exiting ..."
				exit()

		if use_chroot:
			print "Running mock ..."
			os.chdir("rpmbuild/SRPMS/")
			command = "mock -r fedora-11-i386 --verbose --rebuild " + meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11.src.rpm"
			if is_interactive:
				print commands.getoutput(command)
			else:
				child = pexpect.spawn(command, timeout=1200)

				expected_lines = [
				"ERROR: Bad build req: No Package Found for [\w|\-|\<|\>|\=|\.|\s]*. Exiting.", 

				"DEBUG:     File not found: [\w|\d|\_|\-|\.|\/|\ ]*\r\n", 

				"DEBUG: \/usr\/bin\/python: can't open file \'setup.py\': \[Errno 2\] No such file or directory", 

				"DEBUG: No package \'[\w|\d|\s|\>|\<|\=|\_|\-|\.|\/]*\' found\r\n", 

				pexpect.EOF]

				still_reading = True
				had_error = False
				while still_reading:
					result = child.expect(expected_lines)
					#print "[[[" + str(child.before) + "]]]"
					#print "[[[" + str(child.after) + "]]]"

					if result == 0:
						package_name = child.after.split('ERROR: Bad build req: No Package Found for ')[1].split('. Exiting.')[0]
						print "Build requirement not found in the repository '" + package_name + "'."
						had_error = True
					elif result == 1:
						file_name = child.after.split("DEBUG:     File not found: ")[1].split()[0]
						print "File not found '" + file_name + "'. Exiting ..."
						had_error = True
					elif result == 2:
						print "No python setup.py file found. Exiting ..."
						exit()
					elif result == 3:
						package_name = child.after.split("DEBUG: No package '")[1].split("' found\r\n")[0]
						print "Requirement needed, but not listed in build requirements '" + package_name + "'."
						had_error = True
					elif result == len(expected_lines)-1:
						still_reading = False

				child.close()
				if had_error:
					print "Exiting ..."
					exit()

		print "Getting the rpm files ..."
		os.chdir(packagetastic_dir)
		if not os.path.isdir("packages"): os.mkdir("packages")
		for package in packages:
			architecture = self.package_type_to_architecture[package.package_type]
			rpm = meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11." + architecture + ".rpm"
			if use_chroot:
				print commands.getoutput("cp /var/lib/mock/fedora-11-i386/result/" + rpm + " packages/" + rpm)
			else:
				print commands.getoutput("cp ~/rpmbuild/RPMS/" + architecture + "/" + rpm + " packages/" + rpm)
		print "Done"




