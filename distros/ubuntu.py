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
		'c application' : 'i386', 
		'c library' : 'i386', 
		'mono application' : 'i386', 
		'mono library' : 'i386', 
		'python application' : 'all', 
		'python library' : 'all', 
		'documentation' : 'all'
	}

	def build(self, meta, packages):
		home = os.path.expanduser('~')

		# Build the package
		setup_source_code(meta)
		meta.build()

		# Make sure all the listed files exist
		unknown_files = []
		for package in packages:
			for entry in package.files:
				if not os.path.isfile(entry):
					unknown_files.append(entry)

		if unknown_files:
			print "Files that were listed in the stem file were not found:"
			for entry in unknown_files:
				print entry
			exit()

		# Get the parameters
		params = meta.to_hash()
		params['package'] = None
		params['section'] = self.category_to_section[meta.category]
		params['build_requirements'] += ["debhelper (>= 7)", "autotools-dev"]
		params['category_to_section'] = self.category_to_section
		params['package_type_to_architecture'] = self.package_type_to_architecture

		# Add custom parameters
		for package in packages:
			package.custom['size'] = 0
			for entry in package.files:
				if not os.path.isfile(entry): continue
				package.custom['size'] += os.path.getsize(entry) / 1024

		# Generate the *.list files
		for package in packages:
			f = open(home + '/.packagetastic/' + meta.name + '/' + package.name + '.list', 'w')
			f.write("/.\n")
			existing_paths = []
			for entry in package.files:
				if not os.path.isfile(entry): continue
				path = ''
				for part in entry.split('/'):
					if part == '': continue
					path += '/' + part
					if not path in existing_paths:
						existing_paths.append(path)
						f.write(path + "\n")

			f.close()

		# Generate the *.md5sums files
		for package in packages:
			f = open(home + '/.packagetastic/' + meta.name + '/' + package.name + '.md5sums', 'w')
			existing_paths = []
			for entry in package.files:
				if not os.path.isfile(entry): continue

				md5sum = commands.getoutput("md5sum " + entry)
				f.write(md5sum + "\n")

			f.write("\n")
			f.close()

		# Generate the temp status files
		for package in packages:
			params['package'] = package
			with open(home + '/.packagetastic/' + meta.name + '/' + package.name + '.status', 'w') as f:
				from mako.template import Template
				from mako.lookup import TemplateLookup
				lookup = TemplateLookup(directories=['../../distros/ubuntu_templates/'], output_encoding='utf-8')
				template = lookup.get_template("template.status.py")
				f.write(template.render(**params).replace("@@", "$"))

		# Generate the temp available files
		for package in packages:
			params['package'] = package
			with open(home + '/.packagetastic/' + meta.name + '/' + package.name + '.available', 'w') as f:
				from mako.template import Template
				from mako.lookup import TemplateLookup
				lookup = TemplateLookup(directories=['../../distros/ubuntu_templates/'], output_encoding='utf-8')
				template = lookup.get_template("template.available.py")
				f.write(template.render(**params).replace("@@", "$"))

		# Copy all the files for this package
		for package in packages:
			for entry in package.files:
				dir_name = str.join('/', entry.split('/')[:-1])
				run_as_root('mkdir -p ' + home + '/.packagetastic/' + meta.name + dir_name)
				run_as_root('cp ' + entry + ' ' + home + '/.packagetastic/' + meta.name + entry)
		for package in packages:
			for entry in package.files:
				run_as_root('rm ' + entry)

		# Compress all the files into a package
		user_name = commands.getoutput('whoami')
		run_as_root('chown -R ' + user_name + ' ' + home + '/.packagetastic/' + meta.name)
		package = home + '/.packagetastic/' + meta.name
		commands.getoutput('tar --force-local --no-wildcards -v -p -cf ' + package + '_' + meta.version + '_ubuntu-10.04_i386.pkg --use-compress-program=gzip ' + package)

	def install(self, meta, packages):
		home = os.path.expanduser('~')

		# Copy all the files
		for package in packages:
			for entry in package.files:
				dir_name = str.join('/', entry.split('/')[:-1])
				if os.path.isdir(dir_name):
					run_as_root('mkdir -p ' + dir_name)
				run_as_root('cp ' + home + '/.packagetastic/' + meta.name + entry + ' ' + entry)

		# Copy the *.list and *.md5sums
		for package in packages:
			run_as_root("cp " + home + '/.packagetastic/' + meta.name + '/' + package.name + '.list /var/lib/dpkg/info/' + package.name + '.list')
			run_as_root("cp " + home + '/.packagetastic/' + meta.name + '/' + package.name + '.md5sums /var/lib/dpkg/info/' + package.name + '.md5sums')

		# Rename status to status-old, and create the new status
		if os.path.isfile('/var/lib/dpkg/status-old'):
			run_as_root("rm /var/lib/dpkg/status-old")
		run_as_root("mv /var/lib/dpkg/status /var/lib/dpkg/status-old")
		run_as_root("cp /var/lib/dpkg/status-old /var/lib/dpkg/status")

		# Append the new status to the existing status
		for package in packages:
			run_as_root("cat " + home + "/.packagetastic/" + meta.name + "/" + package.name + ".status" + " >> /var/lib/dpkg/status")

		# Rename available to available-old, and create the new available
		if os.path.isfile('/var/lib/dpkg/available-old'):
			run_as_root("rm /var/lib/dpkg/available-old")
		run_as_root("mv /var/lib/dpkg/available /var/lib/dpkg/available-old")
		run_as_root("cp /var/lib/dpkg/available-old /var/lib/dpkg/available")

		for package in packages:
			is_available = False
			with open('/var/lib/dpkg/available', 'r') as f:
				for entry in f.read().split("\r\n\r\n"):
					if entry.count('Package: ' + meta.name):
						is_available = True

			# FIXME: This should update the existing package data
			# Append the new available to the existing available
			if not is_available:
				run_as_root("cat " + home + "/.packagetastic/" + meta.name + "/" + package.name + ".available" + " >> /var/lib/dpkg/available")

		run_as_root("touch /var/lib/dpkg/lock")

		print "Done"

