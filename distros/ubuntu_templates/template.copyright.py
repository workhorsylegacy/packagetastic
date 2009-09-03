<%doc> \
    This is a template dpkg copyright file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
This package was debianized by ${packager_name} <${packager_email}> on 
${timestring}.

It was downloaded from ${homepage}

${('Upstream Authors', 'Upstream Author')[ len(authors) > 0 ]}:

    ${str.join("\n    ", authors)}

Copyright:

    Copyright (C) ${str.join("\n    ", copyright)}

License:

${"    " + license_text.replace("\n", "\n    ").rstrip()}

The Debian packaging is (C) ${year}, ${packager_name} <${packager_email}> and
is licensed under the ${license}, see above.
