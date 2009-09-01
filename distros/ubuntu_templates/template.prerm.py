<%doc> \
    This is a template dpkg blah.prerm file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
#!/bin/sh

set -e

if [ "$1" != "upgrade" ]; then
	update-alternatives --remove ${alternate_name} /usr/bin/${name}
fi

#DEBHELPER#
