#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class LibVirtPackage(BaseMeta):
	def __init__(self):
		BaseMeta.__init__(self)
		self._name = 'libvirt'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._authors = [u'Daniel Veillard <veillard@redhat.com>']
		self._copyright = [u'2000 Daniel Veillard', 
							u'1991-2009 Free Software Foundation, Inc.', 
							u'2008 IBM Corp.', 
							u'2005-2009 Red Hat, Inc.', 
							u'2006-2008 Daniel P. Berrange', 
							u'2008 Virtual Iron Software, Inc.', 
							u'2008 David F. Lively', 
							u'2005 Anthony Liguori', 
							u'2006, 2007 Binary Karma', 
							u'2006 Shuveb Hussain', 
							u'2007 Anoop Joe Cyriac', 
							u'2000 Bjorn Reese', 
							u'2006, 2007 Binary Karma']
		self._homepage = 'http://libvirt.org'
		self._license = 'GPL2+'
		self._source = 'http://libvirt.org/sources/libvirt-0.6.0.tar.gz'

		self._build_requirements = ["libxml2-dev", 
									"libncurses-dev", 
									"libreadline-dev", 
									"zlib-dev", 
									"libgnutls-dev", 
									"libavahi-client-dev", 
									"libsasl2-dev", 
									"libxen3-dev",
									"lvm2", 
									"libpolicykit-dbus-dev", 
									"open-iscsi", 
									"libparted1.8-dev", 
									"libselinux-dev", 
									"libdevmapper-dev", 
									"uuid-dev", 
									"libhal-dev"]

		self._short_description = u'library for interfacing with different virtualization systems'

		self._long_description = u"Libvirt is a C toolkit to interact with the virtualization capabilities \n" + \
									u"of recent versions of Linux (and other OSes). The library aims at providing \n" + \
									u"a long term stable C API for different virtualization mechanisms. It currently \n" + \
									u"supports QEMU, KVM, and XEN."

		self._changelog = [Changelog(version="0.6.0", release=1, time="Wed, 16 Sep 2009 23:09:55 -0700", text=u"Initial release") ]

class LibVirtBin(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'libvirt-bin'
		self._build_method = 'c application'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = []
		self._additional_description = \
		u"This package contains the supporting binaries to use with libvirt"

class LibVirtZero(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'libvirt0'
		self._build_method = 'c application'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = ['lvm2']
		self._additional_description = u""

class LibVirtZeroDebug(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'libvirt0-dbg'
		self._build_method = 'c application'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = ['libvirt0']
		self._additional_description = \
		u"This package contains the debugging symbols."

class LibVirtDocumentation(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'libvirt-doc'
		self._build_method = 'documentation'
		self._category = 'Documentation'
		self._priority = 'optional'
		self._install_requirements = []
		self._additional_description = \
		u"This package contains the documentation."

class LibVirtDev(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'libvirt-dev'
		self._build_method = 'c application'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = ['libvirt0', 'libxen3-dev']
		self._additional_description = \
		u"This package contains the header files and static libraries which are \n" + \
		u"needed for developing the applications with libvirt."

# FIXME: Make the python bindings work too
'''
class PythonLibVirt(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'python-libvirt'
		self._build_method = 'python library'
		self._category = 'Development/Libraries'
		self._priority = 'optional'
		self._install_requirements = ['libvirt0']
		self._additional_description = \
		u"This package contains Python bindings for the libvirt library"
'''


