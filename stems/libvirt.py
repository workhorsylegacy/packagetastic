#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from lib_packagetastic import *

class LibVirtPackage(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
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
		self._license = 'GPL'
		self._source = 'http://libvirt.org/sources/libvirt-0.6.0.tar.gz'

		self._build_requirements = ["cdbs (>= 0.4.43)", 
									"debhelper (>= 5.0.38)", 
									"libxml2-dev", 
									"libncurses5-dev", 
									"libreadline5-dev", 
									"zlib1g-dev", 
									"libgnutls-dev", 
									"python-dev (>= 2.3.5-11)",
									"python-central (>= 0.5.6)", 
									"quilt", 
									"libavahi-client-dev", 
									"libsasl2-dev", 
									"libxen3-dev [i386 amd64]",
									"lvm2", 
									"libpolkit-dbus-dev", 
									"open-iscsi", 
									"libparted1.8-dev"]

		self._install_requirements = ["bridge-utils", 
									"dnsmasq-base", 
									"netcat-openbsd", 
									"iptables", 
									"adduser"]

		self._short_description = u'library for interfacing with different virtualization systems'

		self._long_description = u"Libvirt is a C toolkit to interact with the virtualization capabilities \n" + \
									u"of recent versions of Linux (and other OSes). The library aims at providing \n" + \
									u"a long term stable C API for different virtualization mechanisms. It currently \n" + \
									u"supports QEMU, KVM, and XEN."

		self._changelog = [Changelog(version="0.6.0", release=1, time="Fri, 21 Aug 2009 19:49:12 -0700", text=u"Initial release") ]

	def install(self):
		return ''
		#self.configure_make()

