#!/usr/bin/env python

from packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class LibVirtPackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'libvirt'
		self._version = '0.6.0'
		self._section = 'development'
		self._priority = 'optional'
		self._authors = ['Daniel Veillard <veillard@redhat.com>']
		self._copyright = ['2000 Daniel Veillard', 
							'1991-2009 Free Software Foundation, Inc.', 
							'2008 IBM Corp.', 
							'2005-2009 Red Hat, Inc.', 
							'2006-2008 Daniel P. Berrange', 
							'2008 Virtual Iron Software, Inc.', 
							'2008 David F. Lively', 
							'2005 Anthony Liguori', 
							'2006, 2007 Binary Karma', 
							'2006 Shuveb Hussain', 
							'2007 Anoop Joe Cyriac', 
							'2000 Bjorn Reese', 
							'2006, 2007 Binary Karma']
		self._packager_name = 'Matthew Brennan Jones'
		self._packager_email = 'mattjones@workhorsy.org'
		self._bug_mail = 'mattjones@workhorsy.org'
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

		self._short_description = 'library for interfacing with different virtualization systems'

		# FIXME: Having a one space indent on this is a Debian specific thing and should be handled by the framework instead.
		self._long_description = " Libvirt is a C toolkit to interact with the virtualization capabilities \n" + \
									" of recent versions of Linux (and other OSes). The library aims at providing \n" + \
									" a long term stable C API for different virtualization mechanisms. It currently \n" + \
									" supports QEMU, KVM, and XEN."

	def build(self):
		self.configure_make_install()

build_ubuntu(LibVirtPackage())

