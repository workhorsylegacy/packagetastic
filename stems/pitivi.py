#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class PitiviPackage(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'pitivi'
		self._version = '0.11.3'
		self._section = 'misc'
		self._priority = 'optional'
		self._authors = ['Christophe Sauthier <christophe.sauthier@gmail.com>', 
							'Laszlo Pandy <laszlok2@gmail.com>', 
							'Ernst Persson  <ernstp@gmail.com>', 
							'Richard Boulton <richard@tartarus.org>', 
							'Thibaut Girka <thibaut.girka@free.fr>', 
							'Jeff Fortin <nekohayo@gmail.com>', 
							'Johan Dahlin <jdahlin@async.com.br>', 
							'Brandon Lewis <brandon_lewis@berkeley.edu>', 
							'Luca Della Santina <dellasantina@farm.unipi.it>', 
							'Thijs Vermeir <thijsvermeir@gmail.com>']
		self._copyright = ['Edward HERVEY <bilboed@bilboed.com>', 
							'Christophe Sauthier <christophe.sauthier@gmail.com>', 
							'Laszlo Pandy <laszlok2@gmail.com>', 
							'Ernst Persson <ernstp@gmail.com>', 
							'Richard Boulton <richard@tartarus.org>']
		self._homepage = 'http://www.pitivi.org'
		self._license = 'LGPL2.1'
		self._source = 'http://ftp.gnome.org/pub/GNOME/sources/pitivi/0.11/pitivi-0.11.3.tar.gz'
		self._build_method = 'python application'

		self._build_requirements = ['libxml-parser-perl', 
										'intltool (>= 0.35)']

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

		self._short_description = "non-linear audio/video editor using GStreamer"

		self._long_description = "PiTiVi allows users to easily edit audio/video projects based on the\n" + \
									"GStreamer framework.  PiTIVi provides several ways of creating and\n" + \
									"modifying a timeline.  Ranging from a simple synopsis view (a-la\n" + \
									"iMovie) to the full-blown editing view (aka Complex View) which puts\n" + \
									"you in complete control of your editing."

		self._changelog = [{"version" : "0.11.3", "time" : "Fri, 21 Aug 2009 18:20:25 -0700", "text" : "Initial release" } ]



