<%doc> \
    This is a template dpkg changelog file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
% for item in changelog[:]:
${name} (${item.version}-${item.release}) unstable; urgency=low

  * ${item.text}

 -- ${packager_name} <${packager_email}>  ${item.time}
% endfor

