<%doc> \
    This is a template dpkg changelog file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
% for item in changelog[:]:
<%
prev_version = item['version']
item_version = item['version']
item_time = item['time']
item_text = item['text']
%>\
${name} (${item_version}-1) unstable; urgency=low

  * ${item_text}

 -- ${packager_name} <${packager_email}>  ${item_time}
% endfor

