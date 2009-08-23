#!/usr/bin/env python

import sys
from lib_packagetastic import *

# Move the path to the location of the current file
os.chdir(os.sys.path[0])


class PexpectPackage(BasePackage):
	def __init__(self):
		BasePackage.__init__(self)
		self._name = 'pexpect'
		self._version = '2.3'
		self._section = 'python'
		self._priority = 'optional'
		self._authors = ['Noah Spurrier <noah@noah.org>', 'Richard Holden', 'Marco Molteni', 'Kimberley Burchett',
						'Robert Stone', 'Hartmut Goebel', 'Chad Schroeder', 'Erick Tryzelaar', 'Dave Kirby', 
						'Ids vander Molen', 'George Todd', 'Noel Taylor', 'Nicolas D. Cesar', 'Alexander Gattin', 
						'Geoffrey Marshall', 'Francisco Lourenco', 'Glen Mabey', 'Karthik Gurusamy', 
						'Fernando Perez', 'Corey Minyard', 'Jon Cohen', 'Guillaume Chazarain', 'Andrew Ryan', 
						'Nick Craig-Wood', 'Andrew Stone', 'Jorgen Grahn']
		self._copyright = ['2008 Noah Spurrier']
		self._homepage = 'http://pexpect.sourceforge.net'
		self._license = 'MIT'
		self._source = 'http://downloads.sourceforge.net/pexpect/pexpect-2.3.tar.gz'
		self._build_method = 'python library'

		self._build_requirements = []

		self._install_requirements = []

		self._short_description = "Pexpect is a pure Python Expect. It allows easy control of other applications."

		self._long_description = "Pexpect is a Python module for spawning child applications and controlling\n" + \
								"them automatically. Pexpect can be used for automating interactive applications\n" + \
								"such as ssh, ftp, passwd, telnet, etc. It can be used to a automate setup\n" + \
								"scripts for duplicating software package installations on different servers. It\n" + \
								"can be used for automated software testing. Pexpect is in the spirit of Don\n" + \
								"Libes' Expect, but Pexpect is pure Python. Other Expect-like modules for Python\n" + \
								"require TCL and Expect or require C extensions to be compiled. Pexpect does not\n" + \
								"use C, Expect, or TCL extensions. It should work on any platform that supports\n" + \
								"the standard Python pty module. The Pexpect interface focuses on ease of use so\n" + \
								"that simple tasks are easy."

		self._changelog = [{"version" : "2.3", "time" : "Fri, 07 Aug 2009 18:32:26 -0700", "text" : "Initial release" } ]


	def after_install(self):
		return \
		"# Correct some permissions\n" + \
		"find examples -type f -exec chmod a-x \{\} \;\n" + \
		"chmod 755 $RPM_BUILD_ROOT%{python_sitelib}/FSM.py"


