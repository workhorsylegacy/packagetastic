<%doc> \
    This is a template rpm spec file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with % \
</%doc>\
Name:           ${name}
Version:        ${version}
Release:        ${release}@@{?dist}
Summary:        ${short_description}
Group:          ${group}
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
BuildRequires: ${build_requirement}
% endfor
% for install_requirement in install_requirements:
Requires: ${install_requirement}
% endfor
BuildArch: ${build_arch}


@@description
${long_description}

@@prep
@@setup -q


@@build
% if build_method == 'c application' or build_method == 'c library':
@@configure
make @@{?_smp_mflags}
% elif build_method == 'python application' or build_method == 'python library':
@@{__python} setup.py build
% endif


@@install
rm -rf @@{buildroot}
% if build_method == 'c application' or build_method == 'c library':
make install DESTDIR=@@{buildroot}
rm -f @@{buildroot}@@{_infodir}/dir
% elif build_method == 'python application' or build_method == 'python library':
@@{__python} setup.py install -O1 --skip-build --root @@{buildroot}
% endif


@@check
cd tests
make check-TESTS


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
% endif
@@defattr(-,root,root)
\
% if len(docs) > 0:
@@doc ${str.join(', ', docs)}
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
% if import_sitelib == True:
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
% if has_lang == True:
@@find_lang @@{name}
% endif

## FIXME: These should not be here
<%
from time import strftime
from email.utils import parsedate
%>
@@changelog
% for item in changelog[:]:
<% vague_time = strftime("%a %b %d %Y", parsedate(item.time)) %> \
* ${vague_time} - ${packager_email} - ${item.version}
- ${item.text}

% endfor


