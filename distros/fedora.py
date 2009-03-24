

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

		# FIXME:Determine the %files and %doc
		'''
		%files
		%defattr(-,root,root)
		%doc README COPYING ChangeLog doc examples LICENSE

		%{_mandir}/man1/%{name}.*
		%{_mandir}/man5/%{name}_config.*

		%{_bindir}/#{name}
		%{_infodir}/#{name}.info*

		%{python_sitelib}/*

		%{_datadir}/applications/%{name}.desktop
		%{_datadir}/icons/hicolor/*/*/%{name}*.png
		%{_datadir}/icons/hicolor/*/*/%{name}*.svg
		%{_datadir}/pixmaps/%{name}.png
		'''

		fields = None
		if package.build_method == 'c configure make':
			fields = self.generate_fedora_install_for_c_configure_make(f, package)
		elif package.build_method == 'pure python library':
			fields = self.generate_fedora_install_for_pure_python_library(f, package)
		elif package.build_method == 'pure python application':
			fields = self.generate_fedora_install_for_pure_python_library(f, package)

		f.close()

		# Create the rpm file
		print "Building the rpm package ..."

		print commands.getoutput("rpmbuild -ba ~/rpmbuild/SPECS/" + package.name + ".spec")

		print "Copying the rpm package to the packages directory ..."
		if not os.path.isdir("packages"): os.mkdir("packages")
		arch = fields['build_arch']
		rpm = package.name + "-" + package.version + "-1.fc10." + arch + ".rpm"
		commands.getoutput("cp ~/rpmbuild/RPMS/" + arch + "/" + rpm + " packages/" + rpm)
		print "Done"

	def generate_fedora_install_for_c_configure_make(self, f, package):
		# Make additions to fields
		fields = package.to_hash({
				'build_arch' : 'i386'
		})

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
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%find_lang #{name}


%check
cd tests
make check-TESTS


%clean
rm -rf $RPM_BUILD_ROOT


%post
#{after_install}


%preun
#{before_uninstall}


%files -f #{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_mandir}/man1/#{name}.1*
%{_bindir}/#{name}
%{_infodir}/#{name}.info*

%changelog
* #{human_timestring} #{packager_name} <#{packager_email}> - #{version}-1
- Initial package.
""", fields))

		return fields

	def generate_fedora_install_for_pure_python_library(self, f, package):
		# Make additions to fields
		fields = package.to_hash()
		fields = package.to_hash({
				'build_arch' : 'noarch', 
				'build_requirements' : ['python-devel'] + package.build_requirements, 
				'install_requirements' : ['python'] + package.install_requirements
		})

		f.write(substitute_strings(
"""%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           #{name}
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
%{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#{after_install}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc README COPYING ChangeLog
%doc README doc examples LICENSE
%{python_sitelib}/*

%changelog
* #{human_timestring} #{packager_name} <#{packager_email}> - #{version}-1
- Initial package.
""", fields))

		return fields

