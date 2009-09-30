#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'gpodder'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._authors = [u'Thomas Perl <thp[at]thpinfo.com>']
		self._copyright = [u'2005-2008 Thomas Perl']
		self._homepage = 'http://gpodder.org/'
		self._license = 'GPL3+'
		self._source = 'http://download.berlios.de/gpodder/gpodder-0.14.0.tar.gz'

		self._build_requirements = ['python-feedparser', 'imagemagick']

		self._short_description = u"A free podcast aggregator written in PyGTK"

		self._long_description = u"gPodder is a podcast receiver/catcher. You can subscribe to feeds\n" + \
									u"(\"podcasts\") and automatically download new audio and video content.\n" + \
									u"Downloaded content can be played on your desktop or synchronized to\n" + \
									u"iPods, MTP-based players, filesystem-based MP3 players and Bluetooth\n" + \
									u"enabled mobile phones"

		self._changelog = [Changelog(version="0.14.0", release=1, time="Fri, 21 Aug 2009 20:24:17 -0700", text=u"Initial release") ]

class GPodder(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'gpodder'
		self._build_method = 'python application'
		self._category = 'Applications/Audio'
		self._priority = 'optional'
		self._install_requirements = []

		self._files = ['/usr/bin/gpodder', 
						'/usr/share/gpodder/', 
						'/usr/share/icons/hicolor/', 
						'/usr/share/man/man1/*', 
						'/usr/share/applications/*.desktop', 
						'/usr/share/pixmaps/gpodder*.png', 
						'/usr/lib/python2.6/site-packages/gpodder/', 
						'/usr/lib/python2.6/site-packages/gpodder*.egg-info']


