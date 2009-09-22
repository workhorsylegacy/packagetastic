<%doc> \
    This is a template rpm spec file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with % \
    \\\\ is replaced with \\n \
</%doc>\
% if uses_python:
@@{!?python_sitelib: @@global python_sitelib @@(@@{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

% endif
Name:           ${name}
Version:        ${version}
Release:        ${release}@@{?dist}
Summary:        ${short_description}
Group:          ${category_to_group[packages[0].category]}
License:        ${license}
URL:            ${homepage}
Source0:        ${source}
% if patches:
<%n = 1%>
% for patch in patches:
Patch${n}: ${patch}\
<%n += 1%>
% endfor
% endif
BuildRoot: @@{_tmppath}/@@{name}-@@{version}-@@{release}-root-@@(@@{__id_u} -n)
BuildArch: ${build_method_to_build_arch[packages[0].build_method]}

## Build Requirements
% for build_requirement in build_requirements:
BuildRequires: ${filter_requirement(build_requirement)}
% endfor
% for install_requirement in packages[0].install_requirements:
Requires: ${filter_requirement(install_requirement)}
% endfor
% for additional_install_requirement in additional_install_requirements:
Requires: ${filter_requirement(additional_install_requirement)}
% endfor


@@description
${long_description}

@@prep
@@setup -q
% if patches:
<%n = 1%>\
% for patch in patches:
@@patch${n} -p0\
<%n += 1%>
% endfor
% endif

@@build
% if uses_c:
@@configure
make @@{?_smp_mflags}
% elif uses_python:
@@{__python} setup.py build
% endif


@@install
rm -rf @@{buildroot}
% if uses_c:
make install DESTDIR=@@{buildroot}
rm -f @@{buildroot}@@{_infodir}/dir
% elif uses_python:
@@{__python} setup.py install -O1 --skip-build --root @@{buildroot}
% endif
% if has_icon_cache:
rm -f @@{buildroot}/@@{_datadir}/icons/hicolor/icon-theme.cache
% endif

% if has_desktop_file:
desktop-file-install --vendor=""                 \\\\
  --delete-original                              \\\\
  --dir=@@{buildroot}@@{_datadir}/applications     \\\\
  @@{buildroot}@@{_datadir}/${desktop_file_name}
% endif

% if has_lang:
@@find_lang @@{name}
% endif

#@@check
#cd tests
#make check-TESTS


@@clean
rm -rf @@{buildroot}

## Post install functions
@@post
% if has_info:
/sbin/install-info @@{_infodir}/@@{name}.info @@{_infodir}/dir || :
%endif
% if has_mime:
update-mime-database @@{_datadir}/mime &> /dev/null ||:
% endif
% if has_icons:
gtk-update-icon-cache -qf @@{_datadir}/icons/hicolor &>/dev/null || :
% endif

## Pre uninstall functions
@@preun
% if has_info:
if [ $1 = 0 ] ; then
  /sbin/install-info --delete @@{_infodir}/@@{name}.info @@{_infodir}/dir || :
fi
% endif


## Post uninstall functions
@@postun
% if has_icons:
gtk-update-icon-cache -qf @@{_datadir}/icons/hicolor &>/dev/null || :
% endif


## Files
% if has_lang:
@@files -f @@{name}.lang
% else:
@@files
% endif
@@defattr(-,root,root,-)
\
% if len(docs) > 0:
@@doc ${str.join(' ', docs)}
% endif

% if import_python_sitelib:
@@{python_sitelib}/*
% endif
% for entry in mandir_entries:
@@{_mandir}/${entry}
% endfor
% for entry in bindir_entries:
@@{_bindir}/${entry}
% endfor
% for entry in infodir_entries:
@@{_infodir}/${entry}
% endfor
% for entry in datadir_entries:
@@{_datadir}/${entry}
% endfor


## FIXME: These should not be here
<%
from time import strftime
from email.utils import parsedate
%>
@@changelog
% for item in changelog[:]:
<% vague_time = strftime("%a %b %d %Y", parsedate(item.time)) %>\
* ${vague_time} - ${packager_email} - ${item.version}
- ${item.text}

% endfor


