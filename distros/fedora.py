

class Builder(object):
	def build(self, package):
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

		# Make additions to fields
		fields = package.to_hash()
		# FIXME: Here is where we would get all the fedora specific stuff into the fields

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
""", fields))

		f.close()

		# Create the rpm file
		print "Building the rpm package ..."

		commands.getoutput("rpmbuild -ba ~/rpmbuild/SPECS/" + package.name + ".spec")

		print "Copying the rpm package to the packages directory ..."
		if not os.path.isdir("packages"): os.mkdir("packages")
		arch = fields['build_arch']
		rpm = package.name + "-" + package.version + "-1.fc10." + arch + ".rpm"
		commands.getoutput("cp ~/rpmbuild/RPMS/" + arch + "/" + rpm + " packages/" + rpm)
		print "Done"

	# FIXME: Change this disaster to generate the prep to files section of the spec file
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

