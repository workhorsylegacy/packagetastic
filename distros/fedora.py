


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

	def build(self, meta, packages, root_password, gpg_password):
		# Setup the directories
		print "Setting up the rpmdev directories ..."
		commands.getoutput('rm -rf ~/rpmbuild')
		commands.getoutput('rpmdev-setuptree')

		setup_source_code(meta)

		# Copy the source code to the build tree
		print "Copying the source code ..."
		commands.getoutput(substitute_strings("cp ../../sources/" + meta.source.split('/')[-1] + " ~/rpmbuild/SOURCES/" + meta.source.split('/')[-1], meta.to_hash()))

		# FIXME: Figure out how %defattr(-,root,root,-) works
		# Determine the params for %files
		params = meta.to_hash()
		params['docs'] = []
		for doc in ['README', 'COPYING', 'ChangeLog', 'LICENSE']:
			if os.path.isfile(doc):
				params['docs'].append(doc)

		for doc in ['doc', 'examples']:
			if os.path.isdir(doc):
				params['docs'].append(doc)

		if os.path.isfile('doc/' + meta.name + '.1'):
			params['has_man1'] = True
		elif os.path.isfile('man/' + meta.name + '.1'):
			params['has_man1'] = True
		else:
			params['has_man1'] = False

		if os.path.isfile('doc/' + meta.name + '_config.5'):
			params['has_man5'] = True
		elif os.path.isfile('man/' + meta.name + '_config.5'):
			params['has_man5'] = True
		else:
			params['has_man5'] = False

		params['has_bindir'] = False
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			params['has_bindir'] = True
			params['import_sitelib'] = False
		elif meta.build_method == 'python library':
			params['has_bindir'] = False
			params['import_sitelib'] = True
		elif meta.build_method == 'python application':
			params['has_bindir'] = True
			params['import_sitelib'] = True

		params['has_info'] = os.path.isfile('doc/' + meta.name + '.info')

		params['has_lang'] = os.path.isdir('po')

		params['has_desktop_file'] = os.path.isfile('data/' + meta.name + '.desktop')

		params['has_icons'] = os.path.isdir('data/icons')

		params['group'] = self.category_to_group[meta.category]

		if meta.build_method == 'c application' or meta.build_method == 'c library':
			params['install_requirements'] = packages[0].install_requirements
		elif meta.build_method == 'python application' or meta.build_method == 'python library':
			params['install_requirements'] = packages[0].install_requirements + ['python']
		else:
			print "Unknown build method '" + meta.build_method + "'. Exiting ..."
			exit()

		params['join_method'] = meta.join


		# Create the spec file
		os.chdir('../..')
		print "Building the spec file ..."
		# Write the custom parts of the spec file
		with open('distros/fedora_templates/template.spec.py') as f:
			from mako.template import Template
			template = Template(f.read())
			with open(os.path.expanduser('~/rpmbuild/SPECS/') + meta.name + '.spec', 'w') as spec_file:
				spec_file.write(template.render(**params).replace("@@", "%"))

		# Create the rpm file
		packagetastic_dir = commands.getoutput('pwd')
		os.chdir(os.path.expanduser("~"))

		print "Building the rpm package ..."
		command = "rpmbuild -ba rpmbuild/SPECS/" + meta.name + ".spec"
		print commands.getoutput(command)
		"""
		child = pexpect.spawn(command, timeout=1200)

		expected_lines = ["error: Failed build dependencies:\r\n" +
							"[\W]*[\w|\d|\.|\-]* is needed by [\w|\d|\.|\-]*fc[\d]*.src", 

							"error: File /home/[\w|\d|\_]*/rpmbuild/SOURCES/" + 
							meta.name + "-" + meta.version + ".tar.gz:" + 
							" No such file or directory", 

							pexpect.EOF]

		still_reading = True
		while still_reading:
			result = child.expect(expected_lines)
			#print "[[[" + str(child.before) + "]]]"
			#print "[[[" + str(child.after) + "]]]"

			if result == 0:
				print child.after
			elif result == 1:
				print child.after
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()
		"""

		print "Copying the rpm package to the packages directory ..."
		os.chdir(packagetastic_dir)
		if not os.path.isdir("packages"): os.mkdir("packages")
		rpm = meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11." + meta.build_arch + ".rpm"
		commands.getoutput("cp ~/rpmbuild/RPMS/" + meta.build_arch + "/" + rpm + " packages/" + rpm)
		print "Done"




