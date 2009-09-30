#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'gwibber'
		self._category = 'Applications/Communications'
		self._priority = 'optional'
		self._authors = [u'Ryan Paul (SegPhault) <segphault@arstechnica.com>']
		self._copyright = [u'2008 Ryan Paul']
		self._homepage = 'https://launchpad.net/gwibber'
		self._license = 'GPL2+'
		self._source = 'http://launchpad.net/gwibber/+download/gwibber-0.8.tar.gz'

		self._build_requirements = ['python-all-dev', 
									'python-distutils-extra']

		self._short_description = u"Open source microblogging client for GNOME"

		self._long_description = u"It supports Twitter, Jaiku, Identi.ca, Facebook, and Digg."

		self._changelog = [Changelog(version="0.8", release=1, time="Mon, 24 Aug 2009 15:28:47 -0700", text=u"Initial release") ]

class Gwibber(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'gwibber'
		self._build_method = 'python application'
		self._category = 'Applications/Communications'
		self._priority = 'optional'
		self._install_requirements = ['python-dbus', 
										'python-gtk2', 
										'python-gconf', 
										'python-notify', 
										#'python-egenix-mxdatetime', 
										'python-simplejson', 
										'python-cairo', 
										'libwebkit', 
										'python-webkitgtk', 
										'librsvg2', 
										'librsvg2-common', 
										'python-feedparser', 
										'python-imaging', 
										'python-gnome2-desktop', 
										'python-xdg']

		self._files = ['/usr/lib/python2.6/site-packages/gwibber', 
						'/usr/lib/python2.6/site-packages/gwibber-*.egg-info', 
						'/usr/bin/gwibber', 
						'/usr/share/gwibber', 
						'/usr/share/pixmaps/gwibber.svg', 
						'/usr/share/applications/fedora-gwibber.desktop']

