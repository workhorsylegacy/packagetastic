

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

		# Uncompress the source code so we can examine it
		print "Uncompressing source code ..."
		if not os.path.isdir("builds"): os.mkdir("builds")
		commands.getoutput(substitute_strings("cp sources/#{name}-#{version}.tar.gz builds/#{name}_#{version}.orig.tar.gz", package.to_hash()))
		os.chdir("builds")
		commands.getoutput(substitute_strings("tar xzf #{name}_#{version}.orig.tar.gz", package.to_hash()))
		os.chdir(substitute_strings("#{name}-#{version}", package.to_hash()))

		# FIXME: Figure out how %defattr(-,root,root,-) works
		# Determine the params for %files
		params = {}
		params['docs'] = []
		for doc in ['README', 'COPYING', 'ChangeLog', 'LICENSE']:
			if os.path.isfile(doc):
				params['docs'].append(doc)

		for doc in ['doc', 'examples']:
			if os.path.isdir(doc):
				params['docs'].append(doc)

		if os.path.isfile('doc/' + package.name + '.1'):
			params['has_man1'] = True
		elif os.path.isfile('man/' + package.name + '.1'):
			params['has_man1'] = True
		else:
			params['has_man1'] = False

		if os.path.isfile('doc/' + package.name + '_config.5'):
			params['has_man5'] = True
		elif os.path.isfile('man/' + package.name + '_config.5'):
			params['has_man5'] = True
		else:
			params['has_man5'] = False

		params['has_bindir'] = False
		if package.build_method == 'c configure make':
			params['has_bindir'] = True
			params['import_sitelib'] = False
		elif package.build_method == 'pure python library':
			params['has_bindir'] = False
			params['import_sitelib'] = True
		elif package.build_method == 'pure python application':
			params['has_bindir'] = True
			params['import_sitelib'] = True

		params['has_info'] = os.path.isfile('doc/' + package.name + '.info')

		params['has_lang'] = os.path.isdir('po')

		params['has_desktop_file'] = os.path.isfile('data/' + package.name + '.desktop')

		params['has_icons'] = os.path.isdir('data/icons')

		# Create the spec file
		os.chdir('../..')
		print "Building the spec file ..."
		commands.getoutput('touch ~/rpmbuild/SPECS/' + package.name + '.spec')
		f = open(os.path.expanduser('~/rpmbuild/SPECS/') + package.name + '.spec', 'w')

		# Write the custom parts of the spec file
		fields = None
		if package.build_method == 'c configure make':
			fields = self.generate_fedora_install_for_c_configure_make(f, package, params)
		elif package.build_method == 'pure python library':
			fields = self.generate_fedora_install_for_pure_python_library(f, package, params)
		elif package.build_method == 'pure python application':
			fields = self.generate_fedora_install_for_pure_python_library(f, package, params)

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

	def generate_fedora_install_for_c_configure_make(self, f, package, params):
		# Make additions to fields
		fields = package.to_hash({
				'build_arch' : 'i386', 
				'files' : self.generate_file(package, params), 
				'pre_and_post' : self.generate_pre_and_post_functions(package, params), 
				'install' : self.generate_install_for_c_configure_make(package, params), 
				'install_extra' : self.generate_install_extras(package, params)
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


#{install}
#{install_extra}


%check
cd tests
make check-TESTS


%clean
rm -rf %{buildroot}


#{pre_and_post}


#{files}

%changelog
* #{human_timestring} #{packager_name} <#{packager_email}> - #{version}-1
- Initial package.
""", fields))

		return fields

	def generate_fedora_install_for_pure_python_library(self, f, package, params):
		# Make additions to fields
		fields = package.to_hash()
		fields = package.to_hash({
				'build_arch' : 'noarch', 
				'build_requirements' : ['python-devel'] + package.build_requirements, 
				'install_requirements' : ['python'] + package.install_requirements, 
				'files' : self.generate_file(package, params), 
				'pre_and_post' : self.generate_pre_and_post_functions(package, params), 
				'install' : self.generate_install_for_pure_python_library(package, params), 
				'install_extra' : self.generate_install_extras(package, params)
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


#{install}
#{install_extra}

#{after_install}

%clean
rm -rf %{buildroot}


#{pre_and_post}


#{files}

%changelog
* #{human_timestring} #{packager_name} <#{packager_email}> - #{version}-1
- Initial package.
""", fields))

		return fields

	def generate_pre_and_post_functions(self, package, params):
		pre, post, preun, postun = '', '', '', ''

		if params['has_info']:
			post += \
"""/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :
"""
			preun += \
"""if [ $1 = 0 ] ; then
  /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi
"""

		if params['has_icons'] == True:
			post += \
"""gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :
"""

			postun += \
"""gtk-update-icon-cache -qf %{_datadir}/icons/hicolor &>/dev/null || :
"""

		retval = ''
		for name, body in {'pre':pre, 'post':post, 'preun':preun, 'postun':postun}.iteritems():
			if len(body) > 0:
				retval += substitute_strings(
"""
%#{name}
#{body}
""", {'name' : name, 'body' : body})

		return retval


	def generate_file(self, package, params):
		fields = []
		lang = ''

		if params['has_lang']:
			lang = '-f %{name}.lang'

		if len(params['docs']) > 0:
			fields.append('%doc ' + str.join(' ', params['docs']))

		if params['has_man1'] == True:
			fields.append('%{_mandir}/man1/%{name}.1*')

		if params['has_man5'] == True:
			fields.append('%{_mandir}/man5/%{name}_config.5*')

		if params['has_bindir'] == True:
			fields.append('%{_bindir}/%{name}')

		if params['has_info'] == True:
			fields.append('%{_infodir}/%{name}.info*')

		if params['import_sitelib'] == True:
			fields.append('%{python_sitelib}/*')

		if params['has_desktop_file'] == True:
			fields.append('%{_datadir}/applications/%{name}.desktop')

		if params['has_icons'] == True:
			fields.append('%{_datadir}/icons/hicolor/*/*/%{name}*.png')
			fields.append('%{_datadir}/icons/hicolor/*/*/%{name}*.svg')
			fields.append('%{_datadir}/pixmaps/%{name}.png')

		return substitute_strings(
"""%files #{lang}
%defattr(-,root,root)
#{fields}
""", {
		'lang' : lang, 
		'fields' : str.join('\n', fields)
	})

	def generate_install_for_pure_python_library(self, package, params):
		return \
"""
%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
"""

	def generate_install_for_c_configure_make(self, package, params):
		return \
""" %install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir
"""

	def generate_install_extras(self, package, params):
		retval = ''

		if params['has_lang'] == True:
			retval += \
"""
%find_lang %{name}
"""

		if params['has_icons'] == True:
			retval += \
"""
rm -f %{buildroot}/%{_datadir}/icons/hicolor/icon-theme.cache
rm -f %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications data/%{name}.desktop
"""

		return retval


