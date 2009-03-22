#!/usr/bin/env python

import os, time, re
import commands
import pexpect
import base64


licenses = { 'GPL2+' : \
"""    This package is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This package is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this package; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

On Debian systems, the complete text of the GNU General
Public License can be found in `/usr/share/common-licenses/GPL'."""
,
'MIT' : \
"""
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
}

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

class BasePackage(object):
	# FIXME: This should be just a constructor that is called when children are __init__()
	def call_parent_constructor(self):
		self._name = None
		self._version = None
		self._section = None
		self._priority = None
		self._authors = []
		self._copyright = []
		self._packager_name = None
		self._packager_email = None
		self._bug_mail = None
		self._homepage = None
		self._license = None
		self._source = None
		self._build_method = None
		self._build_requirements = []
		self._install_requirements = []
		self._short_description = None
		self._long_description = None

	def get_name(self): return self._name
	def set_name(self, value): self._name = value
	name = property(get_name, set_name)

	def get_version(self): return self._version
	def set_version(self, value): self._version = value
	version = property(get_version, set_version)

	def get_section(self): return self._section
	def set_section(self, value): self._section = value
	section = property(get_section, set_section)

	def get_priority(self): return self._priority
	def set_priority(self, value): self._priority = value
	priority = property(get_priority, set_priority)

	def get_authors(self): return self._authors
	def set_authors(self, value): self._authors = value
	authors = property(get_authors, set_authors)

	def get_copyright(self): return self._copyright
	def set_copyright(self, value): self._copyright = value
	copyright = property(get_copyright, set_copyright)

	def get_packager_name(self): return self._packager_name
	def set_packager_name(self, value): self._packager_name = value
	packager_name = property(get_packager_name, set_packager_name)

	def get_packager_email(self): return self._packager_email
	def set_packager_email(self, value): self._packager_email = value
	packager_email = property(get_packager_email, set_packager_email)

	def get_bug_mail(self): return self._bug_mail
	def set_bug_mail(self, value): self._bug_mail = value
	bug_mail = property(get_bug_mail, set_bug_mail)

	def get_homepage(self): return self._homepage
	def set_homepage(self, value): self._homepage = value
	homepage = property(get_homepage, set_homepage)

	def get_license(self): return self._license
	def set_license(self, value): self._license = value
	license = property(get_license, set_license)

	def get_source(self): return self._source
	def set_source(self, value): self._source = value
	source = property(get_source, set_source)

	def get_build_method(self): return self._build_method
	def set_build_method(self, value): self._build_method = value
	build_method = property(get_build_method, set_build_method)

	def get_build_requirements(self): return self._build_requirements
	def set_build_requirements(self, value): self._build_requirements = value
	build_requirements = property(get_build_requirements, set_build_requirements)

	def get_install_requirements(self): return self._install_requirements
	def set_install_requirements(self, value): self._install_requirements = value
	install_requirements = property(get_install_requirements, set_install_requirements)

	def get_short_description(self): return self._short_description
	def set_short_description(self, value): self._short_description = value
	short_description = property(get_short_description, set_short_description)

	def get_long_description(self): return self._long_description
	def set_long_description(self, value): self._long_description = value
	long_description = property(get_long_description, set_long_description)

	def after_install(self): pass
	def before_install(self): pass
	def after_uninstall(self): pass
	def before_uninstall(self): pass

	def add_to_info(self):
		return \
"""/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :"""

	def delete_from_info(self):
		return \
"""if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi"""

	def to_hash(self, style, additional_fields=None):
		retval={ 'name' : self.name, 
				'version' : self.version, 
				'section' : self.section, 
				'priority' : self.priority, 
				'authors' : self.authors, 
				'copyright' : self.copyright, 
				'packager_name' : self.packager_name, 
				'packager_email' : self.packager_email, 
				'bug_mail' : self.bug_mail,
				'homepage' : self.homepage, 
				'license' : self.license, 
				'source' : self.source, 
				'build_method' : self.build_method, 
				'build_requirements' : self.build_requirements, 
				'install_requirements' : self.install_requirements, 
				'short_description' : self.short_description, 
				'long_description' : self.long_description, 
				'after_install' : self.after_install(), 
				'before_install' : self.before_install(), 
				'after_uninstall' : self.after_uninstall(), 
				'before_uninstall' : self.before_uninstall()
				}

		# Add custom data
		if additional_fields != None:
			retval.update(additional_fields)

		# Make changes that are distro and build method specific
		if style == 'debian':
			retval = self.__filter_hash_for_debian(retval)
		elif style == 'fedora':
			retval = self.__filter_hash_for_fedora(retval)
		else:
			raise Exception("The hash style of '" + str(style) + "' is unknown.")

		# Make changes that make data easier to use
		retval['authors'] = str.join("\n    ", retval['authors'])
		retval['copyright'] = str.join("\n    ", retval['copyright'])
		retval['build_requirements'] = str.join(', ', retval['build_requirements'])
		retval['install_requirements'] = str.join(', ', retval['install_requirements'])
		retval['year'] = time.strftime("%Y", time.localtime())
		retval['timestring'] = time.strftime("%a, %d %b %Y %H:%M:%S %z", time.localtime())
		retval['human_timestring'] = time.strftime("%a %b %d %Y", time.localtime())
		retval['license_text'] = licenses[self.license]
		retval['upstream_authors'] = ('Upstream Authors', 'Upstream Author')[ len(self.authors) > 0 ]

		return retval

	def __filter_hash_for_fedora(self, retval):
		if self._build_method == 'c configure make':

			retval['build_arch'] = 'i386'
			retval['build'] = \
"""%configure
make %{?_smp_mflags}"""

			retval['check'] = \
"""cd tests
make check-TESTS"""

			retval['install'] = substitute_strings(
"""rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%find_lang #{name}""", retval)

			retval['files'] = substitute_strings(
"""-f #{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_mandir}/man1/#{name}.1*
%{_bindir}/#{name}
%{_infodir}/#{name}.info*""", retval)

		elif self._build_method == 'pure python library':

			retval['build_requirements'].append('python-devel').append('python-central (>= 0.5.6)')
			retval['install_requirements'].append('python')
			retval['build_arch'] = 'noarch'
			retval['build'] = "%{__python} setup.py build"
			retval['check'] = ''

			retval['install'] = substitute_strings(
"""rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


# Correct some permissions
find examples -type f -exec chmod a-x \{\} \;
chmod 755 $RPM_BUILD_ROOT%{python_sitelib}/FSM.py""", retval)
			# FIXME: This chmod should be a generic command that is part of the build

			retval['files'] = substitute_strings(
"""
%defattr(-,root,root)
%doc README doc examples LICENSE
%{python_sitelib}/*""", retval)

		return retval

	def __filter_hash_for_debian(self, retval):
		retval['long_description'] = " " + retval['long_description'].replace("\n", "\n ").replace("\n \n", "\n .\n")
		retval['build_requirements'] = retval['build_requirements'] + ["debhelper (>= 7)", "autotools-dev"]

		if self.build_method == 'c configure make':
			retval['install_requirements'] = retval['install_requirements'] + ["${shlibs:Depends}", "${misc:Depends}"]
		elif self.build_method == 'pure python application':
			retval['install_requirements'] = retval['install_requirements'] + ["${python:Depends}"]

		return retval

def build_ubuntu(package):
	# Get the root password
	root_password = 'xxx'

	# Get the signature
	signature_key = 'xxx'

	# clear sudo so we don't use it till needed
	commands.getoutput("sudo -k")

	# Uncompress the source code
	print "uncompressing source code ..."
	if not os.path.isdir("builds"): os.mkdir("builds")
	commands.getoutput(substitute_strings("cp sources/#{name}-#{version}.tar.gz builds/#{name}_#{version}.orig.tar.gz", package.to_hash('debian')))
	os.chdir("builds")
	commands.getoutput(substitute_strings("tar xzf #{name}_#{version}.orig.tar.gz", package.to_hash('debian')))
	os.chdir(substitute_strings("#{name}-#{version}", package.to_hash('debian')))
	if not os.path.isdir("debian"): os.mkdir("debian")
	os.chdir("debian")


	# Generate the rules file
	print "Generating rules file ..."
	if package.build_method == 'c configure make':
		generate_debian_rules_for_c_configure_make(package)
	elif package.build_method == 'pure python application':
		generate_debian_rules_for_pure_python_application(package)


	# Create the compat file
	print "Generating compat file ..."
	f = open('compat', 'w')
	f.write('7')
	f.close()


	# Create the control file
	print "Generating control file ..."
	if package.build_method == 'c configure make':
		generate_debian_control_for_c_configure_make(package)
	elif package.build_method == 'pure python application':
		generate_debian_control_for_pure_python_application(package)


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
""", package.to_hash('debian')))

	f.close()


	# Get the mangled gibberish that is on the end of a package file name
	mangle = "-1"

	# Create the changelog
	f = open('changelog', 'w')
	f.write(substitute_strings(
"""#{name} (#{version}#{mangle}) intrepid; urgency=low

  * Initial release

 -- #{packager_name} <#{packager_email}>  #{timestring}

""", package.to_hash('debian', {'mangle' : mangle})))

	f.close()

	# Run debuild
	print "Running debuild ..."
	os.chdir("..")

	command = 'bash -c "debuild -S -sa"'
	child = pexpect.spawn(command, timeout=1200)

	expected_lines = ["dpkg-buildpackage -rfakeroot -d -us -uc -S -sa\r\n",
						"dpkg-buildpackage: set CFLAGS to default value: -g -O2\r\n",
						"dpkg-buildpackage: set CPPFLAGS to default value:\r\n",
						"dpkg-buildpackage: set LDFLAGS to default value: -Wl,-Bsymbolic-functions\r\n",
						"dpkg-buildpackage: set FFLAGS to default value: -g -O2\r\n",
						"dpkg-buildpackage: set CXXFLAGS to default value: -g -O2\r\n",
						"dpkg-buildpackage: source package " + package.name + "\r\n",
						"dpkg-buildpackage: source version " + package.version + "" + mangle + "\r\n",
						"dpkg-buildpackage: source changed by " + package.packager_name + " <" + package.packager_email + ">" + "\r\n",
						"fakeroot debian/rules clean",
						"dh_testdir",
						"dh_testroot",
						"rm -f build-stamp",
						"rm -f config.sub config.guess",
						"dh_clean",
						"dpkg-source -b " + package.name + "-" + package.version,
						"dpkg-source: info: using source format `1.0'",
						"dpkg-source: info: building " + package.name + " using existing " + package.name + "_" + package.version + ".orig.tar.gz",
						"dpkg-source: info: building " + package.name + " in " + package.name + "_" + package.version + "" + mangle + ".diff.gz",
						"dpkg-source: info: building " + package.name + " in " + package.name + "_" + package.version + "" + mangle + ".dsc",
						"dpkg-genchanges: including full source code in upload",
						"dpkg-buildpackage: source only upload (original source is included)",
						"Now running lintian...",
						"Finished running lintian.",
						"Now signing changes and any dsc files...",
						"dpkg-source: error:",
						"dpkg-buildpackage: failure:",

						"You need a passphrase to unlock the secret key for\r\n" +
						"user: \"" + package.packager_name + " <" + package.packager_email + ">" + "\"\r\n" +
						"1024-bit DSA key, ID [\w]*, created \d*-\d*-\d*\r\n" +
						"\r\n" +
						"Enter passphrase: [\w|\s\W]*",

						"gpg: Invalid passphrase; please try again ...",

						"dpkg-source: error: syntax error in " + package.packager_name + "-" + package.version + "/debian/control at line \d*: ",

						"dpkg-buildpackage: failure: fakeroot debian/rules clean gave error exit status 2", 

						"Successfully signed dsc and changes files\r\n",
						pexpect.EOF]

	still_reading = True
	while still_reading:
		result = child.expect(expected_lines)

		if result >= 0 and result <= 26:
			pass
		elif result == 27:
			child.sendline(signature_key)
		elif result == 28:
			print "Invalid signing key. Exiting ..."
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
		elif result == len(expected_lines)-1:
			still_reading = False

	child.close()


	# Run pbuilder
	print "Running pbuilder ..."
	os.chdir("..")

	command = 'bash -c "sudo pbuilder build ' + package.name + '_' + package.version + mangle + '.dsc"'
	child = pexpect.spawn(command, timeout=1200)

	expected_lines = ["\[sudo\] password for [\w|\s]*: ",

						"Sorry, try again.\r\n" +
						"[sudo] password for [\w|\s]*: ",

						pexpect.EOF]

	still_reading = True
	while still_reading:
		result = child.expect(expected_lines)

		if result == 0:
			child.sendline(root_password)
		elif result == 1:
			print "Incorrect password for sudo. Exiting ..."
			exit()
		elif result == len(expected_lines)-1:
			still_reading = False

	child.close()

	# Copy the deb from the cache
	print "Getting deb file ..."
	os.chdir('..')
	if not os.path.isdir("packages"): os.mkdir("packages")
	command = "cp /var/cache/pbuilder/result/" + package.name + "_" + package.version + mangle + "_i386.deb packages/" + package.name + "_" + package.version + mangle + "_i386.deb"

	print "Done"

def generate_debian_rules_for_c_configure_make(package):

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
	dh_clean -k 
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
""", package.to_hash('debian')))

	f.close()

def generate_debian_rules_for_pure_python_application(package):

	f = open('rules', 'w')
	f.write(substitute_strings(
"""#!/usr/bin/make -f
# -*- makefile -*-
DEB_PYTHON_SYSTEM = pycentral

include /usr/share/cdbs/1/rules/debhelper.mk
include /usr/share/cdbs/1/class/python-distutils.mk
include /usr/share/cdbs/1/rules/simple-patchsys.mk

DEB_INSTALL_CHANGELOGS_ALL := ChangeLog

binary-install/#{name}::
	dh_icons -p#{name}

clean::
	rm -rf build/
""", package.to_hash('debian')))

	f.close()

def generate_debian_control_for_c_configure_make(package):
	f = open('control', 'w')

	f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
Priority: #{priority}
Maintainer: Ubuntu MOTU Developers <ubuntu-motu@lists.ubuntu.com>
XSBC-Original-Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: #{build_requirements}
Bugs: mailto:#{bug_mail}
Standards-Version: 3.8.0
Homepage: #{homepage}

Package: #{name}
Architecture: any
Depends: #{install_requirements}
Description: #{short_description}
#{long_description}
""", package.to_hash('debian')))

	f.close()


def generate_debian_control_for_pure_python_application(package):
	f = open('control', 'w')

	f.write(substitute_strings(
"""Source: #{name}
Section: #{section}
XS-Python-Version: all
Priority: #{priority}
Maintainer: Ubuntu MOTU Developers <ubuntu-motu@lists.ubuntu.com>
XSBC-Original-Maintainer: #{packager_name} <#{packager_email}>
Build-Depends: debhelper (>= 5.0.62), python, cdbs (>= 0.4.49), #{build_requirements}
Build-Depends-Indep: python-central (>= 0.5.6)
Bugs: mailto:#{bug_mail}
Standards-Version: 3.8.0
Homepage: #{homepage}

Package: #{name}
Architecture: all
Depends: #{install_requirements}
Description: #{short_description}
#{long_description}
""", package.to_hash('debian')))

	f.close()


def build_fedora(package):
	# clear sudo so we don't use it till needed
	commands.getoutput("sudo -k")

	# Setup the directories
	print "Setting up the rpmdev directories ..."
	commands.getoutput('rm -rf ~/rpmbuild')
	commands.getoutput('rpmdev-setuptree')

	# Copy the source code to the build tree
	print "Copying the source code ..."
	commands.getoutput('cp sources/' + package.source.split('/')[-1] + ' ~/rpmbuild/SOURCES/' + package.source.split('/')[-1])

	# Create the spec file
	print "Building the spec file ..."
	commands.getoutput('touch ~/rpmbuild/SPECS/' + package.name + '.spec')
	f = open(os.path.expanduser('~/rpmbuild/SPECS/') + package.name + '.spec', 'w')

	if package.build_method == 'pure python library':
		f.write("%{!?python_sitelib: %define python_sitelib %(%{__python} -c " + \
				"\"from distutils.sysconfig import get_python_lib; print get_python_lib()\")}\n\n")

	f.write(substitute_strings(
"""Name:           #{name}
Version:        #{version}
Release:        1%{?dist}
Summary:        #{short_description}
Group:          Development/Tools
License:        #{license}
URL:            #{homepage}
Source:         #{source}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


BuildRequires: #{build_requirements}
Requires: #{install_requirements}
BuildArch: #{build_arch}


%description
#{long_description}


%prep
%setup -q


%build
#{build}


%install
#{install}


%check
#{check}


%clean
rm -rf $RPM_BUILD_ROOT


%post
#{after_install}


%preun
#{before_uninstall}


%files #{files}


%changelog
* #{human_timestring} #{packager_name} <#{packager_email}> - #{version}-1
- Initial package.
""", package.to_hash('fedora')))

	f.close()

	# Create the rpm file
	print "Building the rpm package ..."

	commands.getoutput("rpmbuild -ba ~/rpmbuild/SPECS/" + package.name + ".spec")

	print "Copying the rpm package to the packages directory ..."
	if not os.path.isdir("packages"): os.mkdir("packages")
	arch = package.to_hash('fedora')['build_arch']
	rpm = package.name + "-" + package.version + "-1.fc10." + arch + ".rpm"
	commands.getoutput("cp ~/rpmbuild/RPMS/" + arch + "/" + rpm + " packages/" + rpm)
	print "Done"






