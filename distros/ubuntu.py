#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class Builder(object):
	# http://www.debian.org/doc/debian-policy/ch-archive.html#s-subsections
	category_to_section = {
		'Applications/Archiving' : 'Applications/Archiving', 
		'Applications/Audio' : 'sound', 
		'Applications/Communications' : 'comm', 
		'Applications/Databases' : 'database', 
		'Applications/Editors' : 'editors', 
		'Applications/Emulators' : 'misc', 
		'Applications/Engineering' : 'science', 
		'Applications/File' : 'editors', 
		'Applications/Games' : 'games', 
		'Applications/Graphics' : 'graphics', 
		'Applications/HamRadio' : 'hamradio', 
		'Applications/Internet' : 'web', 
		'Applications/Office' : 'editors', 
		'Applications/Publishing' : 'editors', 
		'Applications/System' : 'admin', 
		'Applications/Text' : 'text', 
		'Applications/Video' : 'video', 
		'Applications/Virtualization' : 'misc', 
		'Development/Debuggers' : 'debug', 
		'Development/Languages' : 'devel', 
		'Development/Libraries' : 'libdevel', 
		'Development/System' : 'devel', 
		'Development/Tools' : 'devel', 
		'Development/VersionControlSystems' : 'vcs', 
		'Documentation' : 'doc', 
		'Localization' : 'localization', 
		'System/Base' : 'misc', 
		'System/Daemons' : 'misc', 
		'System/Databases' : 'database', 
		'System/Desktops' : 'misc', 
		'System/Drivers' : 'misc', 
		'System/FileSystems' : 'misc', 
		'System/Fonts' : 'misc', 
		'System/Kernel' : 'kernel', 
		'System/Libraries' : 'libs', 
		'System/Shells' : 'shells', 
		'System/Virtualization' : 'misc', 
		'System/WebServers' : 'web'
	}

	package_type_to_architecture = {
		'c application' : 'any', 
		'c library' : 'any', 
		'mono application' : 'any', 
		'mono library' : 'any', 
		'python application' : 'all', 
		'python library' : 'all', 
		'documentation' : 'all'
	}

	package_type_to_file_thing = {
		'c application' : 'i386', 
		'c library' : 'i386', 
		'mono application' : 'i386', 
		'mono library' : 'i386', 
		'python application' : 'all', 
		'python library' : 'all', 
		'documentation' : 'all'
	}

	def build(self, meta, packages, packager_sudo, packager_gpg, use_chroot, is_interactive):
		if not use_chroot:
			print "Warning: Using pbuilder as the chroot anyway."

		# Make sure the password is legit
		print "Checking if we can use sudo ..."
		child = pexpect.spawn('bash -c "sudo -k; sudo su"', timeout=5)

		expected_lines = ["Sorry, try again.\r\n" + 
							"\[sudo\] password for [\w|\s]*: ", 
							"\[sudo\] password for [\w|\s]*: ", 
							'[$%#]', # command prompt
							pexpect.EOF]

		still_reading = True
		had_error = True
		while still_reading:
			result = child.expect(expected_lines)

			if result == 0:
				child.sendline("")
			elif result == 1:
				child.sendline(packager_sudo)
			elif result == 2:
				child.sendline("exit")
				had_error = False
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()
		if had_error:
			print "Incorrect password for sudo. Exiting ..."
			exit()

		# Clear the left overs from pbuilder
		if os.path.isdir("/var/cache/pbuilder/build/"):
			print "Removing the pbuilder scraps ..."
			for entry in os.listdir("/var/cache/pbuilder/build/"):
				child = pexpect.spawn('bash -c "sudo rm -rf /var/cache/pbuilder/build/' + entry + '"', timeout=5)
				expected_lines = ["\[sudo\] password for [\w|\s]*: ", 
									pexpect.EOF]

				still_reading = True
				try:
					while still_reading:
						result = child.expect(expected_lines)

						if result == 0:
							child.sendline(packager_sudo)
						elif result == len(expected_lines)-1:
							still_reading = False
				except Exception as err:
					print "    Warning: Failed to clean /var/cache/pbuilder/build/"
					child.sendcontrol('c')

				child.close()

			for entry in os.listdir("/var/cache/pbuilder/result/"):
				child = pexpect.spawn('bash -c "sudo rm -rf /var/cache/pbuilder/result/' + entry + '"', timeout=5)
				expected_lines = ["\[sudo\] password for [\w|\s]*: ", 
									pexpect.EOF]

				still_reading = True
				try:
					while still_reading:
						result = child.expect(expected_lines)

						if result == 0:
							child.sendline(packager_sudo)
						elif result == len(expected_lines)-1:
							still_reading = False
				except Exception as err:
					print "    Warning: Failed to clean /var/cache/pbuilder/result/"
					child.sendcontrol('c')

				child.close()

		# clear sudo so we don't use it till needed
		commands.getoutput("sudo -k")

		setup_source_code(meta)

		# Create the debian dir
		if not os.path.isdir("debian"): os.mkdir("debian")
		os.chdir("debian")

		# Copy any patches to the debian dir
		if not os.path.isdir("patches") and len(meta.patches) > 0:
			os.mkdir("patches")
		for patch in meta.patches:
			commands.getoutput("cp ../../../patches/" + meta.name + "/" + patch + " patches/" + patch)

		# Get the parameters
		params = meta.to_hash()
		params['packages'] = packages
		params['section'] = self.category_to_section[meta.category]
		params['build_requirements'] += ["debhelper (>= 7)", "autotools-dev"]
		params['category_to_section'] = self.category_to_section
		params['package_type_to_architecture'] = self.package_type_to_architecture

		# Find out which languages it uses
		for lang in ['c', 'python', 'mono']:
			params['uses_' + lang] = False
			for package in packages:
				if package.package_type == lang + ' application' or package.package_type == lang + ' library':
					params['uses_' + lang] = True

		# Add additional install requirements based on the languages it uses
		params['additional_install_requirements'] = ["${misc:Depends}", "${shlibs:Depends}"]
		if params['uses_c']:
			params['additional_install_requirements'] += []
		if params['uses_python']:
			params['additional_install_requirements'] += ["${python:Depends}"]
		if params['uses_mono']:
			params['additional_install_requirements'] += ["${cli:Depends}"]

		# Make sure any python programs have a setup.py
		if params['uses_python']:
			if meta.build_method =='python':
				if not os.path.isfile('../setup.py'):
					print "Packagetastic can only build python packages with a setup.py file. Exiting ..."
					exit()

		# Generate the rules file
		print "Generating the rules file ..."
		with open('rules', 'w') as rules_file:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.rules.py")
			rules_file.write(template.render(**params).replace("@@", "$"))

		# Create the compat file
		print "Generating the compat file ..."
		with open('compat', 'w') as f:
			f.write('7')

		# Create the pycompat file
		if params['uses_python']:
			print "Generating the pycompat file ..."
			with open('pycompat', 'w') as f:
				f.write('2')

		# Create the control file
		print "Generating the control file ..."
		with open('control', 'w') as control_file:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.control.py")
			control_file.write(template.render(**params).replace("@@", "$"))

		# Create the copyright file
		print "Generating the copyright file ..."
		with open('copyright', 'w') as copyright_file:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.copyright.py")
			copyright_file.write(template.render(**params).replace("@@", "$"))

		# Create the changelog
		print "Generating the changelog file ..."
		with open('changelog', 'w') as changelog_file:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.changelog.py")
			changelog_file.write(template.render(**params).replace("@@", "$"))

		# Generate the pre and post install scripts
		print "Generating the pre and post install scripts ..."
		for package in packages:
			if package.alternate_name != None:
				with open(package.name + '.post', 'w') as post_file:
					from mako.template import Template
					from mako.lookup import TemplateLookup
					lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
					template = lookup.get_template("template.post.py")
					post_file.write(template.render(**package.to_hash()).replace("@@", "$"))

				with open(package.name + '.prerm', 'w') as prerm_file:
					from mako.template import Template
					from mako.lookup import TemplateLookup
					lookup = TemplateLookup(directories=['../../../distros/ubuntu_templates/'], output_encoding='utf-8')
					template = lookup.get_template("template.prerm.py")
					prerm_file.write(template.render(**package.to_hash()).replace("@@", "$"))

		# Run debuild
		print "Running debuild ..."
		os.chdir("..")

		command = 'bash -c "debuild -S -sa"'

		if is_interactive:
			print commands.getoutput(command)
		else:
			child = pexpect.spawn(command, timeout=1200)

			expected_lines = ["dpkg-buildpackage -rfakeroot -d -us -uc -S -sa\r\n",
								"dpkg-buildpackage: set CFLAGS to default value: -g -O2\r\n",
								"dpkg-buildpackage: set CPPFLAGS to default value:\r\n",
								"dpkg-buildpackage: set LDFLAGS to default value: -Wl,-Bsymbolic-functions\r\n",
								"dpkg-buildpackage: set FFLAGS to default value: -g -O2\r\n",
								"dpkg-buildpackage: set CXXFLAGS to default value: -g -O2\r\n",
								"dpkg-buildpackage: source package " + meta.name + "\r\n",
								"dpkg-buildpackage: source version " + meta.version + "-" + str(meta.release) + "\r\n",
								"dpkg-buildpackage: source changed by " + meta.packager_name + " <" + meta.packager_email + ">" + "\r\n",
								"fakeroot debian/rules clean",
								"dh_testdir",
								"dh_testroot",
								"rm -f build-stamp",
								"rm -f config.sub config.guess",
								"dh_clean",
								"dpkg-source -b " + meta.name + "-" + meta.version,
								"dpkg-source: info: using source format `1.0'",
								"dpkg-source: info: building " + meta.name + " using existing " + meta.name + "_" + meta.version + ".orig.tar.gz",
								"dpkg-source: info: building " + meta.name + " in " + meta.name + "_" + meta.version + "-" + str(meta.release) + ".diff.gz",
								"dpkg-source: info: building " + meta.name + " in " + meta.name + "_" + meta.version + "-" + str(meta.release) + ".dsc",
								"dpkg-genchanges: including full source code in upload",
								"dpkg-buildpackage: source only upload (original source is included)",
								"Now running lintian...",
								"Now signing changes and any dsc files...",
								"dpkg-source: error:",
								"dpkg-buildpackage: failure:",

								"Finished running lintian.",

								"You need a passphrase to unlock the secret key for\r\n" +
								"user: \"" + meta.packager_name + " <" + meta.packager_email + ">" + "\"\r\n" +
								"1024-bit DSA key, ID [\w]*, created \d*-\d*-\d*\r\n" +
								"\r\n" +
								"Enter passphrase: [\w|\s\W]*",

								"gpg: Invalid passphrase; please try again ...",

								"dpkg-source: error: syntax error in " + meta.name + "-" + meta.version + "/debian/control at line \d*: ",

								"dpkg-buildpackage: failure: fakeroot debian/rules clean gave error exit status 2", 

								"Successfully signed dsc and changes files\r\n",

								"W\: " + meta.name + " source\: [\w|\d|\s|\W|\.|\-]*\r\n",

								"E\: " + meta.name + " source\: [\w|\d|\s|\W|\.|\-]*\r\n",

								"ImportError: No module named [\w|\d|\.|\-|\_]*\r\n", 

								pexpect.EOF]

			still_reading = True
			had_lintian_error = False
			while still_reading:
				result = child.expect(expected_lines)

				if result >= 0 and result <= 25:
					pass
				elif result == 26 and had_lintian_error:
					print "Lintian has errors. Exiting ..."
					exit()
				elif result == 27:
					child.sendline(packager_gpg)
				elif result == 28:
					print "Invalid gpg password. Exiting ..."
					exit()
				elif result == 29:
					print "Broke when reading the debian/control file '" + \
					child.after + "'. Exiting ..."
					exit()
				elif result == 30:
					print "Broke when running clean from the debian/rules file '" + \
					child.after + "'. Exiting ..."
					exit()
				elif result == 31:
					pass
				elif result == 32:
					print "    Lintian warning: " + child.after[3:-2]
				elif result == 33:
					print "    Lintian error: " + child.after[3:-2]
					had_lintian_error = True
				elif result == 34:
					print "Compile error. " + child.after + " Exiting ..."
					exit()
				elif result == len(expected_lines)-1:
					still_reading = False

			child.close()

		# Run pbuilder
		print "Running pbuilder ..."
		os.chdir("..")

		command = 'bash -c "sudo pbuilder build ' + meta.name + '_' + meta.version + '-' + str(meta.release) + '.dsc"'
		if is_interactive:
			print commands.getoutput(command)
		else:
			child = pexpect.spawn(command, timeout=1200)

			expected_lines = ["\[sudo\] password for [\w|\s]*: ",

								"pbuilder: Failed autobuilding of package", 

								"patching file [\w|\s|\d|\.|\-|\/]*\r\nHunk \#\d FAILED at [\d]*\.\r\nHunk \#\d FAILED at [\d]*\.\r\n", 

								"patch -p0 < debian\/patches\/[\d|\w|\.|\-|\_]*\r\ncan't find file to patch at input line [\d]*", 

								"The following packages have unmet dependencies:\r\n" + 
								"[\w|\W|\s|\d|\.|\-|\/|\r|\n]*" + 
								"The following actions will resolve these dependencies:", 

								"error: can\'t copy \'[\w|\s|\d|\.|\-|\/]*\': doesn\'t exist or not a regular file", 

								pexpect.EOF]

			still_reading = True
			had_error = False
			while still_reading:
				result = child.expect(expected_lines)

				if result == 0:
					child.sendline(packager_sudo)
				elif result == 1 and not had_error:
					print "Failed to build package. Make sure it can be compiled manually before trying to package. Exiting ..."
					had_error = True
				elif result == 2:
					print "Failed to build package. Broke when applying patch. Exiting ..."
					print child.after
					had_error = True
				elif result == 3:
					print "Failed to build package. Broke when applying patch. Exiting ..."
					print child.after
					had_error = True
					child.sendcontrol('c')
				elif result == 4:
					print "Failed to build. Dependencies not in the repositories:"
					for entry in child.after.split('Depends: ')[1:]:
						print entry.strip().split(' which is a')[0]
					print "Exiting ..."
					had_error = True
				elif result == 5:
					file_name = child.after.split("error: can't copy '")[1].split("':")[0]
					print "File not found: '" + file_name + "'. Exiting ..."
					had_error = True
				elif result == len(expected_lines)-1:
					still_reading = False

			child.close()
			if had_error:
				exit()

		# Copy the deb files from the cache
		print "Getting the deb files ..."
		os.chdir('..')
		if not os.path.isdir("packages"): os.mkdir("packages")
		for package in packages:
			thing = self.package_type_to_file_thing[package.package_type]
			command = "cp /var/cache/pbuilder/result/" + \
					package.name + "_" + meta.version + '-' + str(meta.release) + "_" + thing + ".deb " + \
					"packages/" + \
					package.name + "_" + meta.version + '-' + str(meta.release) + "_" + thing + ".deb"
			print commands.getoutput(command)

		print "Done"

