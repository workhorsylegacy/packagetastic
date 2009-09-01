<%doc> \
    This is a template dpkg blah.post file. It uses mako \
    for templating. Additional formatting is added to \
    escape symbols that will conflict with mako. After \
    mako is run, these symbols are replaced with others: \
    @@ is replaced with $ \
</%doc>\
#!/bin/sh

set -e

if [ "$1" = "configure" ] || [ "$1" = "abort-upgrade" ]; then
	update-alternatives --install /usr/bin/${alternate_name} ${alternate_name} /usr/bin/${name} 50 \\
	  --slave /usr/share/man/man1/${alternate_name}.1.gz ${alternate_name}.1.gz \\
	  /usr/share/man/man1/${name}.1.gz
fi

#DEBHELPER#
