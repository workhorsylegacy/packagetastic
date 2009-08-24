

class Builder(object):
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
			print "Incorrect password for root. Exiting ..."
			exit()

		# Clear the left overs from pbuilder
		if os.path.isdir("/var/cache/pbuilder/build/"):
			print "Clearing the pbuilder scraps ..."
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

		# Make sure the source code exists
		if not os.path.isfile("sources/" + meta.source.split('/')[-1]):
			print substitute_strings("Missing source code at: sources/" + meta.source.split('/')[-1] + ". Exiting ...", meta.to_hash())
			exit()

		# Convert any .tar.bz2 files to .tar.gz
		if meta.source.split('/')[-1].endswith('.tar.bz2'):
			os.chdir('sources')
			dir_name = meta.source.split('/')[-1].rstrip('.tar.bz2')
			print "Converting bzip source code to gzip ..."
			commands.getoutput("tar xjf " + meta.source.split('/')[-1])
			commands.getoutput(substitute_strings("mv " + dir_name + " #{name}-#{version}", meta.to_hash()))
			commands.getoutput(substitute_strings("tar -czf #{name}-#{version}.tar.gz #{name}-#{version}", meta.to_hash()))
			commands.getoutput(substitute_strings("rm -rf #{name}-#{version}", meta.to_hash()))
			meta.source = meta.source.rstrip(meta.source.split('/')[-1]) + substitute_strings("#{name}-#{version}.tar.gz", meta.to_hash())
			os.chdir('..')

		# Uncompress the source code
		print "Uncompressing source code ..."
		if not os.path.isdir("builds"): os.mkdir("builds")
		commands.getoutput(substitute_strings("cp sources/" + meta.source.split('/')[-1] + " builds/#{name}_#{version}.orig.tar.gz", meta.to_hash()))
		os.chdir("builds")
		commands.getoutput(substitute_strings("tar xzf #{name}_#{version}.orig.tar.gz", meta.to_hash()))
		os.chdir(substitute_strings("#{name}-#{version}", meta.to_hash()))

		# Create the debian dir
		if not os.path.isdir("debian"): os.mkdir("debian")
		os.chdir("debian")

		# Copy any patches
		if os.path.isdir("../../../patches/" + meta.name) == True:
			patch_files = os.listdir("../../../patches/" + meta.name)
			patch_files.sort()
			if not os.path.isdir("patches"): os.mkdir("patches")
			for patch_file in patch_files:
				if not patch_file.endswith("patch"): continue
				commands.getoutput("cp ../../../patches/" + meta.name + "/" + patch_file + " patches/" + patch_file)

		# Generate the rules file
		print "Generating the rules file ..."
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			self.generate_rules_file_for_c(meta, packages)
		elif meta.build_method == 'python application' or meta.build_method == 'python library':
			self.generate_rules_file_for_python(meta, packages)
		elif meta.build_method == 'mono application':
			self.generate_rules_file_for_mono_application(meta, packages)
		else:
			print "Unknown build method for generating rules file '" + meta.build_method + "'. Exiting ..."
			exit()

		# Create the compat file
		print "Generating compat file ..."
		f = open('compat', 'w')
		f.write('7')
		f.close()

		# Create the control file
		print "Generating control file ..."
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			self.generate_control_file_for_c(meta, packages)
		elif meta.build_method == 'python application':
			self.generate_control_file_for_python_application(meta, packages)
		elif meta.build_method == 'python library':
			self.generate_control_file_for_python_library(meta, packages)
		elif meta.build_method == 'mono application':
			self.generate_control_file_for_mono_application(meta, packages)
		else:
			print "Unknown build method for generating control file '" + meta.build_method + "'. Exiting ..."
			exit()


		# Create the copyright file
		print "Generating copyright file ..."
		f = open('copyright', 'w')

		f.write(substitute_strings(
"""This package was debianized by #{packager_name} <#{packager_email}> on 
#{timestring}.

It was downloaded from #{homepage}

#{upstream_authors}:

    #{authors}

Copyright:

    Copyright (C) #{copyright}

License:

#{license_text}

The Debian packaging is (C) #{year}, #{packager_name} <#{packager_email}> and
is licensed under the #{license}, see above.
""", meta.to_hash()))

		f.close()


		# Get the mangled gibberish that is on the end of a package file name
		mangle = 1

		# Create the changelog
		changelog_body = ""
		if meta.changelog == None:
			print "The changelog is missing. Exiting ..."
			exit()

		prev_version = '0'
		reverse_entries = meta.changelog[:]
		reverse_entries.reverse()
		for item in reverse_entries:
			if prev_version == item['version']:
				mangle += 1
			else:
				mangle = 1
			prev_version = item['version']

			entry = substitute_strings(
"""#{name} (#{item_version}-#{mangle}) unstable; urgency=low

  * #{item_text}

 -- #{packager_name} <#{packager_email}>  #{item_time}

""", meta.to_hash({'mangle' : str(mangle), 
					'item_version' : item['version'], 
					'item_time' : item['time'], 
					'item_text' : item['text']}))

			changelog_body = entry + changelog_body

		f = open('changelog', 'w')
		f.write(changelog_body)
		f.close()

		# Generate the .post install file
		for package in packages:
			if package.alternate_name != None:
				# Create the post install script
				f = open(package.name + '.postinst', 'w')

				f.write(substitute_strings(
"""#!/bin/sh

set -e

if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ]; then
	update-alternatives --install /usr/bin/#{alternate_name} #{alternate_name} /usr/bin/#{name} 50 \\
	  --slave /usr/share/man/man1/#{alternate_name}.1.gz #{alternate_name}.1.gz \\
	  /usr/share/man/man1/#{name}.1.gz
fi

#DEBHELPER#
""", package.to_hash()))

				f.close()

				# Create the post uninstall script
				f = open(package.name + '.prerm', 'w')

				f.write(substitute_strings(
"""#!/bin/sh
 
set -e

if [ "$1" != "upgrade" ]; then
	update-alternatives --remove #{alternate_name} /usr/bin/#{name}
fi

#DEBHELPER#
""", package.to_hash()))

				f.close()

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
							"dpkg-buildpackage: source version " + meta.version + "-" + str(mangle) + "\r\n",
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
							"dpkg-source: info: building " + meta.name + " in " + meta.name + "_" + meta.version + "-" + str(mangle) + ".diff.gz",
							"dpkg-source: info: building " + meta.name + " in " + meta.name + "_" + meta.version + "-" + str(mangle) + ".dsc",
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

		command = 'bash -c "sudo pbuilder build ' + meta.name + '_' + meta.version + '-' + str(mangle) + '.dsc"'
		#print commands.getoutput(command)
		#"""
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
		#"""

		# Determine the architecture
		architecture = 'any'
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			architecture = 'i386'
		elif meta.build_method == 'python application':
			architecture = 'all'
		elif meta.build_method == 'python library':
			architecture = 'all'
		elif meta.build_method == 'mono application':
			architecture = 'i386'
		else:
			print "Unknown build method for setting architecture '" + meta.build_method + "'. Exiting ..."
			exit()

		# Copy the deb files from the cache
		print "Getting the deb files ..."
		os.chdir('..')
		if not os.path.isdir("packages"): os.mkdir("packages")
		for package in packages:
			command = "cp /var/cache/pbuilder/result/" + \
					package.name + "_" + meta.version + '-' + str(mangle) + "_" + architecture + ".deb " + \
					"packages/" + \
					package.name + "_" + meta.version + '-' + str(mangle) + "_" + architecture + ".deb"
			print commands.getoutput(command)

		print "Done"

	def generate_rules_file_for_c(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash()

		# Add patches
		fields["patches"] = ""
		if os.path.isdir("patches"):
			patch_files = os.listdir("patches")
			patch_files.sort()
			for patch_file in patch_files:
				fields["patches"] += "\tpatch -p0 < debian/patches/" + patch_file + "\n"

			fields["patches"] += "\n"

		f = open('rules', 'w')
		f.write(substitute_strings(
"""#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1


# These are used for cross-compiling and for saving the configure script
# from having to guess our platform (since we know it already)
DEB_HOST_GNU_TYPE   ?= $(shell dpkg-architecture -qDEB_HOST_GNU_TYPE)
DEB_BUILD_GNU_TYPE  ?= $(shell dpkg-architecture -qDEB_BUILD_GNU_TYPE)
ifneq ($(DEB_HOST_GNU_TYPE),$(DEB_BUILD_GNU_TYPE))
CROSS= --build $(DEB_BUILD_GNU_TYPE) --host $(DEB_HOST_GNU_TYPE)
else
CROSS= --build $(DEB_BUILD_GNU_TYPE)
endif



config.status: configure
	dh_testdir
	# Add here commands to configure the package.
ifneq "$(wildcard /usr/share/misc/config.sub)" ""
	cp -f /usr/share/misc/config.sub config.sub
endif
ifneq "$(wildcard /usr/share/misc/config.guess)" ""
	cp -f /usr/share/misc/config.guess config.guess
endif
	./configure $(CROSS) --prefix=/usr --mandir=\$${prefix}/share/man --infodir=\$${prefix}/share/info CFLAGS="$(CFLAGS)" LDFLAGS="-Wl,-z,defs"


build: build-stamp

build-stamp:  config.status 
	dh_testdir

#{patches}
	# Add here commands to compile the package.
	$(MAKE)
	#docbook-to-man debian/#{name}.sgml > #{name}.1

	touch $@

clean: 
	dh_testdir
	dh_testroot
	rm -f build-stamp 

	# Add here commands to clean up after the build process.
	[ ! -f Makefile ] || $(MAKE) distclean
	rm -f config.sub config.guess

	dh_clean 

install: build
	dh_testdir
	dh_testroot
	dh_prep  
	dh_installdirs

	# Add here commands to install the package into debian/#{name}.
	$(MAKE) DESTDIR=$(CURDIR)/debian/#{name} install


# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
	dh_installchangelogs ChangeLog
	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install 
""", fields))
		f.close()

	def generate_rules_file_for_mono_application(self, meta, packages):

		fields = meta.to_hash()

		# Add patches
		fields["patches"] = ""
		if os.path.isdir("patches"):
			patch_files = os.listdir("patches")
			patch_files.sort()
			for patch_file in patch_files:
				fields["patches"] += "\tpatch -p0 < debian/patches/" + patch_file + "\n"

			fields["patches"] += "\n"

		f = open('rules', 'w')
		f.write(substitute_strings(
"""#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.

# Uncomment this to turn on verbose mode.
#export DH_VERBOSE=1


# These are used for cross-compiling and for saving the configure script
# from having to guess our platform (since we know it already)
DEB_HOST_GNU_TYPE   ?= $(shell dpkg-architecture -qDEB_HOST_GNU_TYPE)
DEB_BUILD_GNU_TYPE  ?= $(shell dpkg-architecture -qDEB_BUILD_GNU_TYPE)
ifneq ($(DEB_HOST_GNU_TYPE),$(DEB_BUILD_GNU_TYPE))
CROSS= --build $(DEB_BUILD_GNU_TYPE) --host $(DEB_HOST_GNU_TYPE)
else
CROSS= --build $(DEB_BUILD_GNU_TYPE)
endif



config.status: configure
	dh_testdir
	# Add here commands to configure the package.
ifneq "$(wildcard /usr/share/misc/config.sub)" ""
	cp -f /usr/share/misc/config.sub config.sub
endif
ifneq "$(wildcard /usr/share/misc/config.guess)" ""
	cp -f /usr/share/misc/config.guess config.guess
endif
	./configure $(CROSS) --prefix=/usr --mandir=\$${prefix}/share/man --infodir=\$${prefix}/share/info CFLAGS="$(CFLAGS)" LDFLAGS="-Wl,-z,defs"


build: build-stamp

build-stamp:  config.status 
	dh_testdir

#{patches}
	# Add here commands to compile the package.
	$(MAKE)
	#docbook-to-man debian/#{name}.sgml > #{name}.1

	touch $@

clean: 
	dh_testdir
	dh_testroot
	rm -f build-stamp 

	# Add here commands to clean up after the build process.
	[ ! -f Makefile ] || $(MAKE) distclean
	rm -f config.sub config.guess

	dh_clean 

install: build
	dh_testdir
	dh_testroot
	dh_prep  
	dh_installdirs

	# Add here commands to install the package into debian/#{name}.
	$(MAKE) DESTDIR=$(CURDIR)/debian/#{name} install


# Build architecture-independent files here.
binary-indep: build install
# We have nothing to do by default.

# Build architecture-dependent files here.
binary-arch: build install
	dh_testdir
	dh_testroot
	dh_installchangelogs ChangeLog
	dh_installdocs
	dh_installexamples
#	dh_install
#	dh_installmenu
#	dh_installdebconf
#	dh_installlogrotate
#	dh_installemacsen
#	dh_installpam
#	dh_installmime
#	dh_python
#	dh_installinit
#	dh_installcron
#	dh_installinfo
	dh_installman
	dh_link
	dh_strip
	dh_compress
	dh_fixperms
#	dh_perl
#	dh_makeshlibs
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install 
""", fields))

		f.close()

	def generate_rules_file_for_python(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash()

		# Determine if there is a changelog
		if os.path.isfile('../ChangeLog'):
			fields['changelog'] = "DEB_INSTALL_CHANGELOGS_ALL := ChangeLog"

		# Determine if it is built with distutils or autotools
		if os.path.isfile('../setup.py'):
			fields['build_script'] = 'python-distutils'
		elif os.path.isfile('../configure.ac'):
			fields['build_script'] = 'autotools'

		f = open('rules', 'w')
		f.write(substitute_strings(
"""#!/usr/bin/make -f
# -*- makefile -*-
DEB_PYTHON_SYSTEM = pycentral

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/class/#{build_script}.mk
include /usr/share/cdbs/1/rules/simple-patchsys.mk
include /usr/share/cdbs/1/rules/utils.mk

#{changelog}

binary-install/#{name}::
	dh_icons -p#{name}

clean::
	rm -rf build/
""", fields))

		f.close()

	def generate_control_file_for_c(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash({
						'build_requirements' : ["debhelper (>= 7)", "autotools-dev"] + meta.build_requirements,
		})

		f = open('control', 'w')
		f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
Priority: #{priority}
Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: #{build_requirements}
Standards-Version: 3.8.0
Homepage: #{homepage}
""", fields))

		for package in packages:
			# Make additions to fields
			fields = package.to_hash({
							'install_requirements' : ["${shlibs:Depends}", "${misc:Depends}"] + package.install_requirements, 
							'short_description' : package.meta.short_description, 
							'long_description' : package.meta.long_description
			})

			# Make changes to fields
			if len(package.additional_description) > 0:
				fields['long_description'] += "\n\n" + package.additional_description
			fields['long_description'] = ' ' + fields['long_description'].replace("\n", "\n ").replace("\n \n", "\n .\n") 

			f.write(substitute_strings(
"""
Package: #{name}
Section: #{section}
Priority: #{priority}
Architecture: any
Depends: #{install_requirements}
Description: #{short_description}
#{long_description}
""", fields))

		f.close()

	def generate_control_file_for_mono_application(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash({
						'build_requirements' : ["debhelper (>= 7)", "autotools-dev"] + meta.build_requirements
		})

		f = open('control', 'w')
		f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
Priority: #{priority}
Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: #{build_requirements}
Standards-Version: 3.8.0
Homepage: #{homepage}
""", fields))

		for package in packages:
			# Make additions to fields
			fields = package.to_hash({
							'install_requirements' : ["${cli:Depends}", "${misc:Depends}", "${shlibs:Depends}"] + package.install_requirements, 
							'short_description' : package.meta.short_description, 
							'long_description' : package.meta.long_description
			})

			# Make changes to fields
			if len(package.additional_description) > 0:
				fields['long_description'] += "\n\n" + package.additional_description
			fields['long_description'] = ' ' + fields['long_description'].replace("\n", "\n ").replace("\n \n", "\n .\n") 

			f.write(substitute_strings(
"""
Package: #{name}
Section: #{section}
Priority: #{priority}
Architecture: any
Depends: #{install_requirements}
Description: #{short_description}
#{long_description}
""", fields))

		f.close()

	def generate_control_file_for_python_application(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash({
						'build_requirements' : ["debhelper (>= 7)", "autotools-dev"] + meta.build_requirements
		})

		f = open('control', 'w')
		f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
Priority: #{priority}
XS-Python-Version: all
Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: debhelper (>= 5.0.62), python, cdbs (>= 0.4.49), #{build_requirements}
Build-Depends-Indep: python-central (>= 0.5.6)
Standards-Version: 3.8.0
Homepage: #{homepage}
""", fields))

		for package in packages:
			# Make additions to fields
			fields = package.to_hash({
							'install_requirements' : ["${python:Depends}", "${misc:Depends}"] + package.install_requirements, 
							'short_description' : package.meta.short_description, 
							'long_description' : package.meta.long_description
			})

			# Make changes to fields
			if len(package.additional_description) > 0:
				fields['long_description'] += "\n\n" + package.additional_description
			fields['long_description'] = ' ' + fields['long_description'].replace("\n", "\n ").replace("\n \n", "\n .\n") 

			f.write(substitute_strings(
"""
Package: #{name}
Section: #{section}
Priority: #{priority}
Architecture: all
Depends: #{install_requirements}
XB-Python-Version: ${python:Versions}
Description: #{short_description}
#{long_description}
""", fields))

		f.close()

	def generate_control_file_for_python_library(self, meta, packages):
		# Make additions to fields
		fields = meta.to_hash({
						'build_requirements' : ["debhelper (>= 7)", "autotools-dev"] + meta.build_requirements
		})

		f = open('control', 'w')
		f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
Priority: #{priority}
XS-Python-Version: all
Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: debhelper (>= 5.0.62), python, cdbs (>= 0.4.49), #{build_requirements}
Build-Depends-Indep: python-central (>= 0.5.6)
Standards-Version: 3.8.0
Homepage: #{homepage}
""", fields))

		for package in packages:
			# Make additions to fields
			fields = package.to_hash({
							'install_requirements' : ["${python:Depends}", "${misc:Depends}"] + package.install_requirements, 
							'short_description' : package.meta.short_description, 
							'long_description' : package.meta.long_description
			})

			# Make changes to fields
			if len(package.additional_description) > 0:
				fields['long_description'] += "\n\n" + package.additional_description
			fields['long_description'] = ' ' + fields['long_description'].replace("\n", "\n ").replace("\n \n", "\n .\n") 

			f.write(substitute_strings(
"""
Package: #{name}
Section: #{section}
Priority: #{priority}
Architecture: all
Depends: #{install_requirements}
XB-Python-Version: ${python:Versions}
Description: #{short_description}
#{long_description}
""", fields))

		f.close()

