#!/usr/bin/env python


import os
import commands

# Move the path to the location of the current file
os.chdir(os.sys.path[0])

f = open('ubuntu_dependencies.py', 'w')
f.write("packages = {\n")

for dpkg_line in commands.getoutput('dpkg --get-selections | grep -v deinstall').split("\n"):
	# Get the real package name
	package_name = dpkg_line[0:-7].strip()
	name, ver, num = None, None, None
	print "Searching: " + package_name

	# Get all the dependencies
	f.write("				\"" + package_name + "\" : [\n")
	rdepends_result = commands.getoutput('apt-rdepends --follow=DEPENDS ' + package_name)
	if rdepends_result.count(': ') > 0:
		for rdepends_line in rdepends_result.split(package_name + "\n")[1].split("\n"):

			name = "\"" + rdepends_line.split(': ')[1].split(' (')[0] + "\""

			if rdepends_line.count('('):
				ver = "\"" + rdepends_line.split('(')[1].split(' ')[0] + "\""
				num = "\"" + rdepends_line.split('(')[1].split(' ')[1].split(')')[0] + "\""
			else:
				ver, num = None, None

			f.write("							{ 'name' : " + str(name) + ", 'ver' : " + str(ver) + ", 'num' : " + str(num) + "},\n")

	f.write("						],\n")
	f.flush()

f.write("			}\n\n")





