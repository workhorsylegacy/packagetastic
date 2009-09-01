
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

	def build(self, meta, packages, root_password, gpg_password):
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
				child.sendline(root_password)
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
				while still_reading:
					result = child.expect(expected_lines)

					if result == 0:
						child.sendline(root_password)
					elif result == len(expected_lines)-1:
						still_reading = False

				child.close()

			for entry in os.listdir("/var/cache/pbuilder/result/"):
				child = pexpect.spawn('bash -c "sudo rm -rf /var/cache/pbuilder/result/' + entry + '"', timeout=5)
				expected_lines = ["\[sudo\] password for [\w|\s]*: ", 
									pexpect.EOF]

				still_reading = True
				while still_reading:
					result = child.expect(expected_lines)

					if result == 0:
						child.sendline(root_password)
					elif result == len(expected_lines)-1:
						still_reading = False

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

		params['additional_install_requirements'] = []
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			params['additional_install_requirements'] = ["${shlibs:Depends}", "${misc:Depends}"]
		elif meta.build_method == 'python application' or meta.build_method == 'python library':
			params['install_requirements'] = ["${python:Depends}", "${misc:Depends}"]
		elif meta.build_method == 'mono application' or meta.build_method == 'mono library':
			params['additional_install_requirements'] = ["${cli:Depends}", "${misc:Depends}", "${shlibs:Depends}"]
		else:
			print "Unknown build method for generating control file '" + meta.build_method + "'. Exiting ..."
			exit()

		# Generate the rules file
		print "Generating the rules file ..."
		with open('../../../distros/ubuntu_templates/template.rules.py') as rules_template:
			from mako.template import Template
			template = Template(rules_template.read())
			with open('rules', 'w') as rules_file:
				rules_file.write(template.render(**params).replace("@@", "$"))

		# Create the compat file
		print "Generating the compat file ..."
		with open('compat', 'w') as f:
			f.write('7')

		# Create the control file
		print "Generating the control file ..."
		with open('../../../distros/ubuntu_templates/template.control.py') as control_template:
			from mako.template import Template
			template = Template(control_template.read())
			with open('control', 'w') as control_file:
				control_file.write(template.render(**params).replace("@@", "$"))

		# Create the copyright file
		print "Generating the copyright file ..."
		with open('../../../distros/ubuntu_templates/template.copyright.py') as copyright_template:
			from mako.template import Template
			template = Template(copyright_template.read())
			with open('copyright', 'w') as copyright_file:
				copyright_file.write(template.render(**params).replace("@@", "$"))

		# Create the changelog
		print "Generating the changelog file ..."
		with open('../../../distros/ubuntu_templates/template.changelog.py') as changelog_template:
			from mako.template import Template
			template = Template(changelog_template.read())
			with open('changelog', 'w') as changelog_file:
				changelog_file.write(template.render(**params).replace("@@", "$"))

		# Generate the pre and post install scripts
		print "Generating the pre and post install scripts ..."
		for package in packages:
			if package.alternate_name != None:
				with open('../../../distros/ubuntu_templates/template.post.py') as post_template:
					from mako.template import Template
					template = Template(post_template.read())
					with open(package.name + '.post', 'w') as post_file:
						post_file.write(template.render(**params).replace("@@", "$"))

				with open('../../../distros/ubuntu_templates/template.prerm.py') as prerm_template:
					from mako.template import Template
					template = Template(prerm_template.read())
					with open(package.name + '.prerm', 'w') as prerm_file:
						prerm_file.write(template.render(**params).replace("@@", "$"))

		# Run debuild
		print "Running debuild ..."
		os.chdir("..")

		command = 'bash -c "debuild -S -sa"'
		#print commands.getoutput(command)
		#"""
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

							pexpect.EOF]

		still_reading = True
		had_lintian_error = False
		while still_reading:
			result = child.expect(expected_lines)

			if result >= 0 and result <= 25:
				pass
			elif result == 26 and had_lintian_error:
				print "Exiting because of Lintian error ..."
				exit()
			elif result == 27:
				child.sendline(gpg_password)
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
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()
		#"""

		# Run pbuilder
		print "Running pbuilder ..."
		os.chdir("..")

		command = 'bash -c "sudo pbuilder build ' + meta.name + '_' + meta.version + '-' + str(meta.release) + '.dsc"'
		print commands.getoutput(command)
		"""
		child = pexpect.spawn(command, timeout=1200)

		expected_lines = ["\[sudo\] password for [\w|\s]*: ",

							"pbuilder: Failed autobuilding of package", 

							"patching file [\w|\s|\d|\.|\-|\/]*\r\nHunk \#\d FAILED at [\d]*\.\r\nHunk \#\d FAILED at [\d]*\.\r\n", 

							"patch -p0 < debian\/patches\/[\d|\w|\.|\-|\_]*\r\ncan't find file to patch at input line [\d]*", 

							"The following packages have unmet dependencies:\r\n" + 
							"[\w|\W|\s|\d|\.|\-|\/|\r|\n]*" + 
							"The following actions will resolve these dependencies:", 

							pexpect.EOF]

		still_reading = True
		had_error = False
		while still_reading:
			result = child.expect(expected_lines)

			if result == 0:
				child.sendline(root_password)
			elif result == 1:
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
			elif result == len(expected_lines)-1:
				still_reading = False

		child.close()
		if had_error:
			exit()
		"""

		# Copy the deb files from the cache
		print "Getting the deb files ..."
		os.chdir('..')
		if not os.path.isdir("packages"): os.mkdir("packages")
		for package in packages:
			command = "cp /var/cache/pbuilder/result/" + \
					package.name + "_" + meta.version + '-' + str(meta.release) + "_" + meta.build_arch + ".deb " + \
					"packages/" + \
					package.name + "_" + meta.version + '-' + str(meta.release) + "_" + meta.build_arch + ".deb"
			print commands.getoutput(command)

		print "Done"

