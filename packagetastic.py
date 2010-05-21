#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys
import lib_packagetastic

# Move the path to the location of the current file
os.chdir(os.sys.path[0])

# Make sure we are root and the uid for the normal user was passed
if not lib_packagetastic.is_root():
	print "This program must be run as root. Exiting ..."
	exit()

# Determine what we are going to do
mode = ""
if len(sys.argv) == 5 and sys.argv[1] == "build":
	mode = "build"
elif len(sys.argv) == 5 and sys.argv[1] == "install":
	mode = "install"
#elif len(sys.argv) == 4 and sys.argv[1] == "build_all":
#	mode = "build_all"
else:
	mode = "help"

lib_packagetastic.setup_user_ids(int(sys.argv[4]))

# Show the usage
if mode == "help":
	print "usage:"
	print "./packagetastic build package_name"
	print "./packagetastic install package_name"
#	print "./packagetastic build_all"
	print ""
	print "build: Generates a Packagetastic package for the current distro."
	print "build_all: Generates all the packages."
	print ""
	print "examples:"
	print "./packagetastic build hello"
#	print "./packagetastic build_all"
	exit()

# Build a package
if mode == "build":
	# Get the arguments
	package_name = sys.argv[2].lower()
	distro_name = sys.argv[3].lower()

	# Setup packagetastic
	lib_packagetastic.init_packagetastic(distro_name)

	# Build the package
	lib_packagetastic.build(distro_name, package_name)

# Install a package
if mode == "install":
	# Get the arguments
	package_name = sys.argv[2].lower()
	distro_name = sys.argv[3].lower()

	# Setup packagetastic
	lib_packagetastic.init_packagetastic(distro_name)

	# Build the package
	lib_packagetastic.install(distro_name, package_name)

# Build all packages
if mode == "build_all":
	# Get the arguments
	distro_name = sys.argv[2].lower()

	# Setup packagetastic
	lib_packagetastic.init_packagetastic(distro_name)

	# Get a list of all the stem files
	stem_names = []
	for entry in os.listdir('stems/'):
		if entry.endswith('.stem') and os.path.isfile('stems/' + entry):
			stem_name = entry.split('.stem')[0]
			stem_names.append(stem_name)
	stem_names.sort()

	# Build all the packages
	for package_name in stem_names:
		try:
			lib_packagetastic.build(distro_name, package_name)
		except KeyboardInterrupt:
			raise
		except:
			pass



