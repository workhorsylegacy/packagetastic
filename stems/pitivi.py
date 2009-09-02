#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class Meta(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'pitivi'
		self._category = 'Applications/Video'
		self._priority = 'optional'
		self._authors = [u'Christophe Sauthier <christophe.sauthier@gmail.com>', 
							u'Laszlo Pandy <laszlok2@gmail.com>', 
							u'Ernst Persson  <ernstp@gmail.com>', 
							u'Richard Boulton <richard@tartarus.org>', 
							u'Thibaut Girka <thibaut.girka@free.fr>', 
							u'Jeff Fortin <nekohayo@gmail.com>', 
							u'Johan Dahlin <jdahlin@async.com.br>', 
							u'Brandon Lewis <brandon_lewis@berkeley.edu>', 
							u'Luca Della Santina <dellasantina@farm.unipi.it>', 
							u'Thijs Vermeir <thijsvermeir@gmail.com>']
		self._copyright = [u'Edward HERVEY <bilboed@bilboed.com>', 
							u'Christophe Sauthier <christophe.sauthier@gmail.com>', 
							u'Laszlo Pandy <laszlok2@gmail.com>', 
							u'Ernst Persson <ernstp@gmail.com>', 
							u'Richard Boulton <richard@tartarus.org>']
		self._homepage = 'http://www.pitivi.org'
		self._license = 'LGPL2.1'
		self._source = 'http://ftp.gnome.org/pub/GNOME/sources/pitivi/0.11/pitivi-0.11.3.tar.gz'

		self._build_requirements = ['libxml-parser-perl', 
										'intltool (>= 0.35)']

		self._short_description = u"non-linear audio/video editor using GStreamer"

		self._long_description = u"PiTiVi allows users to easily edit audio/video projects based on the\n" + \
									u"GStreamer framework.  PiTIVi provides several ways of creating and\n" + \
									u"modifying a timeline.  Ranging from a simple synopsis view (a-la\n" + \
									u"iMovie) to the full-blown editing view (aka Complex View) which puts\n" + \
									u"you in complete control of your editing."

		self._changelog = [Changelog(version="0.11.3", release=1, time="Fri, 21 Aug 2009 18:20:25 -0700", text=u"Initial release") ]

class Pitivi(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'pitivi'
		self._build_method = 'python application'
		self._category = 'Applications/Video'
		self._priority = 'optional'
		self._install_requirements = ['python-gtk2 (>= 2.8)', 
										'python-gst0.10 (>= 0.10.6)', 
										'gstreamer0.10-gnonlin (>= 0.10.10)', 
										'python-cairo (>= 1.0.0)', 
										'python-glade2', 
										'python-gnome2', 
										'python-dbus', 
										'python-pkg-resources', 
										'python-zope-interface', 
										'python-setuptools', 
										'gstreamer0.10-plugins-base', 
										'gstreamer0.10-plugins-good', 
										'libgstreamer0.10-0 (>= 0.10.13.1)', 
										'gstreamer0.10-x', 
										'gnome-icon-theme', 
										'python-pygoocanvas']

