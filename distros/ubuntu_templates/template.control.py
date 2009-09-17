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
% if uses_python:
XS-Python-Version: all
% endif
Maintainer: ${packager_name} <${packager_email}>
% if uses_python:
Build-Depends: debhelper (>= 5.0.62), python, ${str.join(', ', build_requirements)}
Build-Depends-Indep: python-support (>= 0.3)
% else:
Build-Depends: ${str.join(', ', build_requirements)}
% endif
Standards-Version: 3.8.0
Homepage: ${homepage}

% for package in packages:
Package: ${package.name}
Section: ${category_to_section[package.category]}
Priority: ${package.priority}
Architecture: ${build_method_to_architecture[package.build_method]}
Depends: ${str.join(', ', package.install_requirements + additional_install_requirements)}
% if uses_python:
XB-Python-Version: @@{python:Versions}
% endif
Description: ${short_description}
% if len(package.additional_description) == 0:
${' ' + long_description.replace("\n", "\n ").replace("\n \n", "\n .\n")}
% else:
${' ' + (long_description + '\n\n' + package.additional_description).replace("\n", "\n ").replace("\n \n", "\n .\n")}
% endif


% endfor
