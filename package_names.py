#!/usr/bin/env python
# -*- coding: UTF-8 -*-

package_names = {
	'desktop-file-utils' : { 
		'fedora' : ['desktop-file-utils'], 
		'ubuntu' : ['desktop-file-utils']
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
		'ubuntu' : ['mono-dev']
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
	'monodoc-banshee' : { 
		'fedora' : [], 
		'ubuntu' : ['monodoc-banshee-manual']
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
	'python-glade2' : { 
		'fedora' : ['pygtk2-libglade'], 
		'ubuntu' : ['python-glade2']
	}, 
	'python-gtk2' : { 
		'fedora' : ['pygtk2'], 
		'ubuntu' : ['python-gtk2']
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
		'fedora' : ['python-setuptools'], 
		'ubuntu' : ['python-setuptools']
	}, 
	'gettext' : { 
		'fedora' : ['gettext'], 
		'ubuntu' : ['gettext']
	}, 
	'info' : { 
		'fedora' : ['info'], 
		'ubuntu' : ['info']
	}, 
	'python-vte' : { 
		'fedora' : [], 
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
	'python-all-dev' : { 
		'fedora' : ['python-devel', 'python'], 
		'ubuntu' : ['python-all-dev']
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
		'fedora' : ['perl-libxml-perl'], 
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
	'gstreamer' : { 
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
	'libogmrip-dev' : { 
		'fedora' : ['ogmrip-devel'], 
		'ubuntu' : ['libogmrip-dev']
	}, 
	'ogmrip' : { 
		'fedora' : ['ogmrip'], 
		'ubuntu' : ['ogmrip']
	}, 
	'libdvdread-dev' : { 
		'fedora' : ['libdvdread-devel'], 
		'ubuntu' : ['libdvdread-dev']
	}, 
	'libhal-dev' : { 
		'fedora' : ['hal-devel', 'hal-libs'], 
		'ubuntu' : ['libhal-dev']
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
	'libgconf2-dev' : { 
		'fedora' : ['GConf2-devel'], 
		'ubuntu' : ['libgconf2-dev']
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
	'libnotify-dev' : { 
		'fedora' : ['libnotify-devel'], 
		'ubuntu' : ['libnotify-dev-gtk2.10']
	}, 
	'tesseract' : { 
		'fedora' : ['tesseract'], 
		'ubuntu' : ['tesseract']
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
