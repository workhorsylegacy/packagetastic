<%doc> \
    This is a template dpkg control file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
Source: ${name}
Section: ${category_to_section[category]}
Priority: ${priority}
% if build_method == 'python application' or build_method == 'python library':
XS-Python-Version: all
% endif
Maintainer: ${packager_name} <${packager_email}>
% if build_method == 'python application' or build_method == 'python library':
Build-Depends: debhelper (>= 5.0.62), python, cdbs (>= 0.4.49), ${str.join(', ', build_requirements)}
Build-Depends-Indep: python-central (>= 0.5.6)
% else:
Build-Depends: ${str.join(', ', build_requirements)}
% endif
Standards-Version: 3.8.0
Homepage: ${homepage}

% for package in packages:
Package: ${package.name}
Section: ${category_to_section[package.category]}
Priority: ${package.priority}
Architecture: ${build_arch}
Depends: ${str.join(', ', package.install_requirements + additional_install_requirements)}
% if build_method == 'python application' or build_method == 'python library':
XB-Python-Version: @@{python:Versions}
% endif
Description: ${short_description}
${' ' + long_description.replace("\n", "\n ").replace("\n \n", "\n .\n")}

% endfor
