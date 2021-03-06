#!/usr/bin/env python
# -*- coding: UTF-8 -*-

package_names = {
	'yelp' : { 
		'fedora' : [], 
		'ubuntu' : ['yelp']
	},
	'python-pkg-resources' : { 
		'fedora' : [], 
		'ubuntu' : ['python-pkg-resources']
	},
	'unzip' : { 
		'fedora' : [], 
		'ubuntu' : ['unzip']
	},
	'python-indicate' : { 
		'fedora' : [], 
		'ubuntu' : ['python-indicate']
	},
	'python-pycurl' : { 
		'fedora' : [], 
		'ubuntu' : ['python-pycurl']
	},
	'python-desktopcouch-records' : { 
		'fedora' : [], 
		'ubuntu' : ['python-desktopcouch-records']
	},
	'python-wnck' : { 
		'fedora' : [], 
		'ubuntu' : ['python-wnck']
	},
	'python-gtkspell' : { 
		'fedora' : [], 
		'ubuntu' : ['python-gtkspell']
	},
	'dbus-x11' : { 
		'fedora' : [], 
		'ubuntu' : ['dbus-x11']
	},
	'python-mygpoclient' : { 
		'fedora' : [], 
		'ubuntu' : ['python-mygpoclient']
	},
	'hicolor-icon-theme' : { 
		'fedora' : [], 
		'ubuntu' : ['hicolor-icon-theme']
	},
	'python-support' : { 
		'fedora' : [], 
		'ubuntu' : ['python-support']
	},
	'docbook-utils' : { 
		'fedora' : [], 
		'ubuntu' : ['docbook-utils']
	},
	'libxtst-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libxtst-dev']
	},
	'libgudev-1.0-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libgudev-1.0-dev']
	},
	'gnome-pkg-tools' : { 
		'fedora' : [], 
		'ubuntu' : ['gnome-pkg-tools']
	},
	'libpango1.0-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libpango1.0-dev']
	},
	'librsvg2-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['librsvg2-dev']
	},
	'libgnome-desktop-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libgnome-desktop-dev']
	},
	'libcanberra-gtk-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libcanberra-gtk-dev']
	},
	'libgconf2-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libgconf2-dev']
	},
	'libcairo2-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libcairo2-dev']
	},
	'libdbus-1-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libdbus-1-dev']
	},
	'seahorse' : { 
		'fedora' : [], 
		'ubuntu' : ['seahorse']
	},
	'python-gtksourceview2' : { 
		'fedora' : [], 
		'ubuntu' : ['python-gtksourceview2']
	},
	'python-gnomekeyring' : { 
		'fedora' : [], 
		'ubuntu' : ['python-gnomekeyring']
	},
	'bzr-dbus' : { 
		'fedora' : [], 
		'ubuntu' : ['bzr-dbus']
	},
	'python-nautilus' : { 
		'fedora' : [], 
		'ubuntu' : ['python-nautilus']
	},
	'bzr-stats' : { 
		'fedora' : [], 
		'ubuntu' : ['bzr-stats']
	},
	'bzr' : { 
		'fedora' : [], 
		'ubuntu' : ['bzr']
	},
	'nautilus-bzr' : { 
		'fedora' : [], 
		'ubuntu' : ['nautilus-bzr']
	},
	'bzr-gtk' : { 
		'fedora' : [], 
		'ubuntu' : ['bzr-gtk']
	}, 
	'libkarma-cil' : { 
		'fedora' : [], 
		'ubuntu' : ['libkarma-cil']
	}, 
	'libkarma-cil-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libkarma-cil-dev']
	}, 
	'libwebkit-cil-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libwebkit-cil-dev']
	}, 
	'libgdata-cil-dev' : { 
		'fedora' : [], 
		'ubuntu' : ['libgdata-cil-dev']
	}, 
	'gstreamer0.10-alsa' : { 
		'fedora' : [], 
		'ubuntu' : ['gstreamer0.10-alsa']
	}, 
	#'gstreamer0.10-gnomevfs' : { 
	#	'fedora' : [], 
	#	'ubuntu' : ['gstreamer0.10-gnomevfs']
	#}, 
	'autotools-dev' : {
		'fedora' : ['autotools-dev'], 
		'ubuntu' : ['autotools-dev']
	},
	'cheese' : {
		'fedora' : ['cheese'], 
		'ubuntu' : ['cheese']
	},
	'cheese-common' : {
		'fedora' : ['cheese-common'], 
		'ubuntu' : ['cheese-common']
	},
	'libcheese-gtk' : {
		'fedora' : ['libcheese-gtk'], 
		'ubuntu' : ['libcheese-gtk18']
	},
	'libcheese-gtk-dev' : {
		'fedora' : ['libcheese-gtk-dev'], 
		'ubuntu' : ['libcheese-gtk-dev']
	},
	'lxdream' : {
		'fedora' : ['lxdream'], 
		'ubuntu' : ['lxdream']
	}, 
	'ldc' : {
		'fedora' : ['ldc'], 
		'ubuntu' : ['ldc']
	}, 
	'libtango-ldc-dev' : {
		'fedora' : ['libtango-ldc-dev'], 
		'ubuntu' : ['libtango-ldc-dev']
	}, 
	'mysql-client' : {
		'fedora' : ['mysql-client'], 
		'ubuntu' : ['mysql-client']
	}, 
	'mysql-server' : {
		'fedora' : ['mysql-server'], 
		'ubuntu' : ['mysql-server']
	}, 
	'libmysqlclient15-dev' : {
		'fedora' : ['libmysqlclient15-dev'], 
		'ubuntu' : ['libmysqlclient15-dev']
	}, 
	'python-mysqldb' : {
		'fedora' : ['python-mysqldb'], 
		'ubuntu' : ['python-mysqldb']
	}, 
	'python-mako' : {
		'fedora' : ['python-mako'], 
		'ubuntu' : ['python-mako']
	}, 
	'build-essential' : {
		'fedora' : [''], 
		'ubuntu' : ['build-essential']
	}, 
	'rootintootin' : {
		'fedora' : ['rootintootin'], 
		'ubuntu' : ['rootintootin']
	}, 
	'meld' : { 
		'fedora' : ['meld'], 
		'ubuntu' : ['meld']
	}, 
	'pkgconfig' : { 
		'fedora' : ['pkgconfig'], 
		'ubuntu' : ['pkg-config']
	}, 
	'subtitleripper' : { 
		'fedora' : ['subtitleripper'], 
		'ubuntu' : ['subtitleripper']
	}, 
	'theora-tools' : { 
		'fedora' : ['theora-tools'], 
		'ubuntu' : ['libogg0', 'libtheora0', 'libvorbis0a', 'libpng12-0', 'libsdl1.2debian', 'libglib2.0-0']
	}, 
	'autoconf' : { 
		'fedora' : ['autoconf'], 
		'ubuntu' : ['autoconf']
	}, 
	'libtiff-dev' : { 
		'fedora' : ['libtiff-devel'], 
		'ubuntu' : ['libtiff4-dev']
	}, 
	'libtiff' : { 
		'fedora' : ['libtiff'], 
		'ubuntu' : ['libtiff4']
	}, 
	'enca' : { 
		'fedora' : ['enca'], 
		'ubuntu' : ['enca', 'libenca0']
	}, 
	'enca-dev' : { 
		'fedora' : ['enca-devel'], 
		'ubuntu' : ['enca', 'libenca-dev']
	}, 
	'avahi-daemon' : { 
		'fedora' : ['avahi'], 
		'ubuntu' : ['avahi-daemon']
	}, 
	'brasero' : { 
		'fedora' : ['brasero'], 
		'ubuntu' : ['brasero']
	}, 
	'podsleuth' : { 
		'fedora' : ['podsleuth-devel'], 
		'ubuntu' : ['podsleuth']
	}, 
	'hal' : { 
		'fedora' : ['hal', 'hal-devel'], 
		'ubuntu' : ['hal']
	}, 
	'libhal-dev' : { 
		'fedora' : ['hal-libs'], 
		'ubuntu' : ['libhal1', 'libhal-dev']
	}, 
	'gparted' : {
		'fedora' : ['gparted'],
		'ubuntu' : ['gparted']
	}, 
	'parted' : {
		'fedora' : ['parted'],
		'ubuntu' : ['parted']
	}, 
	'pkg-config' : {
		'fedora' : ['pkg-config'],
		'ubuntu' : ['pkg-config']
	}, 
	'libgtkmm-2.4-dev' : {
		'fedora' : ['libgtkmm-2.4-dev'],
		'ubuntu' : ['libgtkmm-2.4-dev']
	}, 
	'libparted0-dev' : {
		'fedora' : ['libparted0-dev'],
		'ubuntu' : ['libparted0-dev']
	}, 
	'rarian-compat' : {
		'fedora' : ['rarian-compat'],
		'ubuntu' : ['rarian-compat']
	}, 
	'gstreamer0.10-ffmpeg' : { 
		'fedora' : ['gstreamer-ffmpeg'], 
		'ubuntu' : ['gstreamer0.10-ffmpeg']
	}, 
	'gstreamer0.10-plugins-ugly' : { 
		'fedora' : ['gstreamer-plugins-ugly'], 
		'ubuntu' : ['gstreamer0.10-plugins-ugly']
	}, 
	'gstreamer0.10-plugins-bad' : { 
		'fedora' : ['gstreamer-plugins-bad'], 
		'ubuntu' : ['gstreamer0.10-plugins-bad']
	}, 
	'gstreamer0.10-plugins-good' : { 
		'fedora' : ['gstreamer-plugins-good'], 
		'ubuntu' : ['gstreamer0.10-plugins-good']
	}, 
	'gstreamer0.10-plugins-base' : { 
		'fedora' : ['gstreamer-plugins-base'], 
		'ubuntu' : ['gstreamer0.10-plugins-base']
	}, 
	'libgstreamer-plugins-base0.10-dev' : { 
		'fedora' : ['gstreamer-plugins-base-devel'], 
		'ubuntu' : ['libgstreamer-plugins-base0.10-dev']
	}, 
	'libgstreamer0.10-dev' : { 
		'fedora' : ['gstreamer-devel'], 
		'ubuntu' : ['libgstreamer0.10-dev']
	}, 
	'libgnomevfs2-dev' : { 
		'fedora' : ['gnome-vfs2-devel'], 
		'ubuntu' : ['libgnomevfs2-dev']
	}, 
	'libxxf86vm-dev' : { 
		'fedora' : ['libXxf86vm-devel'], 
		'ubuntu' : ['libxxf86vm-dev']
	}, 
	'libxrandr-dev' : { 
		'fedora' : ['libXrandr-devel'], 
		'ubuntu' : ['libxrandr-dev']
	}, 
	'libx11-dev' : { 
		'fedora' : ['libX11-devel'], 
		'ubuntu' : ['libx11-dev']
	}, 
	'libgtk2.0-dev' : { 
		'fedora' : ['gtk2-devel'], 
		'ubuntu' : ['libgtk2.0-dev']
	}, 
	'python-gtk2-dev' : { 
		'fedora' : ['pygtk2-devel'], 
		'ubuntu' : ['python-gtk2-dev']
	}, 
	'python-gtk2' : { 
		'fedora' : ['pygtk2'], 
		'ubuntu' : ['python-gtk2']
	}, 
	'python-glade2' : { 
		'fedora' : ['pygtk2-libglade'], 
		'ubuntu' : ['python-glade2']
	}, 
	'libglib2.0-dev' : { 
		'fedora' : ['glib2-devel'], 
		'ubuntu' : ['libglib2.0-dev']
	}, 
	'libmtp-dev' : { 
		'fedora' : ['libmtp-devel'], 
		'ubuntu' : ['libmtp-dev']
	}, 
	'libsqlite3-dev' : { 
		'fedora' : ['libsqlite3x-devel'], 
		'ubuntu' : ['libsqlite3-dev']
	}, 
	'libipodui-cil' : { 
		'fedora' : ['ipod-sharp'], 
		'ubuntu' : ['libipodui-cil']
	}, 
	'libipodui-cil-dev' : { 
		'fedora' : ['libipodui-cil-dev'], 
		'ubuntu' : ['libipodui-cil-dev']
	}, 
	'libipod-cil' : { 
		'fedora' : ['ipod-sharp'], 
		'ubuntu' : ['libipod-cil']
	}, 
	'libipod-cil-dev' : { 
		'fedora' : ['libipod-cil-dev'], 
		'ubuntu' : ['libipod-cil-dev']
	}, 
	'libglade2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libglade2.0-cil']
	}, 
	'libglib2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libglib2.0-cil']
	}, 
	'libglib2.0-cil-dev' : { 
		'fedora' : ['libglib2.0-cil-dev'], 
		'ubuntu' : ['libglib2.0-cil-dev']
	}, 
	'libnotify0.4-cil' : { 
		'fedora' : ['notify-sharp'], 
		'ubuntu' : ['libnotify0.4-cil']
	}, 
	'libnotify-cil-dev' : { 
		'fedora' : ['libnotify-cil-dev'], 
		'ubuntu' : ['libnotify-cil-dev']
	}, 
	'libnotify-dev' : { 
		'fedora' : ['libnotify-devel'], 
		'ubuntu' : ['libnotify-dev-gtk2.10']
	}, 
	'libmono-zeroconf-cil-dev' : { 
		'fedora' : ['libmono-zeroconf-cil-dev'], 
		'ubuntu' : ['libmono-zeroconf-cil-dev']
	}, 
	'libmono-zeroconf1.0-cil' : { 
		'fedora' : ['mono-zeroconf'], 
		'ubuntu' : ['libmono-zeroconf1.0-cil']
	}, 
	'libtaglib2.0-cil' : { 
		'fedora' : ['taglib-sharp'], 
		'ubuntu' : ['libtaglib2.0-cil']
	}, 
	'uuid-dev' : { 
		'fedora' : ['uuid-devel'], 
		'ubuntu' : ['uuid-dev']
	}, 
	'libdevmapper-dev' : { 
		'fedora' : ['device-mapper-devel'], 
		'ubuntu' : ['libdevmapper-dev']
	}, 
	'libselinux-dev' : { 
		'fedora' : ['libselinux-devel'], 
		'ubuntu' : ['libselinux1-dev']
	}, 
	'libparted1.8-dev' : { 
		'fedora' : ['parted-devel'], 
		'ubuntu' : ['libparted1.8-dev']
	}, 
	'open-iscsi' : { 
		'fedora' : ['iscsi-initiator-utils'], 
		'ubuntu' : ['open-iscsi']
	}, 
	'libpolicykit-dbus-dev' : { 
		'fedora' : ['PolicyKit-devel'], 
		'ubuntu' : ['libpolkit-dbus-dev']
	}, 
	'lvm2' : { 
		'fedora' : ['lvm2'], 
		'ubuntu' : ['lvm2']
	}, 
	'libxen3-dev' : { 
		'fedora' : ['xen-devel'], 
		'ubuntu' : ['libxen3-dev']
	}, 
	'libsasl2-dev' : { 
		'fedora' : ['cyrus-sasl-devel'], 
		'ubuntu' : ['libsasl2-dev']
	}, 
	'libavahi-client-dev' : { 
		'fedora' : ['avahi-devel'], 
		'ubuntu' : ['libavahi-client-dev']
	}, 
	'libgnutls-dev' : { 
		'fedora' : ['gnutls-devel'], 
		'ubuntu' : ['libgnutls-dev']
	}, 
	'zlib-dev' : { 
		'fedora' : ['zlib-devel'], 
		'ubuntu' : ['zlib1g-dev']
	}, 
	'libreadline-dev' : { 
		'fedora' : ['readline-devel'], 
		'ubuntu' : ['libreadline5-dev']
	}, 
	'libncurses-dev' : { 
		'fedora' : ['ncurses-devel'], 
		'ubuntu' : ['libncurses5-dev']
	}, 
	'libxml2-dev' : { 
		'fedora' : ['libxml2-devel'], 
		'ubuntu' : ['libxml2-dev']
	}, 
	'libvirt' : { 
		'fedora' : ['libvirt'], 
		'ubuntu' : ['libvirt']
	}, 
	'libvirt0' : { 
		'fedora' : ['libvirt'], 
		'ubuntu' : ['libvirt0']
	}, 
	'libvirt0-dbg' : { 
		'fedora' : ['libvirt'], 
		'ubuntu' : ['libvirt0-dbg']
	}, 
	'libvirt-bin' : { 
		'fedora' : ['libvirt'], 
		'ubuntu' : ['libvirt-bin']
	}, 
	'libvirt-doc' : { 
		'fedora' : ['libvirt'], 
		'ubuntu' : ['libvirt-doc']
	}, 
	'libvirt-dev' : { 
		'fedora' : ['libvirt-devel'], 
		'ubuntu' : ['libvirt-dev']
	}, 
	'python-libvirt' : { 
		'fedora' : ['libvirt-python'], 
		'ubuntu' : ['python-libvirt']
	}, 
	'libmono-sharpzip2.84-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-sharpzip2.84-cil']
	}, 
	'libmono2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono2.0-cil']
	}, 
	'libmono-sqlite2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-sqlite2.0-cil']
	}, 
	'libmono-system-web2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-system-web2.0-cil']
	}, 
	'libmono-system-data2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-system-data2.0-cil']
	}, 
	'libmono-dev' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-dev']
	}, 
	'mono-devel' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['mono-devel']
	}, 
	'boo' : { 
		'fedora' : ['boo'], 
		'ubuntu' : ['boo']
	}, 
	'lsb-release' : { 
		'fedora' : ['redhat-lsb'], 
		'ubuntu' : ['lsb-release']
	}, 
	'libgnomepanel2.24-cil' : { 
		'fedora' : ['gnome-desktop-sharp-devel'], 
		'ubuntu' : ['libgnomepanel2.24-cil']
	}, 
	'libmono-addins-gui0.2-cil' : { 
		'fedora' : ['mono-addins-devel'], 
		'ubuntu' : ['libmono-addins-gui0.2-cil']
	}, 
	'libmono-addins0.2-cil' : { 
		'fedora' : ['mono-addins-devel'], 
		'ubuntu' : ['libmono-addins0.2-cil']
	}, 
	'libndesk-dbus-glib1.0-cil' : { 
		'fedora' : ['ndesk-dbus-glib-devel'], 
		'ubuntu' : ['libndesk-dbus-glib1.0-cil']
	}, 
	'libndesk-dbus-glib1.0-cil-dev' : {
		'fedora' : ['libndesk-dbus-glib1.0-cil-dev'], 
		'ubuntu' : ['libndesk-dbus-glib1.0-cil-dev']
	},
	'libndesk-dbus1.0-cil' : { 
		'fedora' : ['ndesk-dbus-devel'], 
		'ubuntu' : ['libndesk-dbus1.0-cil']
	}, 
	'libndesk-dbus1.0-cil-dev' : {
		'fedora' : ['libndesk-dbus1.0-cil-dev'], 
		'ubuntu' : ['libndesk-dbus1.0-cil-dev']
	},
	'libmono-addins-cil-dev' : {
		'fedora' : ['libmono-addins-cil-dev'], 
		'ubuntu' : ['libmono-addins-cil-dev']
	},
	'libmono-addins-gui-cil-dev' : {
		'fedora' : ['libmono-addins-gui-cil-dev'], 
		'ubuntu' : ['libmono-addins-gui-cil-dev']
	},
	'libtaglib-cil-dev' : { 
		'fedora' : ['libtaglib-cil-dev'], 
		'ubuntu' : ['libtaglib-cil-dev']
	}, 
	'libmono-cairo2.0-cil' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['libmono-cairo2.0-cil']
	}, 
	'scrollkeeper' : { 
		'fedora' : ['scrollkeeper'], 
		'ubuntu' : ['scrollkeeper']
	}, 
	'gnome-doc-utils' : { 
		'fedora' : ['gnome-doc-utils'], 
		'ubuntu' : ['gnome-doc-utils']
	}, 
	'libgmime2.2a-cil' : { 
		'fedora' : ['gmime-sharp'], 
		'ubuntu' : ['libgmime2.2a-cil']
	}, 
	'libatk1.0-dev' : { 
		'fedora' : ['atk-devel'], 
		'ubuntu' : ['libatk1.0-dev']
	}, 
	'sharutils' : { 
		'fedora' : ['sharutils'], 
		'ubuntu' : ['sharutils']
	}, 
	'cli-common-dev' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['cli-common-dev']
	}, 
	'libpanel-applet2-dev' : { 
		'fedora' : ['gnome-panel-devel', 'gnome-panel-libs'], 
		'ubuntu' : ['libpanel-applet2-dev']
	}, 
	'libgtkspell-dev' : { 
		'fedora' : ['gtkspell-devel'], 
		'ubuntu' : ['libgtkspell-dev']
	}, 
	'libgconf2.0-cil' : { 
		'fedora' : ['gnome-sharp-devel'], 
		'ubuntu' : ['libgconf2.0-cil']
	}, 
	'libgconf2.0-cil-dev' : { 
		'fedora' : ['libgconf2.0-cil-dev'], 
		'ubuntu' : ['libgconf2.0-cil-dev']
	}, 
	'libgconf2-dev' : { 
		'fedora' : ['GConf2-devel'], 
		'ubuntu' : ['libgconf2-dev']
	}, 
	'libgnome2.24-cil' : { 
		'fedora' : ['gnome-sharp-devel'], 
		'ubuntu' : ['libgnome2.24-cil']
	}, 
	'libgtk2.0-cil' : { 
		'fedora' : ['gtk-sharp2-devel'], 
		'ubuntu' : ['libgtk2.0-cil']
	}, 
	'libgtk2.0-cil-dev' : { 
		'fedora' : ['libgtk2.0-cil-dev'], 
		'ubuntu' : ['libgtk2.0-cil-dev']
	}, 
	'hello' : { 
		'fedora' : ['hello'], 
		'ubuntu' : ['hello']
	}, 
	'jokosher' : { 
		'fedora' : ['jokosher'], 
		'ubuntu' : ['jokosher']
	}, 
	'mono-dev' : { 
		'fedora' : ['mono-devel'], 
		'ubuntu' : ['mono-devel']
	}, 
	'shrip' : { 
		'fedora' : ['shrip'], 
		'ubuntu' : ['shrip']
	}, 
	'spacepony-client' : { 
		'fedora' : ['spacepony-client'], 
		'ubuntu' : ['spacepony-client']
	}, 
	'pyactiveresource' : { 
		'fedora' : ['pyactiveresource'], 
		'ubuntu' : ['pyactiveresource']
	}, 
	'pitivi' : { 
		'fedora' : ['pitivi'], 
		'ubuntu' : ['pitivi']
	}, 
	'pexpect' : { 
		'fedora' : ['pexpect'], 
		'ubuntu' : ['pexpect']
	}, 
	'gwibber' : { 
		'fedora' : ['gwibber'], 
		'ubuntu' : ['gwibber']
	}, 
	'gwibber-service' : { 
		'fedora' : ['gwibber-service'], 
		'ubuntu' : ['gwibber-service']
	}, 
	'gwibber-themes' : { 
		'fedora' : ['gwibber-themes'], 
		'ubuntu' : ['gwibber-themes']
	}, 
	'd-feet' : { 
		'fedora' : ['d-feet'], 
		'ubuntu' : ['d-feet']
	}, 
	'gpodder' : { 
		'fedora' : ['gpodder'], 
		'ubuntu' : ['gpodder']
	}, 
	'banshee' : { 
		'fedora' : ['banshee'], 
		'ubuntu' : ['banshee']
	}, 
	'monodoc-manual' : { 
		'fedora' : ['monodoc'], 
		'ubuntu' : ['monodoc-manual']
	}, 
	'monodoc-banshee' : { 
		'fedora' : [], 
		'ubuntu' : ['monodoc-banshee-manual']
	}, 
	'monodoc-base' : { 
		'fedora' : ['monodoc'], 
		'ubuntu' : ['monodoc-base']
	}, 
	'gstreamer-gnonlin' : { 
		'fedora' : ['gnonlin'], 
		'ubuntu' : ['gstreamer0.10-gnonlin']
	}, 
	'python-cairo' : { 
		'fedora' : ['pycairo'], 
		'ubuntu' : ['python-cairo']
	}, 
	'python-dbus' : { 
		'fedora' : ['dbus-python'], 
		'ubuntu' : ['python-dbus']
	}, 
	'python-gstreamer' : { 
		'fedora' : ['gstreamer-python'], 
		'ubuntu' : ['python-gst0.10']
	}, 
	'gstreamer-plugins-good' : { 
		'fedora' : ['gstreamer-plugins-good'], 
		'ubuntu' : ['gstreamer0.10-plugins-good']
	}, 
	'gstreamer-plugins-base' : { 
		'fedora' : ['gstreamer-plugins-bad'], 
		'ubuntu' : ['gstreamer0.10-plugins-base']
	}, 
	'python-setuptools' : { 
		'fedora' : ['python-setuptools-devel'], 
		'ubuntu' : ['python-setuptools']
	}, 
	'gettext' : { 
		'fedora' : ['gettext'], 
		'ubuntu' : ['gettext']
	}, 
	'gettext-dev' : { 
		'fedora' : ['gettext-devel'], 
		'ubuntu' : ['gettext']
	}, 
	'info' : { 
		'fedora' : ['info'], 
		'ubuntu' : ['info']
	}, 
	'python' : { 
		'fedora' : ['python'], 
		'ubuntu' : ['python']
	}, 
	'python-vte' : { 
		'fedora' : ['vte'], 
		'ubuntu' : ['python-vte']
	}, 
	'python-gobject' : { 
		'fedora' : ['pygobject2'], 
		'ubuntu' : ['python-gobject']
	}, 
	'desktop-file-utils' : { 
		'fedora' : ['desktop-file-utils'], 
		'ubuntu' : ['desktop-file-utils']
	}, 
	'python-webkit' : { 
		'fedora' : ['python-webkit'], 
		'ubuntu' : ['python-webkit']
	}, 
	'python-central' : { 
		'fedora' : ['python-central'], 
		'ubuntu' : ['python-central']
	}, 
	'python-all-dev' : { 
		'fedora' : ['python-devel', 'python'], 
		'ubuntu' : ['python-all-dev']
	}, 
	'python-all' : { 
		'fedora' : [], 
		'ubuntu' : ['python-all']
	},
	'python-dev' : { 
		'fedora' : ['python-devel', 'python'], 
		'ubuntu' : ['python-dev']
	}, 
	'python-distutils-extra' : { 
		'fedora' : ['python-distutils-extra'], 
		'ubuntu' : ['python-distutils-extra']
	}, 
	'python-gconf' : { 
		'fedora' : ['gnome-python2-gconf'], 
		'ubuntu' : ['python-gconf']
	}, 
	'python-notify' : { 
		'fedora' : ['notify-python'], 
		'ubuntu' : ['python-notify']
	}, 
	'python-inotify' : { 
		'fedora' : ['python-inotify'], 
		'ubuntu' : ['python-pyinotify']
	}, 
	'tomboy' : { 
		'fedora' : ['tomboy'], 
		'ubuntu' : ['tomboy']
	}, 
	'terminator' : { 
		'fedora' : ['terminator'], 
		'ubuntu' : ['terminator']
	}, 
	'python-egenix-mxdatetime' : { 
		'fedora' : [], 
		'ubuntu' : ['python-egenix-mxdatetime']
	}, 
	'python-simplejson' : { 
		'fedora' : ['python-simplejson'], 
		'ubuntu' : ['python-simplejson']
	}, 
	'libwebkit' : { 
		'fedora' : ['webkitgtk'], 
		'ubuntu' : ['libwebkit-1.0-1']
	}, 
	'python-webkitgtk' : { 
		'fedora' : ['pywebkitgtk'], 
		'ubuntu' : ['python-webkitgtk']
	}, 
	'librsvg2-common' : { 
		'fedora' : ['librsvg2'], 
		'ubuntu' : ['librsvg2-2', 'librsvg2-common']
	}, 
	'librsvg2' : { 
		'fedora' : ['librsvg2'], 
		'ubuntu' : ['librsvg2-2', 'librsvg2-common']
	}, 
	'python-feedparser' : { 
		'fedora' : ['python-feedparser'], 
		'ubuntu' : ['python-feedparser']
	}, 
	'python-imaging' : { 
		'fedora' : ['python-imaging'], 
		'ubuntu' : ['python-imaging']
	}, 
	'python-gnome2-desktop' : { 
		'fedora' : ['gnome-python2-gnomedesktop'], 
		'ubuntu' : ['python-gnome2-desktop']
	}, 
	'python-xdg' : { 
		'fedora' : ['pyxdg'], 
		'ubuntu' : ['python-xdg']
	}, 
	'libxml-parser-perl' : { 
		'fedora' : ['perl(XML::Parser)'], 
		'ubuntu' : ['libxml-parser-perl']
	}, 
	'intltool' : { 
		'fedora' : ['intltool'], 
		'ubuntu' : ['intltool']
	}, 
	'python-gnome2' : { 
		'fedora' : ['gnome-python2'], 
		'ubuntu' : ['python-gnome2']
	}, 
	'python-zope-interface' : { 
		'fedora' : ['python-zope-interface'], 
		'ubuntu' : ['python-zope-interface']
	}, 
	'libgstreamer' : { 
		'fedora' : ['gstreamer'], 
		'ubuntu' : ['libgstreamer0.10-0']
	}, 
	'gstreamer0.10' : { 
		'fedora' : ['gstreamer'], 
		'ubuntu' : ['gstreamer0.10-x']
	}, 
	'gnome-icon-theme' : { 
		'fedora' : ['gnome-icon-theme'], 
		'ubuntu' : ['gnome-icon-theme']
	}, 
	'python-pygoocanvas' : { 
		'fedora' : ['pygoocanvas'], 
		'ubuntu' : ['python-pygoocanvas']
	}, 
	'ogmrip-dev' : { 
		'fedora' : ['ogmrip-devel'], 
		'ubuntu' : ['libogmrip-dev', 'ogmrip']
	}, 
	'ogmrip' : { 
		'fedora' : ['ogmrip'], 
		'ubuntu' : ['ogmrip']
	}, 
	'libdvdread-dev' : { 
		'fedora' : ['libdvdread-devel'], 
		'ubuntu' : ['libdvdread-dev']
	}, 
	'eject' : { 
		'fedora' : ['eject'], 
		'ubuntu' : ['eject']
	}, 
	'mplayer' : { 
		'fedora' : ['mplayer'], 
		'ubuntu' : ['mplayer']
	}, 
	'mencoder' : { 
		'fedora' : ['mencoder'], 
		'ubuntu' : ['mencoder']
	}, 
	'libenchant-dev' : { 
		'fedora' : ['enchant-devel'], 
		'ubuntu' : ['libenchant-dev']
	}, 
	'vorbis-tools' : { 
		'fedora' : ['vorbis-tools'], 
		'ubuntu' : ['vorbis-tools']
	}, 
	'lame' : { 
		'fedora' : ['lame'], 
		'ubuntu' : ['lame']
	}, 
	'gconf2' : { 
		'fedora' : ['GConf2'], 
		'ubuntu' : ['gconf2']
	}, 
	'libglade2-dev' : { 
		'fedora' : ['libglade2-devel'], 
		'ubuntu' : ['libglade2-dev']
	}, 
	'mkvtoolnix' : { 
		'fedora' : ['mkvtoolnix'], 
		'ubuntu' : ['mkvtoolnix']
	}, 
	'libtheora-dev' : { 
		'fedora' : ['libtheora-devel'], 
		'ubuntu' : ['libtheora-dev']
	}, 
	'faac' : { 
		'fedora' : ['faac'], 
		'ubuntu' : ['faac']
	}, 
	'libvorbis-dev' : { 
		'fedora' : ['libvorbis-devel'], 
		'ubuntu' : ['libvorbis-dev']
	}, 
	'libdbus-glib-dev' : { 
		'fedora' : ['dbus-glib-devel'], 
		'ubuntu' : ['libdbus-glib-1-dev']
	}, 
	'libx264-dev' : { 
		'fedora' : ['x264-libs'], 
		'ubuntu' : ['libx264-dev']
	}, 
	'ogmtools' : { 
		'fedora' : ['ogmtools'], 
		'ubuntu' : ['ogmtools']
	}, 
	'tesseract' : { 
		'fedora' : ['tesseract'], 
		'ubuntu' : ['tesseract-ocr']
	}, 
	'tesseract-dev' : { 
		'fedora' : ['tesseract-devel'], 
		'ubuntu' : ['tesseract-ocr-dev']
	}, 
	'ocrad' : { 
		'fedora' : ['ocrad'], 
		'ubuntu' : ['ocrad']
	}, 
	'gocr' : { 
		'fedora' : ['gocr'], 
		'ubuntu' : ['gocr']
	}, 
	'gpac' : { 
		'fedora' : ['gpac'], 
		'ubuntu' : ['gpac']
	}, 
	'help2man' : { 
		'fedora' : ['help2man'], 
		'ubuntu' : ['help2man']
	}, 
	'imagemagick' : { 
		'fedora' : ['ImageMagick'], 
		'ubuntu' : ['imagemagick']
	}, 
	'python-gpod' : {
		'fedora' : ['python-gpod'], 
		'ubuntu' : ['python-gpod']
	}, 
	'python-pymtp' : {
		'fedora' : [], 
		'ubuntu' : ['python-pymtp']
	}, 
}
