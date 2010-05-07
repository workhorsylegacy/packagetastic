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

		# Clear sudo so we don't use it till needed
		commands.getoutput("sudo -k")

		# Build the package
		setup_source_code(meta)
		meta.build()

		# Get the parameters
		params = meta.to_hash()
		params['packages'] = packages
		params['section'] = self.category_to_section[meta.category]
		params['build_requirements'] += ["debhelper (>= 7)", "autotools-dev"]
		params['category_to_section'] = self.category_to_section
		params['package_type_to_architecture'] = self.package_type_to_architecture

		# Add custom parameters
		for package in packages:
			package.custom['size'] = 0
			for entry in package.files:
				if not os.path.isfile(entry): continue
				package.custom['size'] += os.path.getsize(entry)

		# Generate the *.list file
		f = open('/home/matt/Desktop/dpkg/info/hello.list', 'w')
		f.write("/.\n")
		existing_paths = []
		for package in packages:
			for entry in package.files:
				if not os.path.isfile(entry): continue
				path = ''
				for part in entry.split('/'):
					if part == '': continue
					path += '/' + part
					if not path in existing_paths:
						existing_paths.append(path)
						f.write(path + "\n")

		f.write("\n")
		f.close()

		# Generate the *.md5sums file
		f = open('/home/matt/Desktop/dpkg/info/hello.md5sums', 'w')
		existing_paths = []
		for package in packages:
			for entry in package.files:
				if not os.path.isfile(entry): continue

				md5sum = commands.getoutput("md5sum " + entry)
				f.write(md5sum + "\n")

		f.write("\n")
		f.close()

		# Copy status to status-old
		if os.path.isfile('/home/matt/Desktop/dpkg/status-old'):
			os.remove('/home/matt/Desktop/dpkg/status-old')
		shutil.copy2('/home/matt/Desktop/dpkg/status', '/home/matt/Desktop/dpkg/status-old')

		# Generate the temp status file
		with open('/home/matt/Desktop/dpkg/temp-status', 'w') as f:
			from mako.template import Template
			from mako.lookup import TemplateLookup
			lookup = TemplateLookup(directories=['../../distros/ubuntu_templates/'], output_encoding='utf-8')
			template = lookup.get_template("template.status.py")
			f.write(template.render(**params).replace("@@", "$"))

		# Append the new status to the existing status
		with open('/home/matt/Desktop/dpkg/status', 'a') as status:
			with open('/home/matt/Desktop/dpkg/temp-status', 'r') as temp_status:
				status.write(temp_status.read())
		os.remove('/home/matt/Desktop/dpkg/temp-status')

		print "Done"

