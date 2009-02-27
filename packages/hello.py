#!/usr/bin/env python

from packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class HelloPackage(BasePackage):
	def __init__(self):
		self.call_parent_constructor()
		self._name = 'hello'
		self._version = '2.1.1'
		self._section = 'devel'
		self._priority = 'optional'
		self._authors = ['Free Software Foundation, Inc.']
		self._copyright = ['1992, 1995, 1996, 1997-1999, 2000-2002 Free Software Foundation, Inc.']
		self._packager_name = 'Matthew Brennan Jones'
		self._packager_email = 'mattjones@workhorsy.org'
		self._bug_mail = 'mattjones@workhorsy.org'
		self._homepage = 'http://ftp.gnu.org'
		self._license = 'GPL'
		self._source = 'http://ftp.gnu.org/gnu/hello/hello-2.1.1.tar.gz'

		# FIXME: debhelper is a Debian specific package
		self._build_requirements = ["debhelper (>= 7)", 
									"autotools-dev"]

		self._install_requirements = ["${shlibs:Depends}", 
										"${misc:Depends}"]

		self._short_description = 'The classic greeting, and a good example'

		# FIXME: Having a one space indent on this is a Debian specific thing and should be handled by the framework instead.
		self._long_description = " The GNU hello program produces a familiar, friendly greeting.  It\n" + \
								" allows non-programmers to use a classic computer science tool which\n" + \
								" would otherwise be unavailable to them.\n" + \
								" .\n" + \
								" Seriously, though: this is an example of how to do a Debian\n" + \
								" package.\n" + \
								" It is the Debian version of the GNU Project's `hello world' program\n" + \
								" (which is itself an example for the GNU Project)."

	def build(self):
		self.configure_make_install()



build_ubuntu(HelloPackage())

