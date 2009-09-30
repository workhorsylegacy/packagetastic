#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'terminator'
		self._category = 'Applications/System'
		self._priority = 'optional'
		self._authors = [u'Chris Jones <cmsj@tenshu.net>']
		self._copyright = [u'2006-2008 Chris Jones']
		self._homepage = 'http://www.tenshu.net/terminator/'
		self._license = 'GPL2+'
		self._source = 'http://launchpad.net/terminator/trunk/0.12/+download/terminator_0.12.tar.gz'

		self._build_requirements = ['python-dev', 'gettext', 'desktop-file-utils']

		self._short_description = u"multiple GNOME terminals in one window"

		self._long_description = u"Terminator is a little project to produce an efficient way of\n" + \
									u"filling a large area of screen space with terminals.\n" + \
									u"\n" + \
									u"The user can have multiple terminals in one window and use\n" + \
									u"key bindings to switch between them. See the manpage for\n" + \
									u"details."

		self._changelog = [Changelog(version="0.12", release=1, time="Fri, 07 Aug 2009 18:32:26 -0700", text=u"Initial release") ]

class Shrip(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'terminator'
		self._build_method = 'python application'
		self._alternate_name = 'x-terminal-emulator'
		self._category = 'Applications/System'
		self._priority = 'optional'
		self._install_requirements = ['python-gobject', 'python-gtk2', 
										'python-gconf', 'python-vte']

		self._files = ['/usr/share/man/man1/terminator.*', 
						'/usr/share/man/man5/terminator_config.*', 
						'/usr/bin/terminator', 
						'/usr/lib/python2.6/site-packages/*', 
						'/usr/share/applications/terminator.desktop', 
						'/usr/share/icons/hicolor/*/*/terminator*.png', 
						'/usr/share/icons/hicolor/*/*/terminator*.svg', 
						'/usr/share/pixmaps/terminator.png']


