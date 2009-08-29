

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
		params = {}
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

		# Create the spec file
		os.chdir('../..')
		print "Building the spec file ..."
		# Write the custom parts of the spec file
		fields = None
		if meta.build_method == 'c application' or meta.build_method == 'c library':
			fields = self.generate_spec_file_for_c(meta, packages, params)
		elif meta.build_method == 'python library':
			fields = self.generate_spec_file_for_python_library(meta, packages, params)
		elif meta.build_method == 'python application':
			fields = self.generate_spec_file_for_python_library(meta, packages, params)
		else:
			print "Unknown build method '" + meta.build_method + "'. Exiting ..."
			exit()

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
		arch = fields['build_arch']
		rpm = meta.name + "-" + meta.version + "-" + str(meta.release) + ".fc11." + arch + ".rpm"
		commands.getoutput("cp ~/rpmbuild/RPMS/" + arch + "/" + rpm + " packages/" + rpm)
		print "Done"

	def generate_spec_file_for_c(self, meta, packages, params):
		# Make additions to fields
		fields = meta.to_hash({
				'build_arch' : 'i386', 
				'files' : self.generate_file(meta, params), 
				'pre_and_post' : self.generate_pre_and_post_functions(meta, params), 
				'install' : self.generate_install_for_c(meta, params), 
				'install_extra' : self.generate_install_extras(meta, params), 
				'changelog' : self.generate_changelog(meta), 
				'install_requirements' : meta.join(packages[0].install_requirements), 
				'group' : self.category_to_group[meta.category]
		})

		f = open(os.path.expanduser('~/rpmbuild/SPECS/') + meta.name + '.spec', 'w')
		f.write(substitute_strings(
"""Name:           #{name}
Version:        #{version}
Release:        #{release}%{?dist}
Summary:        #{short_description}
Group:          #{group}
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
#{changelog}
""", fields))
		f.close()

		return fields

	def generate_spec_file_for_python_library(self, meta, packages, params):
		# Make additions to fields
		fields = meta.to_hash({
				'build_arch' : 'noarch', 
				'build_requirements' : ['python-setuptools-devel'], 
				'files' : self.generate_file(meta, params), 
				'pre_and_post' : self.generate_pre_and_post_functions(meta, params), 
				'install' : self.generate_install_for_python_library(meta, params), 
				'install_extra' : self.generate_install_extras(meta, params), 
				'changelog' : self.generate_changelog(meta), 
				'install_requirements' : meta.join(packages[0].install_requirements + ['python']), 
				'group' : self.category_to_group[meta.category]
		})

		f = open(os.path.expanduser('~/rpmbuild/SPECS/') + meta.name + '.spec', 'w')
		f.write(substitute_strings(
"""%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}


Name:           #{name}
Version:        #{version}
Release:        #{release}%{?dist}
Summary:        #{short_description}
Group:          #{group}
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
#{changelog}
""", fields))
		f.close()

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


	def generate_file(self, meta, params):
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

	def generate_install_for_python_library(self, package, params):
		return \
"""%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
"""

	def generate_install_for_c(self, meta, params):
		return \
"""%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_infodir}/dir
"""

	def generate_install_extras(self, meta, params):
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

	def generate_changelog(self, meta):
		# FIXME: These should be at the top.
		from time import strftime
		from email.utils import parsedate

		# Create the changelog
		changelog_body = ""
		if meta.changelog == None:
			print "The changelog is missing. Exiting ..."
			exit()

		reverse_entries = meta.changelog[:]
		reverse_entries.reverse()
		for item in reverse_entries:
			item['time'] = time.strftime("%a %b %d %Y", parsedate(item['time']))

			fields = meta.to_hash({
					'item_version' : item['version'], 
					'item_time' : item['time'], 
					'item_text' : item['text']
			})

			entry = substitute_strings(
"""* #{item_time} - #{packager_email} - #{item_version}
- #{item_text}

""", fields)

			changelog_body = entry + changelog_body

		return changelog_body



