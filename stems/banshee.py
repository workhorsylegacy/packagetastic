#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'banshee'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._authors = [u'Aaron Bockover <abock@gnome.org>', 
							u'Gabriel Burt <gabriel.burt@gmail.com>', 
							u'Scott Peterson <lunchtimemama@gmail.com>']
		self._copyright = [u'2004-2007 Alex Graveley', 
							u'2005-2006 Novell', 
							u'2005-2006 Jordi Mas i Hernàndez', 
							u'2005 Øivind Hoel and the GNOME Foundation', 
							u'2006 Ilkka Tuohela', 
							u'2005-2006 Adam Weinberger and the GNOME Foundation', 
							u'2006 The GNOME Foundation', 
							u'2006 Alessandro Gervaso', 
							u'2006 Novell and Gabriel Burt', 
							u'2005 James Willcox <snorp@snorp.net>', 
							u'2004 David Hammerton <david@crazney.net>', 
							u'2005 Jon Lech Johansen <jon@nanocrew.net>', 
							u'2001 by Matthew S. Ford', 
							u'2005 Todd Berman <tberman@off.net>', 
							u'2005 Ed Catmur <ed@catmur.co.uk>', 
							u'2005 Novell, Inc. (Miguel de Icaza, Aaron Bockover)', 
							u'2006 Sebastian Dröge <slomo@ubuntu.com>', 
							u'2006 Ruben Vermeersch <ruben@savanne.be>', 
							u'2006 Novell and Patrick van Staveren', 
							u'2006 Alp Toker <alp@atoker.com>', 
							u'2006 Sebastian Dröge <slomo@circular-chaos.org>', 
							u'2005 by Brian Nickel']
		self._homepage = 'http://banshee-project.org'
		self._license = 'LGPL2.1'
		self._source = 'http://download.banshee-project.org/banshee/banshee-1-1.4.3.tar.bz2'

		self._build_requirements = ['cli-common-dev (>= 0.4.4)', 
									'intltool (>= 0.35)', 
									'lsb-release', 
									'mono-dev (>= 2.0.0)', 
									'boo (>= 0.8.1)', 
									'libmono-dev (>= 1.2.4)', 
									'libmono-system-data2.0-cil', 
									'libmono-system-web2.0-cil', 
									'libmono-cairo2.0-cil', 
									'libmono-sqlite2.0-cil', 
									'libmono2.0-cil', 
									'libmono-sharpzip2.84-cil', 
									'libndesk-dbus1.0-cil (>= 0.5)', 
									'libndesk-dbus-glib1.0-cil (>= 0.3)', 
									'libmono-addins0.2-cil (>= 0.3)', 
									'libmono-addins-gui0.2-cil (>= 0.3)', 
									'libtaglib2.0-cil (>= 2.0.3.2)', 
									'libmono-zeroconf1.0-cil (>= 0.7.3)', 
									'libnotify0.4-cil', 
									'libglib2.0-cil (>= 2.10)', 
									'libgtk2.0-cil (>= 2.10)', 
									'libglade2.0-cil (>= 2.10)', 
									'libgconf2.24-cil', 
									'libgnome2.24-cil', 
									'libipod-cil (>= 0.8.2)', 
									'libipodui-cil (>= 0.8.2)', 
									'libkarma-cil (>= 0.0.5)', 
									'monodoc-base (>= 1.1.9)', 
									'libsqlite3-dev (>= 3.4)', 
									'libmtp-dev (>= 0.2.0)', 
									'gconf2', 
									'libglib2.0-dev', 
									'libgtk2.0-dev (>= 2.8)', 
									'libx11-dev', 
									'libxrandr-dev (>= 2:1.1.1)', 
									'libxxf86vm-dev (>= 1:1.0.1)', 
									'libgnomevfs2-dev', 
									'libgstreamer0.10-dev (>= 0.10.3)', 
									'libgstreamer-plugins-base0.10-dev (>= 0.10.12)']

		self._short_description = u"Media Management and Playback application"

		self._long_description = u"Banshee is an media management and playback application for the GNOME\n" + \
									u"desktop, allowing users to import audio from CDs, search their library,\n" + \
									u"create playlists of selections of their library, sync music to/from iPods\n" + \
									u"and other media devices, play and manage video files and burn selections\n" + \
									u"to a CD."

		self._changelog = [Changelog(version="1.4.3", release=1, time="Sun, 23 Aug 2009 19:31:37 -0700", text=u"Initial release")]

class Banshee(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'banshee'
		self._build_method = 'mono application'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._install_requirements = ['gstreamer0.10-plugins-base', 
										'gstreamer0.10-plugins-good (>= 0.10.8-4)', 
										'gstreamer0.10-gnomevfs', 
										'hal', 
										'gnome-icon-theme (>= 2.16)', 
										'gstreamer0.10-plugins-ugly', 
										'gstreamer0.10-plugins-bad', 
										'gstreamer0.10-ffmpeg', 
										'podsleuth (>= 0.6.0)', 
										'brasero',  
										'avahi-daemon']

class Documentation(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'monodoc-banshee'
		self._build_method = 'documentation'
		self._category = 'Documentation'
		self._priority = 'optional'
		self._install_requirements = ['monodoc-manual']

		self._additional_description = u"This package contains the developer documentation for Banshee."

		self._files = ['/usr/bin/banshee-1', 
						'/usr/lib/banshee-1', 
						'/usr/share/applications/*.desktop', 
						'/usr/share/dbus-1/services/org.bansheeproject.Banshee.service', 
						'/usr/share/dbus-1/services/org.bansheeproject.CollectionIndexer.service', 
						'/usr/share/banshee-1/', 
						'/usr/share/icons/hicolor/*/apps/media-player-banshee.png']


