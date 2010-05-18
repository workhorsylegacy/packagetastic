<%doc> \
    This is a template dpkg available file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
Package: ${package.name}
Priority: ${package.priority}
Section: ${category_to_section[package.category]}
Installed-Size: ${str(package.custom['size'])}
Maintainer: ${packager_name} <${packager_email}>
Architecture: ${package_type_to_architecture[package.package_type]}
Source: ${name}
Version: ${changelog[0].version}-${changelog[0].release}
<%r = []%>\
Depends: \
% for requirement in package.install_requirements:
% if requirement['version']:
<% r.append(requirement['name'] + ' (' + requirement['compare'] + ' ' + requirement['version'] + ')') %>\
% else:
<% r.append(requirement['name']) %>\
% endif
% endfor
${str.join(', ', r)}
Size: ${str(package.custom['size'])}
Description: ${short_description}
% if len(package.additional_description) == 0:
${' ' + long_description.replace("\n", "\n ").replace("\n \n", "\n .\n")}
% else:
${' ' + (long_description + '\n\n' + package.additional_description).replace("\n", "\n ").replace("\n \n", "\n .\n")}
% endif
Homepage: ${homepage}

