#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'tomboy'
		self._category = 'Applications/Office'
		self._priority = 'optional'
		self._authors = [u'Alex Graveley <alex@beatniksoftware.com>', 
							u'Boyd Timothy <btimothy@gmail.com>', 
							u'Chris Scobell <chris@thescobells.com>', 
							u'David Trowbridge <trowbrds@gmail.com>', 
							u'Ryan Lortie <desrt@desrt.ca>', 
							u'Sandy Armstrong <sanfordarmstrong@gmail.com>', 
							u'Sebastian Rittau <srittau@jroger.in-berlin.de>', 
							u'Kevin Kubasik <kevin@kubasik.net>', 
							u'Stefan Schweizer <steve.schweizer@gmail.com>']
		self._copyright = [u'2004-2007 Alex Graveley']
		self._homepage = 'http://projects.gnome.org/tomboy/'
		self._license = 'LGPL2.1'
		self._source = 'http://download.gnome.org/sources/tomboy/0.15/tomboy-0.15.0.tar.gz'

		self._build_requirements = ['mono-dev (>= 2.0)', 
									'libgtk2.0-cil (>= 2.10.4-2)', 
									'libgnome2.24-cil (>= 2.16.1)', 
									'libgconf2.24-cil', 
									'libgtkspell-dev (>= 2.0.9)', 
									'intltool', 
									'libpanel-applet2-dev', 
									'cli-common-dev (>= 0.4.4)', 
									'sharutils', 
									'libgtk2.0-dev (>= 2.10.0)', 
									'libatk1.0-dev (>= 1.2.4)', 
									'libgmime2.2a-cil', 
									'gnome-doc-utils (>= 0.3.2)', 
									'scrollkeeper', 
									'libmono-cairo2.0-cil', 
									'libndesk-dbus1.0-cil (>= 0.4)', 
									'libndesk-dbus-glib1.0-cil (>= 0.3)', 
									'libmono-addins0.2-cil (>= 0.2-4)', 
									'libmono-addins-gui0.2-cil (>= 0.2-4)', 
									'libgnomepanel2.24-cil']

		self._short_description = u"desktop note taking program using Wiki style links"

		self._long_description = u"desktop note taking program using Wiki style links\n" + \
									u"Tomboy is a desktop note-taking application which is simple and easy to\n" + \
									u"use. It lets you organise your notes intelligently by allowing you to\n" + \
									u"easily link ideas together with Wiki style interconnects."

		self._changelog = [Changelog(version="0.15.0", release=1, time="Tue, 11 Aug 2009 20:31:55 -0700", text=u"Initial release") ]

class Tomboy(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'tomboy'
		self._build_method = 'mono application'
		self._category = 'Applications/Office'
		self._priority = 'optional'
		self._install_requirements = []



