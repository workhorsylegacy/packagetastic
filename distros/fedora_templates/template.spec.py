<%doc> \
    This is a template rpm spec file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with % \
</%doc>\
% if uses_python:
@@{!?python_sitelib: @@define python_sitelib @@(@@{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

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
<%n = 0%>
% for patch in patches:
Patch${n}: ${patch} \
<%n += 1%>
% endfor
% endif
BuildRoot:      @@{_tmppath}/@@{name}-@@{version}-@@{release}-root-@@(@@{__id_u} -n)

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

% if has_lang == True:
@@find_lang @@{name}
% endif

#@@check
#cd tests
#make check-TESTS


@@clean
rm -rf @@{buildroot}

## Pre and Post functions
% if has_info:
@@post
/sbin/install-info @@{_infodir}/@@{name}.info @@{_infodir}/dir || :

@@preun
if [ $1 = 0 ] ; then
  /sbin/install-info --delete @@{_infodir}/@@{name}.info @@{_infodir}/dir || :
fi
% endif


% if has_icons:
@@post
gtk-update-icon-cache -qf @@{_datadir}/icons/hicolor &>/dev/null || :

@@postun
gtk-update-icon-cache -qf @@{_datadir}/icons/hicolor &>/dev/null || :
% endif


## Files
% if has_lang:
@@files -f @@{name}.lang
% else:
@@files
% endif
@@defattr(-,root,root)
\
% if len(docs) > 0:
@@doc ${str.join(' ', docs)}
% endif
% if has_man1 == True:
@@{_mandir}/man1/@@{name}.1*
% endif
% if has_man5 == True:
@@{_mandir}/man5/@@{name}_config.5*
% endif
% if has_bindir == True:
@@{_bindir}/@@{name}
% endif
% if has_info == True:
@@{_infodir}/@@{name}.info*
% endif
% if import_python_sitelib == True:
@@{python_sitelib}/*
% endif
% if has_desktop_file == True:
@@{_datadir}/applications/@@{name}.desktop
% endif
% if has_icons == True:
@@{_datadir}/icons/hicolor/*/*/@@{name}*.png
@@{_datadir}/icons/hicolor/*/*/@@{name}*.svg
@@{_datadir}/pixmaps/@@{name}.png
% endif

% if has_icons == True:
rm -f @@{buildroot}/@@{_datadir}/icons/hicolor/icon-theme.cache
rm -f @@{buildroot}/@@{_datadir}/applications/@@{name}.desktop
desktop-file-install --dir=@@{buildroot}@@{_datadir}/applications data/@@{name}.desktop
% endif

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


