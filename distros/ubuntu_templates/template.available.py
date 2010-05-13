<%doc> \
    This is a template dpkg available file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
% for package in packages:
Package: ${package.name}
Priority: ${package.priority}
Section: ${category_to_section[package.category]}
Installed-Size: ${str(package.custom['size'])}
Maintainer: ${packager_name} <${packager_email}>
Architecture: ${package_type_to_architecture[package.package_type]}
Version: ${changelog[0].version}-${changelog[0].release}
Depends: ${str.join(', ', package.install_requirements)}
Size: ${str(package.custom['size'])}
Description: ${short_description}
% if len(package.additional_description) == 0:
${' ' + long_description.replace("\n", "\n ").replace("\n \n", "\n .\n")}
% else:
${' ' + (long_description + '\n\n' + package.additional_description).replace("\n", "\n ").replace("\n \n", "\n .\n")}
% endif
Homepage: ${homepage}

% endfor
